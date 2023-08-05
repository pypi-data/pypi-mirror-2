from cubicweb.web import uicfg
from cubes.conference.views.forms import subject_in_track_vocabulary, subject_in_conf_vocabulary

_pvs = uicfg.primaryview_section
_pvs.tag_subject_of(('Talk', 'has_attachments', 'File'), 'hidden')
_pvs.tag_object_of(('CWUser', 'leads', 'Talk'), 'hidden')
_pvs.tag_object_of(('*', 'in_conf', '*'), 'hidden')
_pvs.tag_subject_of(('*', 'in_conf', '*'), 'hidden')
_pvs.tag_subject_of(('Talk', 'in_track', '*'), 'hidden')
_pvs.tag_object_of(('Talk', 'in_track', '*'), 'hidden')
_pvs.tag_subject_of(('CWUser', 'attend', '*'), 'hidden')
_pvs.tag_object_of(('CWUser', 'reviews', 'Talk'), 'hidden')

_abaa = uicfg.actionbox_appearsin_addmenu
_abaa.tag_subject_of(('Talk', 'has_attachments', 'File'), True)
_abaa.tag_object_of(('Talk', 'in_track', 'Track'), True)
_abaa.tag_object_of(('Sponsor', 'supports_conf', 'Conference'), True)

_afs = uicfg.autoform_section
_afs.tag_object_of(('CWUser', 'leads', 'Talk'), formtype='main', section='hidden')
_afs.tag_subject_of(('Sponsor', 'has_logo', '*'), formtype='main', section='inlined')

uicfg.autoform_field_kwargs.tag_subject_of(('Talk', 'in_track', 'Track'),
                                           {'choices': subject_in_track_vocabulary})

uicfg.autoform_field_kwargs.tag_subject_of(('Talk', 'in_conf', 'Conference'),
                                           {'choices': subject_in_conf_vocabulary})
