# postcreate script. You could setup a workflow here for example

_ = unicode

moderators = add_entity('CWGroup', name=u"moderators")

set_property('boxes.blog_summary_box.visible', u'')

# Conference Workflow

def define_conference_workflow():
    twf = add_workflow(_('conference workflow'), 'Conference')
    planned = twf.add_state(_('planned'), initial=True)
    scheduled = twf.add_state(_('scheduled'))
    archived = twf.add_state(_('archived'))
    twf.add_transition(_('schedule'), (planned,), scheduled,
                       ('managers',),)
    twf.add_transition(_('archive'), (scheduled,), archived,
                       ('managers',),)

define_conference_workflow()

# Talk Workflow

talk_states = rql('Any T, N ORDERBY T WHERE T in_state S, S name N, T is Talk').rows

rql('DELETE Workflow WF WHERE WF workflow_of X, X name "Talk"')

def define_talk_workflow():
    twf = add_workflow(_('talk workflow'), 'Talk')
    draft = twf.add_state(_('draft'), initial=True)
    submitted = twf.add_state(_('submitted'))
    correction = twf.add_state(_('correction'))
    inreview = twf.add_state(_('inreview'))
    accepted = twf.add_state(_('accepted'))
    rejected = twf.add_state(_('rejected'))
    twf.add_transition(_('draft'), (draft,), submitted,
                       ('owners',))
    twf.add_transition(_('send to reviewer'), (submitted,), inreview,
                       ('managers',))
    twf.add_transition(_('need correction'), (inreview,), correction,
                       ('managers',), conditions=('U reviews X',))
    twf.add_transition(_('resend to reviewer'), (correction,), inreview,
                       ('owners',))
    twf.add_transition(_('accept talk'), (inreview,), accepted,
                       ('managers',), conditions=('U reviews X',))
    twf.add_transition(_('reject talk'), (inreview,), rejected,
                       ('managers',), conditions=('U reviews X',))

define_talk_workflow()

commit()
