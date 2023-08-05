from cubicweb.cwconfig import register_persistent_options

register_persistent_options((
    ('sponsor-contact-email',
     {'type' : 'string',
      'default': 'unset',
      'help': 'Sponsor contact email',
      'group': 'ui',
      'site_wide': True}),
     ))
