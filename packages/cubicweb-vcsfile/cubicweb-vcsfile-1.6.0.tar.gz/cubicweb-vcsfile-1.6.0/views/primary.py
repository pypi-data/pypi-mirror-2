"""primary views for entity types defined by the vcsfile package

:organization: Logilab
:copyright: 2007-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"
_ = unicode

from logilab.mtconverter import TransformError, xml_escape

from cubicweb import tags
from cubicweb.mttransforms import ENGINE
from cubicweb.selectors import is_instance
from cubicweb.view import EntityView
from cubicweb.web import uicfg
from cubicweb.web.views import (ibreadcrumbs, idownloadable,
                                baseviews, primary, tabs, navigation)

# primary view tweaks
_pvs = uicfg.primaryview_section
_pvdc = uicfg.primaryview_display_ctrl
_abaa = uicfg.actionbox_appearsin_addmenu

# internal purpose relation
_pvs.tag_subject_of(('*', 'at_revision', '*'), 'hidden')
_pvs.tag_object_of(('*', 'at_revision', '*'), 'hidden')
_pvs.tag_attribute(('Repository', 'local_cache'), 'hidden')

_pvs.tag_attribute(('VersionedFile', 'name'), 'hidden') # in title
_pvs.tag_attribute(('VersionedFile', 'directory'), 'hidden') # in title
_pvs.tag_subject_of(('VersionedFile', 'from_repository', '*'), 'hidden') # in breadcrumb
_pvs.tag_object_of(('*', 'content_for', 'VersionedFile'), 'hidden') # in render_entity_relations

_pvs.tag_subject_of(('Revision', 'parent_revision', 'Revision'), 'attributes')
_pvs.tag_object_of(('Revision', 'parent_revision', 'Revision'), 'attributes')
_pvs.tag_subject_of(('Revision', 'from_repository', '*'), 'hidden') # in breadcrumb
_pvs.tag_object_of(('*', 'from_revision', '*'), 'hidden')

for etype in ('DeletedVersionContent', 'VersionContent'):
    _pvs.tag_attribute((etype, 'revision'), 'hidden')
    _pvs.tag_attribute((etype, 'author'), 'hidden')
    _pvs.tag_subject_of((etype, 'content_for', '*'), 'hidden')

_pvdc.tag_subject_of(('*', 'from_revision', '*'), {'vid': 'incontext'})
_pvdc.tag_subject_of(('*', 'from_repository', '*'), {'vid': 'incontext'})
_pvdc.tag_subject_of(('*', 'content_for', '*'), {'vid': 'incontext'})

_pvdc.tag_attribute(('Repository', 'source_url'), {'vid': 'urlattr'})

# we don't want automatic addrelated action for the following relations...
for rtype in ('from_repository', 'from_revision', 'content_for',
              'parent_revision'):
    _abaa.tag_object_of(('*', rtype, '*'), False)


def render_entity_summary(self, entity):
    if entity.description:
        self.w(tags.div(entity.description, klass='summary'))
    if not entity.is_head(entity.rev.branch):
        msg = self._cw._('this file has newer revisions')
        self.w(tags.div(msg, klass='warning'))


class RepositoryPrimaryView(tabs.TabsMixin, primary.PrimaryView):
    __select__ = is_instance('Repository')

    tabs = [_('repositoryinfo_tab'), _('repositoryfiles_tab'), _('repositoryhistory_tab')]
    default_tab = 'repositoryinfo_tab'

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        entity.complete()
        self.render_entity_title(entity)
        self.render_tabs(self.tabs, self.default_tab, entity)


class RepositoryInfoTab(primary.PrimaryView):
    __regid__ = 'repositoryinfo_tab'
    __select__ = is_instance('Repository')

    def render_entity_title(self, entity):
        pass

    def render_entity_attributes(self, entity):
        super(RepositoryInfoTab, self).render_entity_attributes(entity)
        rset = self._cw.execute('Any REV, REVB, REVN ORDERBY REVN DESC '
                                'WHERE REV branch REVB, REV revision REVN, REV from_repository R, '
                                'R eid %(r)s, NOT X parent_revision REV',
                                {'r': entity.eid})
        if rset:
            self.w('<h3>%s</h3>' % self._cw._('heads'))
            self.wview('table', rset)


class RepositoryFilesTab(EntityView):
    __regid__ = 'repositoryfiles_tab'
    __select__ = is_instance('Repository')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        rset = self._cw.execute(
            'Any VF,VFMD, VFD,VFN ORDERBY VFD,VFN WHERE '
            'VF modification_date VFMD, VF directory VFD, VF name VFN,'
            'VF from_repository X, X eid %(x)s',
            {'x': entity.eid})
        self.wview('table', rset, 'noresult',
                   paginate=True, displayfilter=True,
                   displaycols=[0, 1], cellvids={0: 'incontext'})


class RepositoryHistoryTab(EntityView):
    __regid__ = 'repositoryhistory_tab'
    __select__ = is_instance('Repository')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        rset = self._cw.execute(
            'Any R,RB,RA,RD,RCD, RN,RCS ORDERBY RN DESC WHERE '
            'R branch RB, R author RA, R description RD, R creation_date RCD,'
            'R revision RN, R changeset RCS, R from_repository X, X eid %(x)s',
            {'x': entity.eid})
        self.wview('table', rset, 'noresult',
                   paginate=True, displayfilter=True, displaycols=range(5))


class DVCPrimaryView(primary.PrimaryView):
    __select__ = is_instance('DeletedVersionContent')

    def render_entity_title(self, entity):
        title = self._cw._('Revision %(revision)s of %(file)s: DELETED') % {
            'revision': entity.revision, 'file': entity.file.view('oneline')}
        self.w('<h1>%s</h1>' % title)

    render_entity_summary = render_entity_summary


class VCPrimaryView(idownloadable.IDownloadablePrimaryView):
    __select__ = is_instance('VersionContent')

    def render_entity_title(self, entity):
        title = self._cw._('Revision %(revision)s of %(file)s') % {
            'revision': entity.revision, 'file': entity.file.view('oneline')}
        self.w('<h1>%s</h1>' % title)

    render_entity_summary = render_entity_summary


class VCMetaDataView(baseviews.MetaDataView):
    """paragraph view of some metadata"""
    __select__ = is_instance('VersionContent', 'DeletedVersionContent')

    def cell_call(self, row, col):
        _ = self._cw._
        entity = self.cw_rset.get_entity(row, col)
        self.w(u'<div class="metadata">')
        self.w(u'#%s - ' % entity.eid)
        self.w(u'<span>%s</span> ' % _('revision %s of') % entity.revision)
        self.w(u'<span class="value">%s</span>,&nbsp;'
               % xml_escape(entity.file.path))
        self.w(u'<span>%s</span> ' % _('created on'))
        self.w(u'<span class="value">%s</span>'
               % entity.rev.printable_value('creation_date'))
        if entity.author:
            self.w(u'&nbsp;<span>%s</span> ' % _('by'))
            self.w(tags.span(entity.author, klass='value'))
        self.w(u'</div>')

class VCRevisionView(EntityView):
    __regid__ = 'revision'
    __select__ = is_instance('VersionContent', 'DeletedVersionContent')

    def cell_call(self, row, col):
        vc = self.cw_rset.get_entity(row, col)
        self.w(u'<a href="%s">' % vc.absolute_url())
        vc.rev.view('shorttext', w=self.w)
        self.w(u'</a>')

class RevisionShortView(EntityView):
    __regid__ = 'shorttext'
    __select__ = is_instance('Revision')
    content_type = 'text/plain'

    def cell_call(self, row, col):
        rev = self.cw_rset.get_entity(row, col)
        if rev.changeset:
            self.w(u'#%s:%s' % (rev.revision, rev.changeset))
        else:
            self.w(u'#%s' % rev.revision)


class VFPrimaryView(primary.PrimaryView):
    __select__ = is_instance('VersionedFile')

    def render_entity_attributes(self, entity):
        super(VFPrimaryView, self).render_entity_attributes(entity)
        self.w(u'<div class="content">')
        if entity.deleted_in_branch():
            self.w(_('this file is currently deleted in the version control system'))
        else:
            head = entity.head
            contenttype = head.cw_adapt_to('IDownloadable').download_content_type()
            self.field('head', head.rev.view('incontext'))
            if contenttype.startswith('image/'):
                self.wview('image', head.cw_rset, row=head.cw_row)
            else:
                try:
                    if ENGINE.has_input(contenttype):
                        self.w(head.printable_value('data'))
                except TransformError:
                    pass
                except Exception, ex:
                    msg = self._cw._("can't display data, unexpected error: %s") % ex
                    self.w('<div class="error">%s</div>' % xml_escape(msg))
        self.w(u'</div>')

    def render_entity_relations(self, entity):
        super(VFPrimaryView, self).render_entity_relations(entity)
        self.w(u'<h3>%s</h3>' % self._cw._('Revisions for this file'))
        rset = self._cw.execute(
            'Any VC,RB,RA,RD,RC, R ORDERBY R DESC WHERE '
            'VC content_for VF, VC from_revision R, '
            'R branch RB, R author RA, R description RD, R creation_date RC,'
            'VF eid %(x)s',
            {'x': entity.eid})
        self.wview('table', rset, 'noresult',
                   paginate=True, displayfilter=True,
                   displaycols=range(5),
                   cellvids={0: 'revision'})


class RevisionPrimaryView(primary.PrimaryView):
    __select__ = is_instance('Revision')

    def render_entity_relations(self, rev):
        versioned = rev.reverse_from_revision
        if versioned:
            self.w(u'<table class="listing">')
            self.w(u'<tr><th>%s</th></tr>' %
                   self._cw._('files modified by this revision'))
            for obj in versioned:
                self.w(u'<tr><td><a href="%s">%s</a></td></tr>' % (
                    obj.absolute_url(), xml_escape(obj.dc_title())))
            self.w(u'</table>')
        else:
            self.w(u'<p>%s</p>' % self._cw._('this revision hasn\'t modified any files'))


# navigation: breadcrumbs / prevnext adapters ##################################


class RevisionIPrevNextAdapter(navigation.IPrevNextAdapter):
    __select__ = is_instance('Revision')

    def previous_entity(self): # IPrevNext
        # may have multiple parents, take the first one in the same branch...
        rset = self._cw.execute('Any X LIMIT 1 WHERE R parent_revision X , '
                                'R eid %(r)s, X branch %(branch)s',
                                {'r': self.entity.eid, 'branch': self.entity.branch})
        if rset:
            return rset.get_entity(0, 0)

    def next_entity(self): # IPrevNext
        # may have multiple children, take the first one in the same branch...
        rset = self._cw.execute('Any X LIMIT 1 WHERE X parent_revision R , '
                                'R eid %(r)s, X branch %(branch)s',
                                {'r': self.entity.eid, 'branch': self.entity.branch})
        if rset:
            return rset.get_entity(0, 0)


class RepoContentIBreadCrumbsAdapter(ibreadcrumbs.IBreadCrumbsAdapter):
    __select__ = is_instance('Revision', 'VersionedFiled')

    def parent_entity(self):
        try:
            return self.entity.repository
        except Unauthorized:
            return None


class DVCBreadCrumbView(ibreadcrumbs.BreadCrumbView):
    __regid__ = 'breadcrumbtext'
    __select__ = is_instance('VersionContent', 'DeletedVersionContent')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(entity.rev.dc_title())


class DVCIPrevNextAdapter(navigation.IPrevNextAdapter):
    __select__ = is_instance('VersionContent', 'DeletedVersionContent')

    def previous_entity(self):
        rset = self._cw.execute('Any PV,R,PVR,VF ORDERBY PVR DESC LIMIT 1 '
                                'WHERE PV from_revision R, R revision PVR, '
                                'R branch %(b)s, PV content_for VF, '
                                'R revision < %(r)s, VF eid %(vf)s',
                                {'r': self.entity.rev.revision, 'b': self.entity.rev.branch,
                                 'vf': self.entity.file.eid})
        if rset:
            return rset.get_entity(0, 0)

    def next_entity(self):
        rset = self._cw.execute('Any NV,R,NVR,VF ORDERBY NVR ASC LIMIT 1 '
                                'WHERE NV from_revision R, R revision NVR, '
                                'R branch %(b)s, NV content_for VF, '
                                'R revision > %(r)s, VF eid %(vf)s',
                                {'r': self.entity.rev.revision, 'b': self.entity.rev.branch,
                                 'vf': self.entity.file.eid})
        if rset:
            return rset.get_entity(0, 0)


class DVCIBreadCrumbsAdapter(ibreadcrumbs.IBreadCrumbsAdapter):
    __select__ = is_instance('VersionContent', 'DeletedVersionContent')

    def parent(self): # for breadcrumbs
        return self.entity.file
