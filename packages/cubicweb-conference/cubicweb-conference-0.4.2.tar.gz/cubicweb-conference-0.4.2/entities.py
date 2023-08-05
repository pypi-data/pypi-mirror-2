"""this contains the template-specific entities' classes"""

__docformat__ = "restructuredtext en"

from logilab.common.date import todate

from cubicweb.mixins import TreeMixIn
from cubicweb.entities import AnyEntity
from cubicweb.interfaces import ITree, ICalendarable

class Conference(TreeMixIn, AnyEntity):
    """customized class for Conference entities"""
    __regid__ = 'Conference'
    __implements__ = AnyEntity.__implements__ + (ITree,)

    tree_attribute = 'in_conf'

    def children(self, entities=True):
        """
        Return children entities.
        Overriden to get only Track entities.
        """
        return self.different_type_children(entities)

    def dates(self):
        return (self.start_on, self.end_on)

    def breadcrumbs(self, view=None, recurs=False):
        return [(self.absolute_url(), self.dc_title()),]

    def get_talks_by_track(self, track):
        rql = 'Any T WHERE T in_track TR, TR eid %(tr)s'
        return self._cw.execute(rql, {'tr': track.eid})

    def has_talk(self, day, track):
        for talk in self.get_talks_by_track(track).entities():
            if talk.is_on_day(day):
                return True
        return False

class Track(TreeMixIn, AnyEntity):
    """customized class for Track entities"""
    __regid__ = 'Track'
    __implements__ = AnyEntity.__implements__ + (ITree,)

    tree_attribute = 'in_track'

    def children(self, entities=True):
        """
        Return children entities.
        Overriden to get only Talk entities.
        """
        return self.different_type_children(entities)

    def dates(self):
        return

    def breadcrumbs(self, view=None, recurs=False):
        try:
            breadcrumbs = self.in_conf[0].breadcrumbs(view, True)
        except IndexError:
            breadcrumbs = []
        breadcrumbs += [(self.absolute_url(), self.dc_title()), ]
        return breadcrumbs

class Talk(AnyEntity):
    __regid__ = 'Talk'
    __implements__ = AnyEntity.__implements__ + (ICalendarable,)

    def breadcrumbs(self, view=None, recurs=False):
        try:
            breadcrumbs = self.in_track[0].breadcrumbs(view, True)
        except IndexError:
            breadcrumbs = []
        breadcrumbs += [(self.absolute_url(), self.dc_title()), ]
        return breadcrumbs

    @property
    def start(self):
        return self.start_time

    @property
    def stop(self):
        return self.end_time

    def is_on_day(self, day):
        date = todate(day)
        if self.start_time:
            talk_date = todate(self.start_time)
            return date == talk_date
        else:
            return False
