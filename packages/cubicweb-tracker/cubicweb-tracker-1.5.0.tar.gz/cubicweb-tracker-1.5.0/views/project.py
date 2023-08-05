"""views for Project entities

:organization: Logilab
:copyright: 2006-2009 LOGILAB S.A. (Paris, FRANCE), license is LGPL.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"
_ = unicode

from logilab.mtconverter import xml_escape
from logilab.common import table as _table

from cubicweb.schema import display_name
from cubicweb.view import EntityView, EntityStartupView
from cubicweb.selectors import (implements, has_related_entities, none_rset,
                                anonymous_user, authenticated_user, score_entity)
from cubicweb import tags
from cubicweb.web import component, uicfg
from cubicweb.web.views import tabs, baseviews

_pvdc = uicfg.primaryview_display_ctrl
_pvdc.tag_attribute(('Project', 'summary'), {'showlabel': False})
_pvdc.tag_attribute(('Project', 'description'), {'showlabel': False})

# primary view and tabs ########################################################

class ProjectPrimaryView(tabs.TabbedPrimaryView):
    __select__ = implements('Project')

    tabs = [_('projectinfo_tab'), _('projectroadmap_tab'), _('projecttickets_tab')]
    default_tab = 'projectinfo_tab'


# configure projectinfotab
_pvs = uicfg.primaryview_section
_pvs.tag_attribute(('Project', 'name'), 'hidden')
# XXX keep '*', not Project to match other target types added in eg forge
_pvs.tag_subject_of(('Project', 'uses', '*'), 'attributes')
_pvs.tag_object_of(('Project', 'uses', '*'), 'attributes')
_pvs.tag_object_of(('Project', 'subproject_of', '*'), 'hidden')
_pvs.tag_subject_of(('*', 'subproject_of', 'Project'), 'hidden')

class ProjectInfoTab(tabs.PrimaryTab):
    __regid__ = 'projectinfo_tab'
    __select__ = implements('Project')

    title = None # should not appear in possible views


class ProjectRoadmapTab(EntityView):
    """display the latest published version and in preparation version"""
    __regid__ = 'projectroadmap_tab'
    __select__ = (anonymous_user() & implements('Project') &
                  has_related_entities('version_of', 'object'))

    title = None # should not appear in possible views

    def cell_call(self, row, col):
        self.cw_rset.get_entity(row, col).view('roadmap', w=self.w)


class ProjectTicketsTab(EntityView):
    __regid__ = 'projecttickets_tab'
    __select__ = implements('Project')

    title = None # should not appear in possible views

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        # optimization: prefetch project's to fill entity / relations cache
        entity.reverse_version_of
        rset = self._cw.execute(entity.tickets_rql(limit=1))
        self._cw.form['actualrql'] = entity.active_tickets_rql()
        self.wview('editable-initialtable', rset, 'null',
                   subvid='incontext', displayactions=1,
                   divid='tickets%s' % entity.eid,
                   displaycols=range(entity.tickets_rql_nb_displayed_cols))


# contextual components ########################################################

class ProjectRoadmapVComponent(component.EntityVComponent):
    """display the latest published version and in preparation version"""
    __regid__ = 'roadmap'
    __select__ = (component.EntityVComponent.__select__ &
                  authenticated_user() & implements('Project') &
                  has_related_entities('version_of', 'object'))
    context = 'navcontenttop'
    title = _('Version_plural')
    order = 10

    def cell_call(self, row, col, view=None):
        self.cw_rset.get_entity(row, col).view('roadmap', w=self.w)


class ProjectTreeVComponent(component.EntityVComponent):
    __regid__ = 'projecttree'
    title = _('project tree')
    __select__ = (component.EntityVComponent.__select__ &
                  implements('Project') &
                  score_entity(lambda x: x.children()))
    context = 'navcontentbottom'

    def cell_call(self, row, col, view=None):
        entity = self.cw_rset.get_entity(row, col)
        rset = entity.children(entities=False)
        if rset:
            self.w(u'<div class="section">')
            self.w(tags.h2(self._cw._('Project tree')))
            treeid = 'project_tree_%s' % entity.eid
            self.w(self.view('treeview', rset=rset, treeid=treeid,
                             initial_thru_ajax=True))
            self.w(u'</div>')


# secondary views ##############################################################

class ProjectRoadmapView(EntityView):
    """display the latest published version and in preparation version"""
    __regid__ = 'roadmap'
    __select__ = (implements('Project') &
                  has_related_entities('version_of', 'object'))
    title = None # should not appear in possible views
    rql = ('Any V,DATE ORDERBY version_sort_value(N) '
           'WHERE V num N, V prevision_date DATE, V version_of X, '
           'V in_state S, S name IN ("planned", "dev", "ready"), '
           'X eid %(x)s')

    def cell_call(self, row, col):
        self.w(u'<div class="section">')
        entity = self.cw_rset.get_entity(row, col)
        currentversion = entity.latest_version()
        if currentversion:
            self.w(self._cw._('latest published version:'))
            self.w(u'&nbsp;')
            currentversion.view('incontext', w=self.w)
            self.w(u'<br/>')
        rset = self._cw.execute(self.rql, {'x': entity.eid}, 'x')
        if rset:
            self.wview('ic_progress_table_view', rset)
        allversionsrql = entity.related_rql('version_of', 'object') % {'x': entity.eid}
        self.w('<a href="%s">%s</a>'
               % (xml_escape(self._cw.build_url(vid='list', rql=allversionsrql)),
                  self._cw._('view all versions')))
        self.w(u'</div>')


class ProjectOutOfContextView(baseviews.OutOfContextView):
    """project's out of context view display project's url, which is not
    displayed in the one line / text views
    """
    __select__ = implements('Project')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(tags.a(entity.name, href=entity.absolute_url()))
        # no summary on ext project
        if getattr(entity, 'summary', None):
            self.w(u'&nbsp;')
            self.w(xml_escape(entity.summary))


# other views ##################################################################

class ProjectStatsView(EntityStartupView):
    """Some statistics : how many bugs, sorted by status, indexed by projects
    """
    __regid__ = 'stats'
    __select__ = none_rset() | implements('Project')
    title = _('projects statistics')
    default_rql = 'Any P,PN WHERE P name PN, P is Project'

    def call(self, sort_col=None):
        w = self.w
        req = self._cw
        req.add_css('cubes.tracker.stats.css')
        if self.cw_rset is None:
            self.cw_rset = req.execute(self.default_rql)
        table = _table.Table()
        statuslist = [row[0] for row in self._cw.execute('DISTINCT Any N WHERE S name N, X in_state S, X is Ticket')]
        severities = ['minor', 'normal', 'important']
        table.create_columns(statuslist + severities + ['Total'])
        nb_cols = len(table.col_names)
        # create a stylesheet to compute sums over rows and cols
        stylesheet = _table.TableStyleSheet()
        # fill table
        i = -1
        for row in self.cw_rset:
            i += 1
            eid = row[0]
            row = []
            total = 0
            for status in statuslist:
                rql = "Any COUNT(A) WHERE A is Ticket, A concerns P, A in_state S, S name %(s)s, P eid %(x)s"
                nbtickets = req.execute(rql, {'x': eid, 's': status}, 'x', build_descr=0)[0][0]
                total += nbtickets
                row.append(nbtickets)
            for severity in severities:
                rql = "Any COUNT(A) WHERE A is Ticket, A concerns P, A priority %(p)s, P eid %(x)s"
                nbtickets = req.execute(rql, {'x': eid, 'p': severity}, 'x', build_descr=0)[0][0]
                total += nbtickets
                row.append(nbtickets)
            row.append(total)
            table.append_row(row, xml_escape(self.cw_rset.get_entity(i, 0).name))
            assert len(row) == nb_cols
        # sort table according to sort_col if wanted
        sort_col = sort_col or self._cw.form.get('sort_col', '')
        if sort_col:
            table.sort_by_column_id(sort_col, method='desc')
        else:
            table.sort_by_column_index(0)
        # append a row to compute sums over rows and add appropriate
        # stylesheet rules for that
        if len(self.cw_rset) > 1:
            table.append_row([0] * nb_cols, 'Total')
            nb_rows = len(table.row_names)
            for i in range(nb_cols):
                stylesheet.add_colsum_rule((nb_rows-1, i), i, 0, nb_rows-2)
            table.apply_stylesheet(stylesheet)
        # render the table
        w(u'<table class="stats" cellpadding="5">')
        w(u'<tr>')
        for col in [''] + table.col_names:
            url = self._cw.build_url(vid='stats', sort_col=col,
                                 __force_display=1,
                                 rql=self.cw_rset.printable_rql())
            self.w(u'<th><a href="%s">%s</a></th>\n' % (xml_escape(url), col))
        self.w(u'</tr>')
        for row_name, row, index in zip(table.row_names, table.data,
                                        xrange(len(table.data))):
            if index % 2 == 0:
                w(u'<tr class="alt0">')
            else:
                w(u'<tr class="alt1">')
            if index == len(table.data) - 1:
                w(u'<td>%s</td>' % row_name)
            else:
                url = self._cw.build_url('project/%s' % self._cw.url_quote(row_name))
                self.w(u'<td><a href="%s">%s</a></td>' % (xml_escape(url), row_name))
            for cell_data in row:
                w(u'<td>%s</td>' % cell_data)
            w(u'</tr>')
        w(u'</table>')


class SubscribeToReleasesComponent(component.EntityVComponent):
    """link to subscribe to rss feed for published versions of project
    """
    __regid__ = 'projectreleasesubscriberss'
    __select__ = (component.EntityVComponent.__select__ &
                  implements('Project'))
    context = 'ctxtoolbar'

    def cell_call(self, row, col, view=None):
        entity = self.cw_rset.get_entity(row, col)
        label = self._cw._(u'Subscribe to project releases')
        logo = u'<img src="%s" alt="%s"/>' % (
            self._cw.external_resource('RSS_LOGO_16'), label)
        rql = 'Any V, VN ORDERBY VN DESC WHERE V version_of P, P eid %s, ' \
              'V in_state S, S name "published", V num VN' % entity.eid
        # XXX <project>/versions/rss ?
        url = self._cw.build_url('view', vid='rss', rql=rql)
        self.w(u'<a href="%s" title="%s" class="toolbarButton">%s</a>' % (
            xml_escape(url), label, logo))


