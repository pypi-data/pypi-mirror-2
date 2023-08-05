
# vocabulary for add / talk form

def subject_in_conf_vocabulary(form, field):
    rset = form._cw.execute('Any C ORDERBY T DESC LIMIT 1 WHERE C is Conference, C start_on T')
    if rset:
        entity = rset.get_entity(0,0)
        return [(e.dc_title(), e.eid) for e in [entity] if e.eid != form.edited_entity.eid]
    return []

def subject_in_track_vocabulary(form, field):
    rset = form._cw.execute('DISTINCT Any T WHERE T is Track, T in_conf C WITH C BEING (Any C ORDERBY T DESC LIMIT 1 WHERE C is Conference, C start_on T)')
    if rset:
        return [(entity.dc_title(), entity.eid) for entity in rset.entities()]
    return []
