"""tracker extproject and project entity classes

:organization: Logilab
:copyright: 2006-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"

from warnings import warn

from logilab.common.decorators import cached

from cubicweb.interfaces import ITree
from cubicweb.mixins import TreeMixIn
from cubicweb.entities import AnyEntity, fetch_config

from cubes.tracker.entities import fixed_orderby_rql

class Project(TreeMixIn, AnyEntity):
    __regid__ = 'Project'
    __implements__ = AnyEntity.__implements__ + (ITree,)
    __permissions__ = ('developer', 'client')
    fetch_attrs, fetch_order = fetch_config(('name', 'description', 'description_format',
                                             'summary'))

    TICKET_DEFAULT_STATE_RESTR = 'S name IN ("created","identified","released","scheduled")'

    tree_attribute = 'subproject_of'
    parent_target = 'subject'
    children_target = 'object'

    def dc_title(self):
        return self.name

    def dc_long_title(self):
        if self.summary:
            return u'%s (%s)' % (self.name, self.summary)
        return self.name

    @property
    def project(self):
        """project item interface"""
        return self

    def latest_version(self, states=('published',), reverse=None):
        """returns the latest version(s) for the project in one of the given
        states.

        when no states specified, returns the latest published version.
        """
        order = 'DESC'
        if reverse is not None:
            warn('reverse argument is deprecated',
                 DeprecationWarning, stacklevel=1)
            if reverse:
                order = 'ASC'
        rset = self.versions_in_state(states, order, True)
        if rset:
            return rset.get_entity(0, 0)
        return None

    @cached
    def versions_in_state(self, states, order='ASC', limit=False):
        """returns version(s) for the project in one of the given states, sorted
        by version number.

        If limit is true, limit result to one version.
        If reverse, versions are returned from the smallest to the greatest.

        NOTE: /!\ DO NOT CALL this method with named parameter: `cached`
              implementation doesn't support it yet
        """
        if limit:
            order += ' LIMIT 1'
        rql = 'Any V,N ORDERBY version_sort_value(N) %s ' \
              'WHERE V num N, V in_state S, S name IN (%s), ' \
              'V version_of P, P eid %%(p)s' % (order, ','.join(repr(s) for s in states))
        return self._cw.execute(rql, {'p': self.eid})

    # number of columns to display
    tickets_rql_nb_displayed_cols = 7
    sort_defs = (('in_state', 'S'), ('num', 'VN'), ('priority', 'PR'))
    def tickets_rql(self, limit=None):
        return ('Any B, NOW - CD, NOW - BMD, U,PR,S,V,BD,VN,P,BT,CD,BMD,UL '
                'GROUPBY B,CD,PR,S,V,U,VN,BD,P,BT,BMD,UL '
                '%s %s '
                'WHERE B priority PR, B in_state S, B creation_date CD, '
                'B description BD, '
                'B title BT, B modification_date BMD, '
                'B done_in V?, V num VN, '
                'B created_by U?, U login UL, B concerns P, P eid %s'
               ) % (fixed_orderby_rql(self.sort_defs),
                    limit and ' LIMIT %r' % limit or '',
                    self.eid)
        return rql

    def active_tickets_rql(self):
        return '%s, %s' % (self.tickets_rql(), self.TICKET_DEFAULT_STATE_RESTR)
