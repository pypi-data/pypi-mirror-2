_ = unicode

from cubicweb.web.views import startup

# index view
class IndexView(startup.IndexView):
    __regid__ = 'index'
    title = _('Index')
    add_etype_links = ('Conference',)
    upcoming_conferences = ('Any C WHERE C is Conference, C end_on >= now')
    past_conferences = ('Any C WHERE C is Conference, C end_on < now')

    def call(self):
        # upcoming conferences
        rset = self._cw.execute(self.upcoming_conferences)
        if rset:
            self.w(u'<h1>%s</h1>' % self._cw._(u'Upcoming conferences'))
            self.wview('confsummary', rset, 'null')
        else:
            self.w(self._cw._(u'No conference planned for now...'))

        # past conferences
        rset = self._cw.execute(self.past_conferences)
        if rset:
            self.w(u'<h1>%s</h1>' % self._cw._(u'Past conferences'))
            self.wview('confsummary', rset, 'null')

def registration_callback(vreg):
    vreg.register_all(globals().values(), __name__, (IndexView,))
    vreg.register_and_replace(IndexView, startup.IndexView)
