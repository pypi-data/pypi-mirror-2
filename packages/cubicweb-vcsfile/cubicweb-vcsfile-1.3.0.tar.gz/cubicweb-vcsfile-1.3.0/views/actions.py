"""actions for entity types defined by the vcsfile package

:organization: Logilab
:copyright: 2007-2009 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"
_ = unicode

from cubicweb.selectors import (one_line_rset, implements, rql_condition,
                                but_etype, score_entity)
from cubicweb.web.action import Action
from cubicweb.web.views.actions import CopyAction

from cubes.vcsfile.entities import rql_revision_content


class VCAction(Action):
    __select__ = one_line_rset() & implements('VersionContent', 'DeletedVersionContent')
    category = 'mainactions'


class VCHeadRevisionAction(VCAction):
    __regid__ = 'revhead'
    __select__ = VCAction.__select__ & rql_condition(
        'X from_revision XR, XR revision V, NV from_revision NVR, '
        'NVR revision > V, X content_for VCF, NV content_for VCF')

    title = _('head revision')
    order = 110

    def url(self):
        return self.build_url(rql='Any NV,NVR,VF ORDERBY NVR DESC LIMIT 1 '
                              'WHERE X from_revision XR, XR revision R, NV from_revision NVR, NVR revision NVR, '
                              'NVR revision > R, X content_for VF, NV content_for VF, '
                              'X eid %s' % self.rset[0][0],
                              vid='primary')


class VCAllRevisionsAction(VCAction):
    __regid__ = 'revall'

    title = _('all revisions')
    order = 110

    def url(self):
        return self.build_url(rql='Any V,VR,VCF ORDERBY VR DESC '
                              'WHERE X content_for VCF, V content_for VCF, '
                              'V from_revision R, R revision VR, X eid %s' % self.rset[0][0],
                              vid='list')


class VCRevisionModifiedFilesAction(VCAction):
    __regid__ = 'revfiles'

    title = _('files modified at this revision')
    order = 120
    category = 'moreactions'

    def url(self):
        entity = self.rset.get_entity(0, 0)
        revision = entity.revision
        repoeid = entity.file.repository.eid
        return self.build_url(rql='Any V,F,D,N ORDERBY D,N '
                              'WHERE V from_revision R, R revision %s, V content_for F, '
                              'F directory D, F name N, F from_repository R, R eid %s'
                              % (revision, repoeid), vid='list')


class VCRevisionAllFilesAction(VCAction):
    __regid__ = 'revallfiles'

    title = _('repository content at this revision')
    order = 121
    category = 'moreactions'

    def url(self):
        entity = self.rset.get_entity(0, 0)
        repoeid = entity.file.repository.eid
        rql, args = rql_revision_content(repoeid, entity.rev.revision,
                                         entity.rev.branch)
        return self.build_url('view', rql=rql % args, vid='list')


class VFAction(Action):
    __select__ = one_line_rset() & implements('VersionedFile')
    category = 'mainactions'


class VFAllRevisionsAction(VFAction):
    __regid__ = 'revall'

    title = _('all revisions')
    order = 110

    def url(self):
        return self.build_url(rql='Any V,X,VR ORDERBY VR DESC '
                              'WHERE V content_for X, V from_revision R, R revision VR, '
                              'X eid %s' % self.rset[0][0])

class VFHEADRevisionAction(VFAction):
    __regid__ = 'revhead'

    title = _('HEAD')
    order = 109

    def url(self):
        vfile = self.rset.get_entity(self.row or 0, self.col or 0)
        return self.build_url(rql='Any V WHERE V content_for X, '
                              'V from_revision R, R revision %s, X eid %s'
                              % (vfile.head.revision, vfile.eid))


# deactivate copy action for entities coming from the svn source
CopyAction.__select__ = CopyAction.__select__ & ~implements(
    'Revision', 'VersionedFile', 'VersionContent', 'DeletedVersionContent')


# you should usually choose between one of the two ways below to submit new
# revisions of versioned files
class VFAddRevisionAction(VFAction):
    __regid__ = 'addrevision'

    title = _('actions_addrevision')
    order = 111

    def url(self):
        vfile = self.rset.get_entity(self.row or 0, self.col or 0)
        linkto = 'from_repository:%s:subject' % vfile.repository.eid
        return self.build_url('add/Revision', vfeid=vfile.eid,
                              __linkto=linkto,
                              __redirectpath=vfile.rest_path(),
                              __redirectvid=self.req.form.get('__redirectvid', ''))


class VFPutUpdateAction(VFAction):
    __regid__ ='vfnewrevaction'

    title = _('upload revision')

    def url(self):
        return self.entity(0, 0).absolute_url(vid='vfnewrevform')


class VFRmAction(VFAction):
    __regid__ = 'vcsrmaction'
    __select__ = VFAction.__select__ & \
                 score_entity(lambda x: not x.deleted_in_branch())

    title = _('mark this file as deleted in the repository')
    category = 'moreactions'

    def url(self):
        return self.entity(0, 0).absolute_url(vid='vcsrmform')
