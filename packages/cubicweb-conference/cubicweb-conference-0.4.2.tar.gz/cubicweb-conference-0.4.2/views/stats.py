from logilab.mtconverter import xml_escape
from cubicweb.selectors import nonempty_rset
from cubicweb.view import View, EntityView

class StatTalkView(EntityView):
    __regid__ = 'stat_talk_view'
    __select__ = nonempty_rset()

    def call(self, **kwargs):
        entity = self.cw_rset.get_entity(0,0)
        rql = 'Any T, COUNT(A) GROUPBY T WHERE T is Talk, A attend T, T in_conf C, C eid %(eid)s'
        rset = self._cw.execute(rql, {'eid': entity.eid})
        self.wview('table', rset)

class StatReviewView(EntityView):
    __regid__ = 'stat_review_view'
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(0,0)
        rql = 'Any S, COUNT(T) GROUPBY S WHERE T is Talk, T in_state S, T in_conf C, C eid %(eid)s'
        rset = self._cw.execute(rql, {'eid': entity.eid})
        self.wview('table', rset, 'null')
        rset = self._cw.execute('Any T WHERE T is Talk, T in_state S, S name "submitted"')
        if rset:
            self.w(u'<div id="statreview">')
            self.w(u'<p>%s</p>' % self._cw._(u'Please, assign a reviewer to :'))
            self.w(u'<ul>')
            for talk in rset.entities():
                transition = talk.possible_transitions().next()
                self.w('<li><a href="%s">%s</a></li>' %
                       (xml_escape(talk.absolute_url(vid='statuschange',
                                                     treid=transition.eid)),
                       xml_escape(talk.title)))
            self.w(u'</ul></div>')
