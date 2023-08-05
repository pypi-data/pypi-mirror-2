from cubicweb.view import EntityView
from cubicweb.web import formfields as ff, formwidgets as fwdgs
from cubicweb.web.views.workflow import (WorkflowActions, WFHistoryView,
                                         WFHistoryVComponent, ChangeStateFormView)
from cubicweb.selectors import (match_user_groups, rql_condition,
                                relation_possible, score_entity, implements)

class SendToReviewerStatusChangeView(ChangeStateFormView):
    __select__ = (ChangeStateFormView.__select__ &
                  implements('Talk') &
                  rql_condition('X in_state S, S name "submitted"'))

    def get_form(self, entity, transition, **kwargs):
        # XXX used to specify both rset/row/col and entity in case implements
        # selector (and not implements) is used on custom form
        form = self._cw.vreg['forms'].select(
            'changestate', self._cw, entity=entity, transition=transition,
            redirect_path=self.redirectpath(entity), **kwargs)

        relation = ff.RelationField(name='reviews', role='object',
                                    eidparam=True,
                                    label=_('select reviewers'),
                                    widget=fwdgs.Select(multiple=True))
        form.append_field(relation)
        trinfo = self._cw.vreg['etypes'].etype_class('TrInfo')(self._cw)
        trinfo.eid = self._cw.varmaker.next()
        subform = self._cw.vreg['forms'].select('edition', self._cw, entity=trinfo,
                                                mainform=False)
        subform.field_by_name('wf_info_for', 'subject').value = entity.eid
        trfield = subform.field_by_name('by_transition', 'subject')
        trfield.widget = fwdgs.HiddenInput()
        trfield.value = transition.eid
        form.add_subform(subform)
        return form

class ConferenceWFHistoryVComponent(WFHistoryVComponent):
    __regid__ = 'wfhistory'
    __select__ = (WFHistoryVComponent.__select__ &
                  (match_user_groups('owners', 'managers') | rql_condition('U reviews X')))

class ConferenceWFHistoryView(EntityView):
    __regid__ = 'wfhistory'
    __select__ = (relation_possible('wf_info_for', role='object') &
                  score_entity(lambda x: x.workflow_history) &
                  implements('Talk') &
                  (rql_condition('U reviews X') | match_user_groups('managers','owners')))
    title = _('Workflow history')

    def cell_call(self, row, col, view=None):
        _ = self._cw._
        eid =  self.cw_rset[row][col]
        sel = 'Any FS,TS,WF,D,C'
        rql = ' ORDERBY D DESC WHERE WF wf_info_for X,'\
              'WF from_state FS, WF to_state TS, WF comment C,'\
              'WF creation_date D'
        displaycols = range(4)
        headers = (_('from_state'), _('to_state'), _('comment'), _('date'))
        rql = '%s %s, X eid %%(x)s' % (sel, rql)
        try:
            rset = self._cw.execute(rql, {'x': eid}, 'x')
        except Unauthorized:
            return
        if rset:
            self.wview('table', rset, title=_(self.title), displayactions=False,
                       displaycols=displaycols, headers=headers)

class SendToReviewerStatusChangeView(ChangeStateFormView):
    __select__ = (ChangeStateFormView.__select__ &
                  implements('Talk') &
                  rql_condition('X in_state S, S name "submitted"'))

    def get_form(self, entity, transition, **kwargs):
        # XXX used to specify both rset/row/col and entity in case implements
        # selector (and not implements) is used on custom form
        form = self._cw.vreg['forms'].select(
            'changestate', self._cw, entity=entity, transition=transition,
            redirect_path=self.redirectpath(entity), **kwargs)

        relation = ff.RelationField(name='reviews', role='object',
                                    eidparam=True,
                                    label=_('select reviewers'),
                                    widget=fwdgs.Select(multiple=True))
        form.append_field(relation)
        trinfo = self._cw.vreg['etypes'].etype_class('TrInfo')(self._cw)
        trinfo.eid = self._cw.varmaker.next()
        subform = self._cw.vreg['forms'].select('edition', self._cw, entity=trinfo,
                                                mainform=False)
        subform.field_by_name('wf_info_for', 'subject').value = entity.eid
        trfield = subform.field_by_name('by_transition', 'subject')
        trfield.widget = fwdgs.HiddenInput()
        trfield.value = transition.eid
        form.add_subform(subform)
        return form

def registration_callback(vreg):
    vreg.register(SendToReviewerStatusChangeView)
    vreg.register_and_replace(ConferenceWFHistoryView, WFHistoryView)
    vreg.register_and_replace(ConferenceWFHistoryVComponent, WFHistoryVComponent)
