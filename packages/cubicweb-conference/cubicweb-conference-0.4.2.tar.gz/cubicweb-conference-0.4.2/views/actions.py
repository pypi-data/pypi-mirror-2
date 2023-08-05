from cubicweb.web.action import LinkToEntityAction
from cubicweb.web.views.actions import CopyAction, ModifyAction, AddNewAction, AddRelatedActions
from cubicweb.selectors import implements, match_user_groups, score_entity, rql_condition
from cubicweb.schema import ERQLExpression, RRQLExpression

# actions

class ConferenceAddTrackAction(LinkToEntityAction):
    __regid__ = 'addtrack'
    __select__ = (LinkToEntityAction.__select__ &
                  implements('Conference') &
                  match_user_groups('managers'))
    etype = 'Track'
    rtype = 'in_conf'
    target = 'subject'
    title = _('add Track in conference Conference object')

# There is an "attend" relation. This relation is always visible so we have to
# redefined the "modify" action for managers & owners.

class ManagersAddAction(AddRelatedActions):
     __select__ = AddRelatedActions.__select__ & match_user_groups('managers')

class ManagersModifyAction(ModifyAction):
    __select__ = ModifyAction.__select__ & match_user_groups('managers')

class OwnersModifyAction(ModifyAction):
    __select__ = (ModifyAction.__select__ &
                  implements('Talk') &
                  match_user_groups('owners') &
                  score_entity(lambda x: x.state in ('draft', 'correction')))

class AddDocument(LinkToEntityAction):
    __regid__ = 'adddoc'
    __select__ = (LinkToEntityAction.__select__ &
                  implements('Talk') &
                  (match_user_groups('managers') |
                   (rql_condition('X owned_by U') &
                    score_entity(lambda x: x.state in ('draft', 'correction')))))
    target_etype = 'File'
    rtype = 'has_attachments'
    target = 'object'
    title = _(u'add document to the talk')

# score_entity

def registration_callback(vreg):
    vreg.unregister(CopyAction)
    vreg.unregister(AddRelatedActions)
    vreg.register(ManagersModifyAction)
    vreg.register(AddDocument)
    vreg.register_and_replace(OwnersModifyAction, ModifyAction)

