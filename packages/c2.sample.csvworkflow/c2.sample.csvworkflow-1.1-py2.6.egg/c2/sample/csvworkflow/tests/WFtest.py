# -*- coding: utf-8 -*-

class WFtest(object):

    def doActionLoop(self, obj, trans):
        for tran in trans: obj.portal_workflow.doActionFor(obj, tran)
        return None

    def getWorkflowStateById(self, pwf, wf_id):
        wf = pwf.getWorkflowById(str(wf_id))
        return [state for state in getattr(wf, 'states', None)]
