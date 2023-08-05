"""tracker server side objects, mainly notification stuff

:organization: Logilab
:copyright: 2006-2009 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"


from logilab.common.textutils import normalize_text

from cubicweb.selectors import implements, score_entity
from cubicweb.mail import SkipEmail
from cubicweb.sobjects.notification import (StatusChangeMixIn, NotificationView,
                                            EntityUpdatedNotificationView)

class TrackerEmailView(NotificationView):

    def subject(self):
        entity = self.cw_rset.get_entity(0,0)
        return '[%s] %s' % (entity.project.name, self._subject(entity))

    def _subject(self, entity):
        return '%s %s (%s)' % (entity.dc_type(), self.message, entity.dc_title())


class TicketPropertiesChangeView(TrackerEmailView, EntityUpdatedNotificationView):
    no_detailed_change_attrs =  ('description', 'description_format')
    __select__ = implements('Ticket')

    content = _("""
Ticket properties have been updated by %(user)s:
%(changes)s

url: %(url)s
""")

    def _subject(self, entity):
        return self._cw._(u'%(etype)s "%(title)s" updated') % {
            'etype': entity.dc_type(), 'title': entity.dc_title()}


class VersionChangedView(TicketPropertiesChangeView):
    __select__ = implements('Version')
    content = _("""
Version dates have been updated by %(user)s:
%(changes)s

url: %(url)s
""")


class VersionStatusChangeView(StatusChangeMixIn, TrackerEmailView):
    __select__ = implements('Version')

    def _subject(self, entity):
        return self._cw._(u'version %(num)s is now in state "%(state)s"') % {
            'num': entity.num,
            'state': self._cw.__(self._kwargs['current_state'])}


class VersionPublishedView(VersionStatusChangeView):
    __select__ = (VersionStatusChangeView.__select__
                  # use latest trinfo since we're not yet linked to the new
                  # state at this point
                  & score_entity(lambda x: x.latest_trinfo().new_state.name in x.PUBLISHED_STATES)
                  )

    content = _("""
Bugs fixed in this release:
\t%(bugslist)s

Enhancements implemented in this release:
\t%(enhancementslist)s

Tasks done in this release:
\t%(taskslist)s

url: %(url)s
""")

    def context(self, **kwargs):
        context = super(VersionPublishedView, self).context(**kwargs)
        entity = self.cw_rset.get_entity(0, 0)
        bugs = ['- '+t.dc_title() for t in entity.reverse_done_in if t.type == 'bug']
        enhancements = ['- '+t.dc_title() for t in entity.reverse_done_in if t.type == 'enhancement']
        tasks = ['- '+t.dc_title() for t in entity.reverse_done_in if t.type == 'task']
        context['bugslist'] = '\n\t'.join(bugs)
        context['enhancementslist'] = '\n\t'.join(enhancements)
        context['taskslist'] = '\n\t'.join(tasks)
        return context


class TicketStatusChangeView(StatusChangeMixIn, TrackerEmailView):
    __select__ = implements('Ticket')

    def _subject(self, entity):
        return self._cw._(u'%(etype)s "%(title)s" is now in state "%(state)s"') % {
            'etype': entity.dc_type(), 'title': entity.dc_title(),
            'state': self._cw.__(self._kwargs['current_state'])}


class ProjectAddedView(TrackerEmailView):
    __regid__ = 'notif_after_add_entity'
    __select__ = implements('Project')

    section_attrs = ['summary', 'description']
    content = _("""
A new project was created by %(user)s: #%(eid)s - %(pname)s

%(pcontent)s

URL
---
%(url)s
""")

    def context(self, **kwargs):
        context = super(ProjectAddedView, self).context(**kwargs)
        entity = self.cw_rset.get_entity(0, 0)
        sections = []
        for attr in self.section_attrs:
            val = entity.printable_value(attr, format='text/plain')
            if val:
                sect = self.format_section(self._cw._(attr).capitalize(), val)
                sections.append(sect)
        context['pcontent'] = '\n'.join(sections)
        context['pname'] = entity.name
        return context

    def subject(self):
        return u'[%s] %s: %s' % (
            self._cw.vreg.config.appid, self._cw.__('New Project'), self.cw_rset.get_entity(0,0).name)


class TicketSubmittedView(TrackerEmailView):
    __regid__ = 'notif_after_add_relation_concerns'
    __select__ = implements('Ticket')
    content = _("""
New %(etype)s for project %(pname)s :

#%(eid)s - %(title)s
====================
%(mainsection)s

description
-----------
%(description)s

submitter
---------
%(user)s

URL
---
%(url)s
(project URL: %(purl)s)
""")
    field_attrs = ['type', 'priority']

    def context(self, **kwargs):
        ctx = super(TicketSubmittedView, self).context(**kwargs)
        entity = self.cw_rset.get_entity(0, 0)
        sect = []
        for attr in self.field_attrs:
            sect.append(self.format_field(attr, entity.printable_value(attr)))
        ctx['mainsection'] = '\n'.join(sect)
        description = entity.printable_value('description', format='text/plain')
        description = normalize_text(description, 80)
        ctx['description'] = description
        ctx['pname'] = entity.project.name
        ctx['purl'] = entity.project.absolute_url()
        return ctx

    def _subject(self, entity):
        return '%s %s' % (self._cw.__('New %s' % entity.e_schema),
                          entity.dc_title())
