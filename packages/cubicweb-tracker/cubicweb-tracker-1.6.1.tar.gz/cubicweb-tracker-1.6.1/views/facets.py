from cubicweb.selectors import is_instance
from cubicweb.web.facet import RelationFacet, AttributeFacet

class TicketConcernsFacet(RelationFacet):
    __regid__ = 'concerns-facet'
    __select__ = RelationFacet.__select__ & is_instance('Ticket')
    rtype = 'concerns'
    target_attr = 'name'


class TicketDoneInFacet(RelationFacet):
    __regid__ = 'done_in-facet'
    __select__ = RelationFacet.__select__ & is_instance('Ticket')
    rtype = 'done_in'
    target_attr = 'num'
    sortfunc = 'VERSION_SORT_VALUE'
    sortasc = False


class TicketPriorityFacet(AttributeFacet):
    __regid__ = 'priority-facet'
    __select__ = AttributeFacet.__select__ & is_instance('Ticket')
    rtype = 'priority'
    sortfunc = 'PRIORITY_SORT_VALUE'


class TicketTypeFacet(AttributeFacet):
    __regid__ = 'type-facet'
    __select__ = AttributeFacet.__select__ & is_instance('Ticket')
    rtype = 'type'
