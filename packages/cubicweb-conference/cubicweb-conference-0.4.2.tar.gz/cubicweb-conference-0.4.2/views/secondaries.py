# custom application views
_ = unicode

from logilab.mtconverter import xml_escape
from logilab.common.date import date_range, todate, todatetime

from cubicweb.interfaces import ICalendarable
from cubicweb.selectors import implements, has_related_entities, match_user_groups
from cubicweb.view import EntityView
from cubicweb.web import box
from cubicweb.web.component import Component, EntityVComponent
from cubicweb.web.views import calendar

# boxes
class AttachmentsDownloadBox(box.EntityBoxTemplate):
    """
    A box containing all downloadable attachments of a Talk.
    """
    __regid__ = 'attachments_downloads_box'
    __select__ = box.EntityBoxTemplate.__select__ & implements('Talk') \
        & has_related_entities('has_attachments', 'subject')

    def cell_call(self, row, col, **kwargs):
        entity = self.cw_rset.get_entity(row,col)
        _cw = self._cw
        self.w(u'<div class="sideBox">')
        title = _cw._('Attachments')
        self.w(u'<div class="sideBoxTitle downloadBoxTitle"><span>%s</span></div>'
            % xml_escape(title))
        self.w(u'<div class="sideBox downloadBox"><div class="sideBoxBody">')
        for attachment in entity.has_attachments:
            self.w(u'<div><img src="%s" alt="%s"/><a href="%s">%s</a>'
                   % (_cw.external_resource('DOWNLOAD_ICON'),
                      _cw._('download icon'),
                      xml_escape(attachment.download_url()),
                      xml_escape(attachment.dc_title())))
            self.w(u'</div>')
        self.w(u'</div>\n</div>\n</div>\n')

# components
class AttendanceComponent(EntityVComponent):
    __regid__ = 'attendance'
    __select__ = EntityVComponent.__select__ & implements('Talk')
    context = 'ctxtoolbar'
    htmlclass = 'mainRelated'

    def cell_call(self, row, col, view=None):
        user = self._cw.user
        # skip this for anonymous user
        if user.login == self._cw.vreg.config['anonymous-user']:
            return
        _ = self._cw._
        eid = self.cw_rset[0][0]
        rset = self._cw.execute('Any X WHERE U attend X, U eid %(u)s, X eid %(x)s',
                                {'u': user.eid, 'x': eid}, 'x')
        self.w(u'<div class="%s" id="%s">' % (self.__regid__, self.div_id()))
        if not rset.rowcount:
            # user is not attending the talk
            rql = 'SET U attend X WHERE U eid %(u)s, X eid %(x)s'
            title = _('click here to attend this %s' % self.cw_rset.get_entity(0,0).dc_type())
            msg = _('you are now registered to attend this talk')
            label, label_id= (_('I do not plan to attend'), 'unattend')
        else:
            # user is already attending this talk
            rql = 'DELETE U attend X WHERE U eid %(u)s, X eid %(x)s'
            title = _('click here if you don\'t want to attend this %s anymore'
                      % self.cw_rset.get_entity(0,0).dc_type())
            msg = _('you are not anymore registered to attend this talk')
            label, label_id= (_('I plan to attend'), 'attend')
        url = self._cw.user_rql_callback((rql, {'u': user.eid, 'x': eid}, 'x'),
                                         msg=msg).lstrip('javascript:')
        nb_person_rset = self._cw.execute('Any COUNT(U) WHERE U attend X, X eid %s' % eid)[0][0]
        self.w(u'<div onclick="%s" class="attendbutton" id="%s">'
               u'<div id="attendinfo">%s</div><div>(%s %s)</div></div>'
               % (xml_escape(url), label_id, label, nb_person_rset, _('people were registered')))
        self.w(u'</div>')

class AdminViewTalkComponent(EntityVComponent):
    __regid__ = 'adminviewcomponent'
    __select__ = (EntityVComponent.__select__ &
                  implements('Talk') &
                  match_user_groups('managers'))
    context = 'ctxtoolbar'
    order = 0

    def cell_call(self, row, col, **kwargs):
        entity = self.cw_rset.get_entity(row, col).in_conf[0]
        comp = self._cw.vreg['contentnavigation'].select('adminviewcomponent',
                                                         self._cw,
                                                         rset=entity.as_rset())
        comp.render(self.w)

class AdminViewComponent(EntityVComponent):
    __regid__ = 'adminviewcomponent'
    __select__ = (EntityVComponent.__select__ &
                  implements('Conference') &
                  match_user_groups('managers'))
    context = 'ctxtoolbar'
    order = 0

    def cell_call(self, row, col, **kwargs):
        entity = self.cw_rset.get_entity(row, col)
        iconurl = xml_escape(self._cw.build_url('data/stat.png'))
        url = xml_escape(entity.absolute_url(vid='adminview'))
        label = self._cw._('View statistics')
        self.w(u'<a href="%s" title="%s" class="toolbarButton"><img src="%s" alt="%s"/></a>' %
               (xml_escape(url), label, iconurl, label))

class TalkCalendarItem(calendar.CalendarItemView):
    __select__ = implements('Talk')

    def cell_call(self, row, col, dates=False):
        task = self.cw_rset.complete_entity(row)
        task.view('oneline', w=self.w)
        if task.location:
            self.w(u'<div>[%s %s]</div>' % (self._cw._(u'room'), task.location))

# one day calendar view for day of conference
class OneDayCal(EntityView):
    """Render a one day calendar view"""
    __regid__ = 'onedaycal'
    __select__ = implements(ICalendarable)
    need_navigation = False
    title = _('one day')

    def call(self, day, title=''):
        self._cw.add_js( ('cubicweb.ajax.js', 'cubicweb.calendar.js') )
        self._cw.add_css('cubicweb.calendar.css')

        task_colors = {}   # remember a color assigned to a task
        # colors here are class names defined in cubicweb.css
        colors = [ "col%x" % i for i in range(12) ]
        next_color_index = 0
        done_tasks = []
        task_descrs = []
        for row in xrange(self.cw_rset.rowcount):
            task = self.cw_rset.get_entity(row, 0)
            if task in done_tasks:
                continue
            done_tasks.append(task)
            the_dates = []
            tstart = task.start
            tstop = task.stop
            if tstart:
                tstart = todate(tstart)
                if tstart != day:
                    continue
                the_dates = [tstart]
            if tstop:
                tstop = todate(tstop)
                if tstop != day:
                    continue
                the_dates = [tstop]
            if tstart and tstop:
                the_dates = date_range(max(tstart, day),
                                       min(tstop, day))
            if not the_dates:
                continue

            if task not in task_colors:
                task_colors[task] = colors[next_color_index]
                next_color_index = (next_color_index+1) % len(colors)

            # add task description for the given day
            task_descr = calendar._TaskEntry(task, task_colors[task])
            task_descrs.append(task_descr)

        self.w(u'<div id="oneweekcalid">')
        # build schedule for the given day
        self._build_schedule(day, task_descrs, title)

        self.w(u'</div>')
        self.w(u'<div id="coord"></div>')
        self.w(u'<div id="debug">&#160;</div>')

    def _build_schedule(self, date, task_descrs, title):
        if 'year' in self._cw.form:
            year = int(self._cw.form['year'])
        else:
            year = date.year
        if 'week' in self._cw.form:
            week = int(self._cw.form['week'])
        else:
            week = date.isocalendar()[1]
        self.w(u'<table class="omcalendar" id="week">')
        self.w(u'<tr><th class="transparent"></th></tr>')

        # output header
        self.w(u'<tr>')
        self.w(u'<th class="transparent"></th>') # column for hours
        _today = date.today()
        wdate = date
        if wdate.isocalendar() == _today.isocalendar():
            if title:
                self.w(u'<th class="today">%s<br/>%s %s</th>' %
                       (title, self._cw._(calendar.WEEKDAYS[date.weekday()]),
                        self._cw.format_date(wdate)))
            else:
                self.w(u'<th class="today">%s<br/>%s</th>' %
                       (self._cw._(calendar.WEEKDAYS[date.weekday()]),
                        self._cw.format_date(wdate)))
        else:
            if title:
                self.w(u'<th>%s<br/>%s %s</th>' %
                       (title, self._cw._(calendar.WEEKDAYS[date.weekday()]),
                        self._cw.format_date(wdate)))
            else:
                self.w(u'<th>%s<br/>%s</th>' %
                       (self._cw._(calendar.WEEKDAYS[date.weekday()]),
                        self._cw.format_date(wdate)))
        self.w(u'</tr>')

        # build day calendar
        self.w(u'<tr>')
        self.w(u'<td style="width:1%;">') # column for hours
        extra = u''
        for h in range(8, 20):
            self.w(u'<div class="hour" %s>'%extra)
            self.w(u'%02d:00'%h)
            self.w(u'</div>')
        self.w(u'</td>')

        wdate = date
        classes = ""
        if wdate.isocalendar() == _today.isocalendar():
            classes = " today"
        self.w(u'<td class="column %s" id="%s">' % (classes, calendar.WEEKDAYS[date.weekday()]))
        if len(self.cw_rset.column_types(0)) == 1:
            etype = list(self.cw_rset.column_types(0))[0]
            url = self._cw.build_url(vid='creation', etype=etype,
                                     schedule=True,
                                     __redirectrql=self.cw_rset.printable_rql(),
                                     __redirectparams=self._cw.build_url_params(year=year, week=week),
                                     __redirectvid=self.__regid__
                                 )
            extra = (u' ondblclick="addCalendarItem(event, hmin=8, hmax=20, '
                     u'year=%s, month=%s, day=%s, duration=2, baseurl=\'%s\')"'
                     % (wdate.year, wdate.month, wdate.day, xml_escape(url)))
        else:
            extra = u''
        self.w(u'<div class="columndiv"%s>'% extra)
        for h in range(8, 20):
            self.w(u'<div class="hourline" style="top:%sex;">'%((h-7)*8))
            self.w(u'</div>')
        self._build_calendar_cell(wdate, task_descrs)

        self.w(u'</div>')
        self.w(u'</td>')
        self.w(u'</tr>')
        self.w(u'</table>')

    def _build_calendar_cell(self, date, task_descrs):
        inday_tasks = [t for t in task_descrs
                       if t.is_one_day_task() and t.in_working_hours()]
        wholeday_tasks = [t for t in task_descrs if not t.is_one_day_task()]
        inday_tasks.sort(key=lambda t:t.task.start)
        sorted_tasks = []
        for i, t in enumerate(wholeday_tasks):
            t.index = i
        ncols = len(wholeday_tasks)
        while inday_tasks:
            t = inday_tasks.pop(0)
            for i, c in enumerate(sorted_tasks):
                if not c or c[-1].task.stop <= t.task.start:
                    c.append(t)
                    t.index = i+ncols
                    break
            else:
                t.index = len(sorted_tasks) + ncols
                sorted_tasks.append([t])
        ncols += len(sorted_tasks)
        if ncols == 0:
            return

        inday_tasks = []
        for tasklist in sorted_tasks:
            inday_tasks += tasklist
        width = 100.0/ncols
        for task_desc in wholeday_tasks + inday_tasks:
            task = task_desc.task
            start_hour = 8
            start_min = 0
            stop_hour = 20
            stop_min = 0
            if task.start:
                if todatetime(date) < todatetime(task.start) < todatetime(date + calendar.ONEDAY):
                    start_hour = max(8, task.start.hour)
                    start_min = task.start.minute
            if task.stop:
                if todatetime(date) < todatetime(task.stop) < todatetime(date + calendar.ONEDAY):
                    stop_hour = min(20, task.stop.hour)
                    if stop_hour < 20:
                        stop_min = task.stop.minute

            height = 100.0*(stop_hour+stop_min/60.0-start_hour-start_min/60.0)/(20-8)
            top = 100.0*(start_hour+start_min/60.0-8)/(20-8)
            left = width*task_desc.index
            style = "height: %s%%; width: %s%%; top: %s%%; left: %s%%; " % \
                (height, width, top, left)
            self.w(u'<div class="task %s" style="%s">' % \
                       (task_desc.color, style))
            task.view('calendaritem', dates=False, w=self.w)
            params = self._cw.build_url_params(year=date.year, week=date.isocalendar()[1])
            url = task.absolute_url(vid='edition',
                                    __redirectrql=self.cw_rset.printable_rql(),
                                    __redirectparams=params,
                                    __redirectvid=self.__regid__
                                    )

            self.w(u'<div class="tooltip" ondblclick="stopPropagation(event); '
                   u'window.location.assign(\'%s\'); return false;">'
                   % xml_escape(url))
            task.view('tooltip', w=self.w)
            self.w(u'</div>')
            if task.start is None:
                self.w(u'<div class="bottommarker">'
                       u'<div class="bottommarkerline" '
                       u'style="margin: 0px 3px 0px 3px; height: 1px;"></div>'
                       u'<div class="bottommarkerline" '
                       u'style="margin: 0px 2px 0px 2px; height: 1px;"></div>'
                       u'<div class="bottommarkerline" '
                       u'style="margin: 0px 1px 0px 1px; height: 3ex; '
                       u'color: white; font-size: x-small; vertical-align: center; '
                       u'text-align: center;">end</div>'
                       u'</div>')
            self.w(u'</div>')

