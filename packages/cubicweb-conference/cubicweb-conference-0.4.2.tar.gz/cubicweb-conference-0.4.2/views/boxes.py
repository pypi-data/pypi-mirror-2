# primary views
from logilab.mtconverter import xml_escape
from cubicweb.web import box
from cubicweb.selectors import implements

class CallForPaperBox(box.BoxTemplate):
    __regid__ = 'callbox'

    context = 'left'
    title = _(u'Call for paper')
    order = 0

    def call(self, **kwargs):
        w = self.w
        w(u'<div id="papercall">')
        w(u'<div id="papercall2">')
        w(u'<div class="callforpaper"><a href="%s">%s</a>'
          % (xml_escape(self._cw.build_url('add/Talk')),
             self._cw._('Abstract submission is open !')))
        w(u'</div></div></div>')

class SponsorBox(box.EntityBoxTemplate):
    __regid__ = 'sponsorbox'
    __select__ = (box.EntityBoxTemplate.__select__ &
                  implements('Conference','Talk'))
    context = 'right'
    title = 'Sponsors'

    def cell_call(self, row, col, **kwargs):
        _cw = self._cw
        w = self.w
	entity = self.cw_rset.get_entity(row, col)
        if entity.e_schema.type == 'Conference':
            rql = ('Any L, X, I WHERE I is Image, X has_logo I, X is_sponsor S, S level L, S sponsoring_conf C, C eid %(conf)s')
            rset = _cw.execute(rql, {'conf':entity.eid})
        elif entity.e_schema.type == 'Talk':
            rql = ('Any L, X, I WHERE I is Image, X has_logo I, X is_sponsor S, S level L, S sponsoring_conf C, T in_conf C, T eid %(talk)s')
            rset = _cw.execute(rql, {'talk':entity.eid})
        w(u'<div class="sideBox" id="%s">' % self.__regid__)
        w(u'<div class="sideBoxTitle"><span>%s</span></div>' % _cw._(self.title))
        w(u'<div class="sideBoxBody">')
        if rset:
            # sort sponsor by level
            sponsors = [(level, seid, imgeid) for (level ,seid, imgeid) in rset]
            lhash = {'Gold':3, 'Silver':2, 'Bronze':1, 'Media':1}
            sponsors.sort(cmp=lambda x,y: cmp(lhash[x[0]], lhash[y[0]]))
            for (level, sponsor_eid, image_eid) in rset:
                sponsor = _cw.entity_from_eid(sponsor_eid)
                img = _cw.entity_from_eid(image_eid)
                # adapt image size
                w(u'<div class="%s">' % level)
                w(u'<a href="%s"><img src="%s" alt="%s"/></a>' %
                  (sponsor.url, img.absolute_url(vid="download"), img.title))
                w(u'</div>')
        w(u'<p>%s <a href="mailto:%s">%s</a></p>' % (_cw._('If you are interested in sponsoring or partnering'),
                                                    self._cw.property_value('ui.sponsor-contact-email'),
                                                    _cw._('please contact us')))
        w(u'</div></div>')

class AtTheSameTimeBox(box.EntityBoxTemplate):
    __regid__ = 'atthesametimebox'
    __select__ = (box.EntityBoxTemplate.__select__ &
                  implements('Talk'))
    context = 'incontext'
    title = _(u'At the same time')

    def cell_call(self, row, col, **kwargs):
        _cw = self._cw
        w = self.w
        entity = self.cw_rset.get_entity(row, col)
        rql = ('Any T WHERE T is Talk, NOT T eid %(eid)s, NOT T start_time NULL AND NOT T end_time NULL')
        rset = _cw.execute(rql, {'eid':entity.eid})
        start = entity.start_time
        end = entity.end_time
        if rset and start is not None and end is not None:
            at_the_same_time = []
            for talk in rset.entities():
                s = talk.start_time
                e = talk.end_time
                if (start <= s <= end) or (e >= start and s < end) or (start < e <= end):
                    at_the_same_time.append(talk)
            if len(at_the_same_time):
                w(u'<div class="sideBox" id="%s">' % self.__regid__)
                w(u'<div class="sideBoxTitle"><span>%s</span></div>' % _cw._(self.title))
                w(u'<div class="sideBoxBody">')
                for talk in at_the_same_time:
                    w(u'<p><a href="%s">%s</a></p>' % (talk.absolute_url(), talk.dc_title()))
                w(u'</div></div>')

