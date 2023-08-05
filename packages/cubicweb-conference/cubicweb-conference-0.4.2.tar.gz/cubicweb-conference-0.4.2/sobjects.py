"""this contains the server-side objects"""
import datetime

from cubicweb.selectors import implements
from cubicweb.server.hook import Hook, match_rtype
from cubicweb.server.hook import match_rtype
from cubicweb.sobjects.notification import (RecipientsFinder,
                                            NotificationView,
                                            StatusChangeMixIn)

class AddTalkLeadHook(Hook):
    __regid__ = 'add-talk-lead-hook'
    __select__ = implements('Talk')
    events = ('after_add_entity',)
    def __call__(self):
        if not self._cw.is_internal_session:
            asession = self._cw
            asession.execute('SET U leads X WHERE X eid %(x)s, U eid %(u)s, NOT U attend X',
                             {'x': self.entity.eid, 'u': self._cw.user.eid}, 'x')

class LeadsHook(Hook):
    """
    Create relation attend on CWUser who leads a Talk:
    U leads T => U attend T
    """
    __regid__ = 'lead-entails-attend-hook'
    __select__ = Hook.__select__ & match_rtype('leads')
    events = ('after_add_relation',)

    def __call__(self):
        if not self._cw.is_internal_session:
            asession = self._cw
            asession.execute('SET U attend X WHERE X eid %(x)s, U eid %(u)s, NOT U attend X',
                             {'x': self.eidto, 'u': self.eidfrom}, 'x')

class InTrackHook(Hook):
    """
    When a Talk is added to a Track, automatically add it to the Conference:
    T in_track TR => T in_conf C
    """
    __regid__ = 'in_track-entails-in_conf-hook'
    __select__ = Hook.__select__ & match_rtype('in_track')
    events = ('before_add_relation',)

    def __call__(self):
        if not self._cw.is_internal_session:
            asession = self._cw
            rql = 'Any C WHERE TR in_conf C, TR eid %(tr)s'
            conf = asession.execute(rql, {'tr': self.eidto})
            asession.execute('SET T in_conf C WHERE T eid %(t)s, C eid %(c)s, NOT T in_conf C',
                             {'t': self.eidfrom, 'c': conf[0][0]})

class InConfHook(Hook):
    """
    Remove already existing relation X in_conf C when trying to add a new
    relation X in_conf C
    """
    __regid__ = 'switch-in_conf-hook'
    __select__ = Hook.__select__ & match_rtype('in_conf')
    events = ('before_add_relation',)

    def __call__(self):
         if not self._cw.is_internal_session:
            asession = self._cw
            rql = 'Any C WHERE X in_conf C, X eid %(x)s'
            conf = asession.execute(rql, {'x': self.eidfrom})
            if conf:
                asession.execute('DELETE X in_conf C WHERE X eid %(x)s, C eid %(c)s',
                                 {'x': self.eidfrom, 'c': conf[0][0]})


#-------------------
# Email notification
#-------------------

class TalkNotificationView(NotificationView):
    __select__ = NotificationView.__select__ & implements('Talk',)

    def context(self, **kwargs):
        context = super(TalkNotificationView, self).context(**kwargs)
        entity = self.cw_rset.complete_entity(0,0)
        context.update({'talk_name': entity.title,
                        'date': datetime.date.today().isoformat(),
                        'firstname': entity.reverse_leads[0].firstname,
                        'lastname': entity.reverse_leads[0].surname,
                        'conference': entity.in_track[0].in_conf[0].title})
        return context

    def recipients(self):
        recipients = []
        for finderid in self.recipients_finder:
            finder = self._cw.vreg['components'].select(finderid, self._cw,
                                                        rset= self.cw_rset)
            recipients += finder.recipients()
        return recipients

class TalkAddRecipientsFinder(RecipientsFinder):
    __select__ = RecipientsFinder.__select__ & implements('Talk',)
    __regid__ = 'manager_finder'

    @property
    def user_rql(self):
        return ('Any U, E, A WHERE U is CWUser, U in_group N, N name "managers", U primary_email E, E address A')

class TalkUpdateRecipientsFinder(RecipientsFinder):
    __select__ = RecipientsFinder.__select__ & implements('Talk',)
    __regid__ = 'interested_by_finder'

    @property
    def user_rql(self):
        return ('Any U, E, A WHERE X eid %(eid)s, (U reviews X) OR (U leads X), U primary_email E, E address A' %
                {'eid':  self.cw_rset[0][0]})

class TalkAdd(TalkNotificationView):
    """  Send an email to managers after a talk creation
    """
    __regid__ = 'notif_after_add_entity'

    recipients_finder = ('manager_finder',)

    content = _(u""
                u"Dear %(firstname)s %(lastname)s,\n"
                u"\n"
                u"The talk '%(talk_name)s' was added on %(date)s.\n"
                u"\n"
                u"Sincerely,\n"
                u"\n"
                u"--\n"
                u"The %(conference)s organizing committee.\n")

    def subject(self):
        entity = self.cw_rset.get_entity(0,0)
        return self._cw._('[%s] a talk was added.') % entity.in_track[0].in_conf[0].title

class TalkUpdate(TalkNotificationView):
    __regid__ = 'notif_after_update_entity'

    recipients_finder = ('manager_finder', 'interested_by_finder',)

    content = _(u""
                u"Dear %(firstname)s %(lastname)s,\n"
                u"\n"
                u"The talk '%(talk_name)s' was modified on %(date)s.\n"
                u"\n"
                u"Sincerely,\n"
                u"\n"
                u"--\n"
                u"The %(conference)s organizing committee.\n")

    def subject(self):
        entity = self.cw_rset.get_entity(0,0)
        return self._cw._('[%s] a talk was added.') % entity.in_track[0].in_conf[0].title

class TalkStatusUpdate(StatusChangeMixIn, TalkNotificationView):
    """
    """

    recipients_finder = ('manager_finder', 'interested_by_finder')

    content = _(u""
                u"Dear user,\n\n"
                u"The '%(title)s' status was updated from '%(previous_state)s' to '%(current_state)s'.\n\n"
                u"Sincerely,\n"
                u"\n"
                u"--\n"
                u"The conference organizing committee.\n")

    def subject(self):
        entity = self.cw_rset.get_entity(0,0)
        return _(u'[%s] talk status was updated' % entity.in_track[0].in_conf[0].title)


