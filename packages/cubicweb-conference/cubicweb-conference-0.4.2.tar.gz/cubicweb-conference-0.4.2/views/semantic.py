
from logilab.mtconverter import xml_escape

from cubicweb.view import EntityView
from cubicweb.web.views.urlrewrite import SimpleReqRewriter
from cubicweb.selectors import implements, one_line_rset

class SwrcTalkView(EntityView):
    __regid__ = 'swrc'
    __select__ = implements('Talk')
    title = _('swrc')
    templatable = False
    content_type = 'text/xml'
    def call(self):
        self.w(u'''<?xml version="1.0" encoding="%s"?>
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        xmlns:rdfs="http://www.w3org/2000/01/rdf-schema#"
        xmlns:swrc="http://swrc.ontoware.org/ontology#"
        xmlns:swc="http://data.semanticweb.org/ns/swc/ontology#"
        xmlns:foaf="http://xmlns.com/foaf/0.1/"
        xmlns:dc="http://purl.org/dc/elements/1.1/#">\n''' % self._cw.encoding)
        for i in xrange(self.cw_rset.rowcount):
            self.cell_call(i, 0)
        self.w(u'</rdf:RDF>\n')

    def cell_call(self, row, col):
        entity = self.cw_rset.complete_entity(row, col)
        for conf in entity.in_conf:
            self.w(u'<swc:isPartOf rdf:resource="%s"/>' % conf.absolute_url())
        for track in entity.in_track:
            self.w(u'<swc:isPartOf rdf:resource="%s"/>' % track.absolute_url())
        self.w(u'<swrc:InProceedings rdf:about="%s"/>' % entity.absolute_url())
        self.w(u'<dc:title>%s</dc:title>' % entity.dc_title())
        self.w(u'<swrc:abstract><![CDATA[%s]]></swrc:abstract>' % entity.description)
        for author in entity.reverse_leads:
            self.w(u'<swrc:author rdf:resource="%s"/>' % author.absolute_url())
        for doc in entity.has_attachments:
            self.w(u'<swc:hasRelatedDocument rdf:resource="%s"/>' % doc.absolute_url())

class SwrcConferenceView(EntityView):
    __regid__ = 'swrc'
    __select__ = implements('Conference') & one_line_rset()
    title = _('swrc')
    templatable = False
    content_type = 'text/xml'
    def call(self):
        self.w(u'''<?xml version="1.0" encoding="%s"?>
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        xmlns:rdfs="http://www.w3org/2000/01/rdf-schema#"
        xmlns:swrc="http://swrc.ontoware.org/ontology#"
        xmlns:swc="http://data.semanticweb.org/ns/swc/ontology#"
        xmlns:foaf="http://xmlns.com/foaf/0.1/"
        xmlns:dc="http://purl.org/dc/elements/1.1/#">\n''' % self._cw.encoding)
        self.cell_call(0, 0)
        self.w(u'</rdf:RDF>\n')

    def cell_call(self, row, col):
        entity = self.cw_rset.complete_entity(row, col)
        self.w(u'<rdf:type rdf:resource="http://data.semanticweb.org/ns/swc/ontology#ConferenceEvent"/>')
        self.w(u'<swrc:hasAcronym>%s</swrc:hasAcronym>' % entity.title)
        for track in entity.reverse_in_conf:
            self.w(u'<swrc:isSuperEventOf rdf:resource="%s"/>' % track.absolute_url())

