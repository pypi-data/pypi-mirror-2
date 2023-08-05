from cubicweb.selectors import implements
from cubicweb.appobject import Selector, objectify_selector
from cubicweb.web.facet import RelationFacet, DateRangeFacet

# This selector is used by the TalkDate facet,
# the start_time date is optional.

# N.B. The selector will be useless in 3.6.1, patch submitted.

@objectify_selector
def talk_with_start_time(cls, req, rset, row=0, col=0, **kwargs):
    if len([entity.start_time for entity in rset.entities() if
            entity.start_time is not None]) > 0:
        return 1
    return 0

class TalkDateFacet(DateRangeFacet):
    __regid__ = 'date-facet'
    __select__ = DateRangeFacet.__select__ & implements('Talk') & talk_with_start_time()
    rtype = 'start_time'

class TalkTrackFacet(RelationFacet):
    __regid__ = 'track-facet'
    __select__ = RelationFacet.__select__ & implements('Talk')
    rtype = 'in_track'
    target_attr = 'title'

class TalkTagsFacet(RelationFacet):
    __regid__ = 'tags-facet'
    __select__ = RelationFacet.__select__ & implements('Talk')
    rtype = 'tags'
    target_attr = 'name'

class TalkConferenceFacet(RelationFacet):
    __regid__ = 'conference-facet'
    __select__ = RelationFacet.__select__ & implements('Talk')
    rtype = 'in_conf'
    target_attr = 'title'
