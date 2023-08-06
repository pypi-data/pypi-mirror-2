# -*- coding: utf-8 -*-
"""hooks for vcsfile content types

:organization: Logilab
:copyright: 2007-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"

import os
import os.path as osp
import shutil

from logilab.mtconverter import need_guess, guess_mimetype_and_encoding

from cubicweb import QueryError, ValidationError, Binary
from cubicweb.server import hook
from cubicweb.server.hook import Hook, Operation, set_operation
from cubicweb.selectors import is_instance, score_entity

from cubes.vcsfile import IMMUTABLE_ATTRIBUTES, bridge

def repo_cache_dir(config):
    directory = config['local-repo-cache-root']
    if not osp.isabs(directory):
        directory = osp.join(config.appdatahome, directory)
        if not config.repairing: # don't change value during migration
            config['local-repo-cache-root'] = directory
    if not osp.exists(directory):
        try:
            os.makedirs(directory)
        except:
            config.critical('could not find local repo cache directory; check '
                            'local-repo-cache-root option whose present value is %r)',
                            config['local-repo-cache-root'])
            raise
    return directory

def url_to_relative_path(url):
    scheme, url = url.split('://', 1)
    if scheme == 'file':
        return url.rstrip('/').rsplit('/', 1)[-1]
    else:
        return url.rstrip('/').rsplit('/', 1)[1]

def set_local_cache(vcsrepo):
    cachedir = osp.join(repo_cache_dir(vcsrepo._cw.vreg.config),
                        unicode(vcsrepo.eid))
    if not osp.exists(cachedir):
        try:
            os.makedirs(cachedir)
        except OSError:
            vcsrepo.exception('cant create repo cache directory %s', cachedir)
            return
    try:
        vcsrepo['local_cache'] = osp.join(
            unicode(vcsrepo.eid), url_to_relative_path(vcsrepo.source_url))
    except (IndexError, ValueError):
        # do nothing, validation error should be raised by another hook
        pass

def clone_to_local_cache(vcsrepo):
    handler = bridge.repository_handler(vcsrepo)
    url = vcsrepo.source_url
    try:
        handler.pull_or_clone_cache(url)
    except Exception:
        handler.exception('while trying to clone repo %s', url)
        msg = vcsrepo._cw._('can not clone the repo from %s, '
                            'please check the source url')
        raise ValidationError(vcsrepo.eid, {'source_url': msg % url})


def missing_relation_error(entity, rtype):
    # use __ since msgid recorded in cw, we don't want to translate it in
    # this cube
    __ = entity._cw._
    msg = __('at least one relation %(rtype)s is required on %(etype)s (%(eid)s)')
    errors = {'from_repository': msg % {'rtype': __(rtype),
                                        'etype': __(entity.__regid__),
                                        'eid': entity.eid}}
    return ValidationError(entity.eid, errors)

def missing_attribute_error(entity, attrs):
    msg = _('at least one attribute of %s must be set on a Repository')
    errors = {}
    for attr in attrs:
        errors[attr] = msg % ', '.join(attrs)
    return ValidationError(entity.eid, errors)


# initialization hooks #########################################################

class ServerMaintenanceHook(Hook):
    """install attribute map on the system source sql generator
    """
    __regid__ = 'vcsfile.servermaintenancehook'
    events = ('server_maintenance',)
    def __call__(self):
        repo = self.repo
        repo.system_source.set_storage('VersionContent', 'data',
                                       bridge.VCSStorage())


class ServerStartupHook(Hook):
    """synchronize repository on server startup, and install attribute map
    on the system source sql generator
    """
    __regid__ = 'vcsfile.serverstartuphook'
    events = ('server_startup',)
    def __call__(self):
        repo = self.repo
        repo.system_source.set_storage('VersionContent', 'data',
                                       bridge.VCSStorage())
        cacheroot = repo_cache_dir(repo.config)
        if not os.access(cacheroot, os.W_OK):
            raise ValueError, ('directory %r is not writable '
                               '(check  option)' % (cacheroot, CACHEROOT))

        def refresh_local_hgrepo_caches(repo, osp=osp, bridge=bridge,
                                        cacheroot=cacheroot):
            session = repo.internal_session()
            try:
                reposrset = session.execute(
                    'Any R, RT, RLC, RSU, RP WHERE R is Repository, '
                    'R type "mercurial", NOT R local_cache NULL, '
                    'R type RT, R local_cache RLC, '
                    'R source_url RSU, R path RP')
                for vcsrepo in reposrset.entities():
                    # XXX when this will be available, filter according to
                    # source in the rql query instead of the test below
                    # used to discard repository from external sources
                    if vcsrepo.cw_metainformation()['source']['uri'] != 'system':
                        continue
                    try:
                        repohdlr = bridge.repository_handler(vcsrepo)
                    except bridge.VCSException, ex:
                        repo.error(str(ex))
                        continue
                    except Exception:
                        repo.exception('error while retreiving handler for %s',
                                       vcsrepo.eid)
                        continue
                    try:
                        repohdlr.pull_or_clone_cache(vcsrepo.source_url)
                    except Exception:
                        repohdlr.exception(
                            'error while updating local cache of repository %s',
                            vcsrepo.eid)
                    if repo.config['repository-import']:
                        bridge.import_vcsrepo_content(
                            session, repohdlr, vcsrepo,
                            commitevery=repo.config.get('check-revision-commit-every', 1))
            finally:
                session.close()

        repo.looping_task(repo.config.get('check-revision-interval'),
                          refresh_local_hgrepo_caches, repo)


# internals to be able to create new vcs repo revision using rql queries #######

class VCTransactionOp(Operation):

    def precommit_event(self):
        bridge.set_at_revision(self.session, self.revision.eid)
        transactions = self.session.transaction_data.setdefault('vctransactions', {})
        for transaction in transactions.itervalues():
            transaction.precommit()

    def revertprecommit_event(self):
        transactions = self.session.transaction_data.pop('vctransactions', {})
        for transaction in transactions.itervalues():
            transaction.rollback()

    def commit_event(self):
        transactions = self.session.transaction_data.setdefault('vctransactions', {})
        for transaction in transactions.itervalues():
            transaction.commit()

    def rollback_event(self):
        transactions = self.session.transaction_data.setdefault('vctransactions', {})
        for transaction in transactions.itervalues():
            transaction.rollback()


class VFModificationDateOp(Operation):
    def precommit_event(self):
        for entity in self.session.transaction_data.pop('vcsfile.modifiedvfs'):
            entity.file.set_attributes(modification_date=entity.rev.creation_date)


class UpdateVFModificationDateHook(Hook):
    __regid__ = 'vcsfile.update_vf_mdate'
    __select__ = Hook.__select__ & is_instance('DeletedVersionContent',
                                               'VersionContent')
    events = ('after_add_entity',)

    def __call__(self):
        set_operation(self._cw, 'vcsfile.modifiedvfs', self.entity,
                      VFModificationDateOp)


class AddRevisionHook(Hook):
    __regid__ = 'vcsfile.add_revision_hook'
    __select__ = Hook.__select__ & is_instance('Revision')
    events = ('before_add_entity',)

    def __call__(self):
        entity = self.entity
        session = self._cw
        if not entity.get('revision'):
            # new revision to be created, set a temporary value
            entity['revision'] = 0
        # skip further processing if the revision is being imported from the
        # vcs repository
        if session.is_internal_session:
            return
        try:
            vcsrepoeid = entity['from_repository']
        except KeyError:
            vcsrepoeid = session.transaction_data.pop('vcsrepoeid', None)
            if vcsrepoeid is None:
                raise missing_relation_error(entity, 'from_repository')
        revision = entity.get('revision', 0)
        if revision > 0: # set to 0 by hook
            raise QueryError("can't specify revision")
        transactions = session.transaction_data.setdefault('vctransactions', {})
        # should not have multiple transaction on the same repository
        if vcsrepoeid in transactions:
            raise QueryError('already processing a new revision')
        vcsrepohdlr = bridge.repository_handler(
            session.entity_from_eid(vcsrepoeid))
        transaction = vcsrepohdlr.revision_transaction(session, entity)
        transaction.reveid = entity.eid
        transactions[vcsrepoeid] = transaction
        entity['revision'] = transaction.rev
        VCTransactionOp(session, revision=entity)


class AddVersionContentHook(Hook):
    __regid__ = 'vcsfile.add_version_content_hook'
    __select__ = Hook.__select__ & is_instance('VersionContent')
    events = ('before_add_entity',)

    def __call__(self):
        session = self._cw
        entity = self.entity
        if need_guess(entity.get('data_format'), entity.get('data_encoding')):
            vf = entity._vc_vf()
            encoding = vf.repository.encoding
            mt, enc = guess_mimetype_and_encoding(data=entity.get('data'),
                                                  filename=vf.name,
                                                  fallbackencoding=encoding)
            if mt and not entity.get('data_format'):
                entity['data_format'] = unicode(mt)
            if enc and not entity.get('data_encoding'):
                entity['data_encoding'] = unicode(enc)


class AddDeletedVersionContentHook(Hook):
    __regid__ = 'vcsfile.add_deleted_version_content_hook'
    __select__ = Hook.__select__ & is_instance('DeletedVersionContent')
    events = ('before_add_entity',)

    def __call__(self):
        # skip further processing if the revision is being imported from the
        # vcs repository
        if self._cw.is_internal_session:
            return
        vcsrepohdlr, transaction = self.entity._vc_prepare()
        vf = self.entity._vc_vf()
        vcsrepohdlr.add_versioned_file_deleted_content(self._cw, transaction, vf,
                                                       self.entity)


class AddVersionedFileHook(Hook):
    __regid__ = 'vcsfile.add_versioned_file_hook'
    __select__ = Hook.__select__ & is_instance('VersionedFile')
    events = ('before_add_entity',)

    def __call__(self):
        # skip further processing if the revision is being imported from the
        # vcs repository
        if self._cw.is_internal_session:
            return
        CheckVersionedFileOp(self._cw, entity=self.entity)


class SetRepoCacheBeforeAdd(Hook):
    """clone just after repo creation
    mostly helps the tests
    """
    __regid__ = 'clone_hgrepo_after_add'
    __select__ = (Hook.__select__ & is_instance('Repository'))
    events = ('before_add_entity',)
    order = 2

    def __call__(self):
        repo = self.entity
        if repo.type == 'mercurial' and repo.source_url and not repo.path:
            set_local_cache(repo)


class CloneRepoAfterAdd(Hook):
    """clone just after repo creation, to allow operation which needs local
    access and get quicker checkout if test are running on the same host
    """
    __regid__ = 'clone_hgrepo_after_add'
    __select__ = (Hook.__select__ & is_instance('Repository'))
    events = ('after_add_entity',)
    order = 2

    def __call__(self):
        vcsrepo = self.entity
        if not vcsrepo.local_cache:
            return
        # XXX rmdir on rollback
        clone_to_local_cache(vcsrepo)


class UpdateRepositoryHook(Hook):
    """add repository eid to vcs bridge cache"""
    __regid__ = 'vcsfile.update_repository_hook'
    __select__ = Hook.__select__ & is_instance('Repository')
    events = ('before_update_entity', )

    def __call__(self):
        vcsrepo = self.entity
        if 'type' in vcsrepo.edited_attributes:
            msg = self._cw._('updating type attribute of a repository isn\'t '
                             'supported. Delete it and add a new one.')
            raise ValidationError(vcsrepo.eid, {'type': msg})
        if 'path' in vcsrepo.edited_attributes or 'local_cache' in vcsrepo.edited_attributes:
            bridge._REPOHDLRS.pop(vcsrepo.eid, None)
        if (vcsrepo.type == 'mercurial' and vcsrepo.source_url
            and not vcsrepo.path and not vcsrepo.local_cache):
            # XXX rmdir on rollback
            set_local_cache(vcsrepo)
            clone_to_local_cache(vcsrepo)


class DeleteRepositoryHook(Hook):
    __regid__ = 'vcsfile.add_update_repository_hook'
    __select__ = (Hook.__select__ &
                  is_instance('Repository') &
                  score_entity(lambda x:x.local_cache))
    events = ('before_delete_entity',)

    def __call__(self):
        if self.entity.local_cache:
            cachedir = osp.dirname(osp.join(
                self._cw.vreg.config['local-repo-cache-root'],
                self.entity.local_cache)).encode('ascii')
            set_operation(self._cw, 'vcsfile.deletedirs', cachedir,
                          DeleteDirsOp)

class DeleteDirsOp(Operation):

    def postcommit_event(self):
        for cachedir in self.session.transaction_data.pop('vcsfile.deletedirs'):
            try:
                shutil.rmtree(cachedir)
                self.info('deleted repository cache at %s', cachedir)
            except:
                self.exception('cant delete repository cache at %s', cachedir)


# safety belts #################################################################

def _check_in_transaction(vf_or_rev):
    """check that a newly added versioned file or revision entity is done in
    a vcs repository transaction.
    """
    try:
        vcsrepo = vf_or_rev.from_repository[0]
    except IndexError:
        raise missing_relation_error(vf_or_rev, 'from_repository')
    try:
        transactions = vcsrepo._cw.transaction_data['vctransactions']
        transaction = transactions[vcsrepo.eid]
    except KeyError:
        raise QueryError('no transaction in progress for repository %s'
                         % vcsrepo.eid)
    return transaction


class CheckVersionedFileOp(Operation):
    """check transaction consistency when adding new revision using rql queries
    """
    def precommit_event(self):
        _check_in_transaction(self.entity)


class CheckRevisionOp(Operation):
    """check transaction consistency when adding new revision using rql queries
    """
    def precommit_event(self):
        try:
            revision = self.entity.from_revision[0]
        except IndexError:
            raise missing_relation_error(self.entity, 'from_revision')
        transaction = _check_in_transaction(revision)
        if not transaction.reveid == revision.eid:
            raise QueryError('entity linked to a bad revision')


class CheckImmutableAttributeHook(Hook):
    __regid__ = 'vcsfile.check_immutable_attribute_hook'
    __select__ = Hook.__select__ & is_instance(
        'Revision', 'DeletedVersionContent', 'VersionContent')
    events = ('before_update_entity',)

    def __call__(self):
        for attr in self.entity.keys():
            if attr == 'eid':
                continue
            if '%s.%s' % (self.entity.__regid__, attr) in IMMUTABLE_ATTRIBUTES:
                raise QueryError('%s attribute is not editable' % attr)


class AddUpdateRepositoryHook(Hook):
    __regid__ = 'vcsfile.add_update_repository_hook'
    __select__ = Hook.__select__ & is_instance('Repository')
    events = ('after_add_entity', 'after_update_entity')
    required_attrs = ('path', 'source_url')
    order = 1

    def __call__(self):
        entity = self.entity
        if entity.path and not osp.isabs(self.entity.path):
            msg = self._cw._('path must be absolute')
            raise ValidationError(self.entity.eid, {'path': msg})
        if entity.type == 'subversion' and not entity.path:
            msg = self._cw._('path is mandatory for subversion repositories')
            raise ValidationError(entity.eid, {'path': msg})
        if not entity.source_url and not entity.path:
            raise missing_attribute_error(entity, self.required_attrs)
        if entity.source_url and not entity.path and not entity.local_cache:
            try:
                url_to_relative_path(entity.source_url)
            except:
                msg = self._cw._('url must be of the form protocol://path/to/stuff')
                raise ValidationError(entity.eid, {'source_url': msg})

# folder/tag extensions ########################################################

class ClassifyVersionedFileHook(Hook):
    """classifies VersionedFile automatically according to their path in the
    repository (require cubicweb-tag and/or cubicweb-folder installed)
    """
    __regid__ = 'vcsfile.classify_versioned_file_hook'
    events = ('after_add_entity', )
    __select__ = Hook.__select__ & is_instance('VersionedFile')

    def __call__(self):
        try:
            rschema = self._cw.vreg.schema['tags']
            support_tags = ('Tag', self.entity.e_schema) in rschema.rdefs
        except KeyError:
            support_tags = False
        try:
            rschema = self._cw.vreg.schema['filed_under']
            support_folders = (self.entity.e_schema, 'Folder') in rschema.rdefs
        except KeyError:
            support_folders = False
        if not (support_tags or support_folders):
            return
        for directory in self.entity.directory.split(os.sep):
            if not directory:
                continue
            if support_tags:
                rset = self._cw.execute('Tag X WHERE X name %(name)s',
                                       {'name': directory})
                if rset:
                    self._cw.execute('SET T tags X WHERE X eid %(x)s, T eid %(t)s',
                                    {'x': self.entity.eid, 't': rset[0][0]})
            if support_folders:
                rset = self._cw.execute('Folder X WHERE X name %(name)s',
                                       {'name': directory})
                if rset:
                    self._cw.execute('SET X filed_under F WHERE X eid %(x)s, F eid %(f)s',
                                    {'x': self.entity.eid, 'f': rset[0][0]})
