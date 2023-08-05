# primary views
_ = unicode

from cubicweb.web import uicfg
from datetime import timedelta, date
from logilab.mtconverter import xml_escape

from cubicweb.selectors import implements, rql_condition, match_user_groups
from cubicweb.view import EntityView
from cubicweb.web.views import primary, tabs

class ConfTrackListPrimaryView(primary.PrimaryView):
    __select__ = implements('Track')

    def render_entity_title(self, entity):
        title = entity.dc_title()
        if entity.dates():
            dates = entity.dates()
            dates_html = u'<span class="dates">%s to %s</span>' % \
                        (xml_escape(self._cw.format_date(dates[0])),
                         xml_escape(self._cw.format_date(dates[1])))
            title += u' - %s' % dates_html
        self.w(u'<h1><span class="etype">%s</span> %s</h1>'
               % (entity.dc_type().capitalize(), title))

    def render_entity_attributes(self, entity):
        if entity.description:
            self.w(u'<div>%s</div>' % entity.dc_description('text/html'))

    def render_entity_relations(self, entity):
        if entity.children(entities=False):
            if entity.in_conf[0].end_on > date.today():
                text = self._cw._(u'The following talks will be presented:')
            else:
                text = self._cw._(u'The following talks were presented:')
            self.w(u'<h4>%s</h4>' % text)
            self.wview('list', entity.children(entities=False))


class ConferencePrimaryView(tabs.TabbedPrimaryView):
    __select__ = implements('Conference')
    tabs = [_('confinfo'), _('talkslist'), _('talksschedule'),
            _('userconfschedule')]
    default_tab = 'confinfo'

    def render_entity_title(self, entity):
        title = entity.dc_title()
        if entity.dates():
            dates = entity.dates()
            dates_html = u'<span class="dates">%s to %s</span>' % \
                        (xml_escape(self._cw.format_date(dates[0])),
                         xml_escape(self._cw.format_date(dates[1])))
            title += u' - %s' % dates_html
        self.w(u'<div id="conftitle"><h1><span class="etype">%s</span> %s</h1></div>'
               % (entity.dc_type().capitalize(), title))


class TalkPrimaryView(primary.PrimaryView):
    __select__ = implements('Talk',)

    def render_entity_title(self, entity):
        self.w(u'<h1><span class="etype">%s</span> %s</h1>'
               % (entity.dc_type().capitalize(), entity.dc_title()))
        self.w(u'<table class="talk"><tr><td>')
        self.render_talk_info(entity)
        self.w(u'</td><td>')
        self.w(u'</td></tr></table>')

    def render_talk_info(self, entity):
        self.w(u'<div>')
        if entity.reverse_leads:
            speaker = entity.reverse_leads[0]
            self.w(u'<span class="speaker">%s <a href="%s">%s</a></span>' % (
                    self._cw._(u'Presented by'),
                    xml_escape(speaker.absolute_url()),
                    xml_escape(speaker.name())))
        self.w(u' %s <span>' % self._cw._(u'in'))
        self.wview('csv', entity.related('in_track'), 'null')
        self.w(u'</span>')
        self.render_talk_time_place(entity)
        self.w(u'</div>')

    def render_talk_time_place(self, entity):
        _ = self._cw._
        if entity.start_time or entity.end_time:
            self.w(u'<span class="talktime">')
            if entity.start_time and entity.end_time:
                self.w(_(u"on %(sdate)s from %(stime)s to %(etime)s") %
                       ({'sdate': self._cw.format_date(entity.start_time),
                         'stime': self._cw.format_time(entity.start_time),
                         'etime': self._cw.format_time(entity.end_time)}))
            self.w(u'</span>')
        if entity.location:
            self.w(u'<span> %s %s</span>' % (_(u'in room'), entity.location))

    def render_entity_attributes(self, entity):
        if entity.description:
            self.w(u'<h5>%s</h5>' % _(u'Abstract'))
            self.w(u'<div>%s</div>' % entity.dc_description('text/html'))

class ConferenceSummaryView(EntityView):
    __select__ = implements('Conference',)
    __regid__ = 'confsummary'

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        if entity.dates():
            dates = entity.dates()
            dates_html = (u'<span class="dates">%s to %s</span>' % (
                    xml_escape(self._cw.format_date(dates[0])),
                    xml_escape(self._cw.format_date(dates[1]))))
        self.w(u'<h2><a href="%s">' % xml_escape(entity.absolute_url()))
        self.w(xml_escape(self._cw.view('text', self.cw_rset, row=row, col=col)))
        self.w(u' - %s' % dates_html)
        self.w(u'</a></h2>')

class ConferenceInfoView(EntityView):
    __select__ = implements('Conference')
    __regid__ = 'confinfo'

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        _ = self._cw._
        if entity.description:
            self.w(u'<div>%s</div>' % entity.dc_description('text/html'))
        rql = ('Any TR, TD, MIN(ST), MAX(ET), COUNT(T) GROUPBY TR, '
              'TD WHERE T in_track TR, T start_time ST, T end_time ET, '
              'TR description TD, TR in_conf C, C eid %(c)s')
        rset = self._cw.execute(rql, {'c':entity.eid})
        if rset:
            if entity.end_on > date.today():
                text = _(u'The conference will be divided into the following tracks:')
            else:
                text = _(u'The conference was divided into the following tracks:')
            self.w(u'<div>%s</div>' % text)
            headers = (_(u'Track title'), _(u'Description'), _(u'First talk'),
                       _(u'Last talk'), _(u'Total talks'))
            self.wview('table', rset, headers=headers, displaycols=range(0,5))
        else:
            self.w(u'<div>%s</div>' % _(u'No track yet in this conference.'))

class DcTitleView(EntityView):
    __regid__ = 'dc_long_title'

    def cell_call(self, row, col):
        self.w(self.cw_rset.get_entity(row,col).dc_long_title())

class UserConfSchedule(EntityView):
    __select__ = implements('Conference') & ~ match_user_groups('guests',)
    __regid__ = 'userconfschedule'

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        _ = self._cw._
        rql = ('Any T, ST, L ORDERBY ST WHERE T is Talk, T start_time ST, '
               'T location L, T in_conf C, C eid %(eid)s, U attend T, '
               'U login %(login)s')
        rset = self._cw.execute(rql, {'eid': entity.eid,
                                      'login': self._cw.user.login})
        if rset:
            self.w(u'<p>%s</p>' % _(u'You are registered for these talks:'))
            self.wview('table', rset, headers=(_(u'Talk title'),
                                               _(u'Date'), _(u'Location')))
        else:
            self.w(u'<p>%s</p>' % _(
                    u'Do you plan to attend a specific talk ? Please click on '
                    u'the "I plan to attend" button positionned at the top '
                    u'right of each talk summary.'))

class ConferenceTalksList(EntityView):
    __select__ = implements('Conference')
    __regid__ = 'talkslist'

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        _ = self._cw._
        rql = ('Any T, U, ST, L, TR WHERE T location L, T start_time ST, '
               'U leads T, T in_conf C, T in_track TR, C eid %(c)s')
        rset = self._cw.execute(rql, {'c': entity.eid})
        if rset:
            headers = (_(u'Talk title'), _(u'Speaker'), _(u'Date'),
                       _(u'Location'), _(u'Track'))
            self.wview('table', rset, headers=headers, cellvids={1:'dc_long_title'})
        else:
            self.w(u'<div>%s</div>' % _(u'No talk yet in this conference'))

class ConferenceTalksSchedule(EntityView):
    __select__ = implements('Conference') & rql_condition('T in_conf X')
    __regid__ = 'talksschedule'

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        day = entity.start_on
        while day <= entity.end_on:
            tracks_rql = 'Any TR WHERE TR in_conf C, TR is Track, C eid %(c)s'
            tracks = self._cw.execute(tracks_rql, {'c': entity.eid}).entities()
            self.w(u'<table style="width:100%">')
            self.w(u'<tr>')
            for track in tracks:
                if entity.has_talk(day, track):
                    self.w(u'<td>')
                    self.wview('onedaycal', entity.get_talks_by_track(track),
                               day=day, title=track.title)
                    self.w(u'</td>')

            day += timedelta(1)
            self.w(u'</tr></table>')

class CWUserPrimaryView(primary.PrimaryView):
    __select__ = implements('CWUser') & match_user_groups('guests',)

    def render_entity_title(self, entity):
        title = xml_escape(entity.firstname+' '+entity.surname)
        if title:
            self.w(u'<h1>%s</h1>' % title)

    def render_entity_attributes(self, entity):
        if entity.representing:
            self.w("%s %s" % (self._cw._(u'Representing'), entity.representing))

class AdminView(EntityView):
    __select__ = (implements('Conference') & match_user_groups('managers',))
    __regid__ = 'adminview'

    def cell_call(self, row, col):
        self.w(u'<div id="stat">')
        self.w(u'<p><a href="javascript: toggleVisibility(\'stat_attend\')">%s</a></p>'
               % self._cw._(u'Talk state details'))
        self.w(u'<div id="stat_attend">')
        self.wview('stat_review_view', self.cw_rset)
        self.w(u'</div>')
        self.w(u'<p><a href="javascript: toggleVisibility(\'stat_review\')">%s</a></p>'
               % self._cw._(u'Number of participant by Talk'))
        self.w(u'<div id="stat_review">')
        self.wview('stat_talk_view', self.cw_rset)
        self.w(u'</div>')
        self.w(u'</div>')

