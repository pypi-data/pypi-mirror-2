# -*- coding: utf-8 -*-
"""hooks for vcsfile content types

:organization: Logilab
:copyright: 2007-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"

import os

from logilab.mtconverter import need_guess, guess_mimetype_and_encoding

from cubicweb import QueryError, ValidationError, Binary
from cubicweb.server import hook
from cubicweb.server.hook import Hook, Operation, set_operation
from cubicweb.selectors import is_instance

from cubes.vcsfile import IMMUTABLE_ATTRIBUTES, bridge

def missing_relation_error(entity, rtype):
    # use __ since msgid recorded in cw, we don't want to translate it in
    # this cube
    __ = entity._cw._
    msg = __('at least one relation %(rtype)s is required on %(etype)s (%(eid)s)')
    errors = {'from_repository': msg % {'rtype': __(rtype),
                                        'etype': __(entity.__regid__),
                                        'eid': entity.eid}}
    return ValidationError(entity.eid, errors)

# initialization hooks #########################################################

class ServerStartupHook(Hook):
    """synchronize repository on server startup, and install attribute map
    on the system source sql generator
    """
    __regid__ = 'vcsfile.serverstartuphook'
    events = ('server_startup', 'server_maintenance')
    def __call__(self):
        repo = self.repo
        repo.system_source.set_storage('VersionContent', 'data',
                                       bridge.VCSStorage())
        if self.event == 'server_startup' and repo.config['repository-import']:
            repo.looping_task(repo.config.get('check-revision-interval', 5*60),
                              bridge.import_content, repo,
                              repo.config.get('check-revision-commit-every', 1))

# internals to be able to create new vcs repo revision using rql queries #######

class VCTransactionOp(Operation):

    def precommit_event(self):
        bridge.set_at_revision(self.session, self.revision.eid)

    def revertprecommit_event(self):
        transactions = self.session.transaction_data.setdefault('vctransactions', {})
        for transaction in transactions.itervalues():
            transaction.rollback()

    def commit_event(self):
        transactions = self.session.transaction_data.setdefault('vctransactions', {})
        for transaction in transactions.itervalues():
            transaction.commit()

    revertcommit_event = revertprecommit_event

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
    events = ('after_add_entity',)
    __select__ = Hook.__select__ & is_instance('DeletedVersionContent',
                                              'VersionContent')
    def __call__(self):
        set_operation(self._cw, 'vcsfile.modifiedvfs', self.entity,
                      VFModificationDateOp)


class AddRevisionHook(Hook):
    __regid__ = 'vcsfile.add_revision_hook'
    events = ('before_add_entity',)
    __select__ = Hook.__select__ & is_instance('Revision')

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
    events = ('before_add_entity',)
    __select__ = Hook.__select__ & is_instance('VersionContent')

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
    events = ('before_add_entity',)
    __select__ = Hook.__select__ & is_instance('DeletedVersionContent')

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
    events = ('before_add_entity',)
    __select__ = Hook.__select__ & is_instance('VersionedFile')

    def __call__(self):
        # skip further processing if the revision is being imported from the
        # vcs repository
        if self._cw.is_internal_session:
            return
        CheckVersionedFileOp(self._cw, entity=self.entity)

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


class CheckImmutalbeAttributeHook(Hook):
    __regid__ = 'vcsfile.check_immutable_attribute_hook'
    events = ('before_update_entity',)
    __select__ = Hook.__select__ & is_instance('Revision', 'DeletedVersionContent',
                                              'VersionContent')

    def __call__(self):
        for attr in self.entity.keys():
            if attr == 'eid':
                continue
            if '%s.%s' % (self.entity.__regid__, attr) in IMMUTABLE_ATTRIBUTES:
                raise QueryError('%s attribute is not editable' % attr)


class UpdateRepositoryHook(Hook):
    """add repository eid to vcs bridge cache"""
    __regid__ = 'vcsfile.update_repository_hook'
    events = ('before_update_entity', )
    __select__ = Hook.__select__ & is_instance('Repository')
    def __call__(self):
        # XXX check value actually changed
        try:
            edited = self.entity.edited_attributes
        except AttributeError:
            edited = self.entity
        if 'path' in edited:
            msg = self._cw._('updating path attribute of a repository isn\'t '
                            'supported. Delete it and add a new one.')
            raise QueryError(msg)
        if 'type' in edited:
            msg = self._cw._('updating type attribute of a repository isn\'t '
                            'supported. Delete it and add a new one.')
            raise QueryError(msg)


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
