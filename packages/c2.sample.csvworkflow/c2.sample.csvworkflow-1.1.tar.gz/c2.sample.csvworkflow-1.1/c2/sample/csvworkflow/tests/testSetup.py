# -*- coding: utf-8 -*-

import unittest
import Testing

from plone.app.contentrules.tests.base import ContentRulesTestCase
from Products.CMFCore.permissions import AccessContentsInformation
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import ListFolderContents
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import _checkPermission as checkPerm
from unittest import TestSuite, makeSuite
from WFtest import *

from c2.sample.csvworkflow.tests.base import C2CsvworkflowTestCase

class TestWorkflowAction(C2CsvworkflowTestCase):

    def afterSetUp(self):
        workflow_id = 'c2.sample.csvworkflow' # Apply Workflow
        self.workflow = self.portal.portal_workflow
        self.workflow.setDefaultChain(workflow_id)
        self.portal.acl_users._doAddUser('test_user', 'secret', ['Manager'], []) 
        self.folder.invokeFactory('Document', 'd1')
        self.doc = self.folder.d1

    def testInitialState(self):
        initial_state = 'private' # The initial state of the workflow
        self.assertEquals(self.workflow.getInfoFor(self.doc, 'review_state'), initial_state) 

    def testAllState(self):
        workflow_id = self.workflow.getChainFor(self.doc)[0]
        states = ['private', 'pending', 'published'] # All state with workflow
        wft = WFtest()
        self.assertEqual(set(wft.getWorkflowStateById(self.workflow, workflow_id)), set(states))

    def testTransitionAction(self):
        route_newstate = [
            ('submit', 'pending'), 
            ('publish', 'published'), 
            ('reject', 'private'),
        ] # (transition_id, new_state_id) Workflow transitions in this order
        self.login('test_user')
        for transition, new_state in route_newstate:
            self.doc.portal_workflow.doActionFor(self.doc, transition)
            self.assertEquals(self.workflow.getInfoFor(self.doc, 'review_state'), new_state)

    def testTransitions(self):
        route = ['submit', 'publish'] # Transition to run. Now state is 'published'
        roles = ['Reviewer'] # User have roles
        transitions = ['reject'] # Have transition
        wft = WFtest()
        self.login('test_user')
        wft.doActionLoop(self.doc, route)
        self.portal.acl_users._doAddUser('test_user_2', 'secret', roles, [])
        self.login('test_user_2')
        self.assertEquals([data['id'] for data in self.workflow.getTransitionsFor(self.doc)], transitions)

    def testdPermissions(self):
        route = ['submit', 'publish'] # Transition to run. Now state is 'published'
        roles = ['Reviewer'] # User have role
        accept_per = [AccessContentsInformation, View] # Accept permissions
        reject_per = [ModifyPortalContent] # Reject permissions
        wft = WFtest()
        self.portal.acl_users._doAddUser('test_user', 'secret', ['Manager'], [])
        self.login('test_user')
        wft.doActionLoop(self.doc, route)
        self.portal.acl_users._doAddUser('test_user_2', 'secret', roles, [])
        self.login('test_user_2')
        for hasper in accept_per: self.failUnless(checkPerm(hasper, self.doc))
        for not_hasper in reject_per: self.failIf(checkPerm(not_hasper, self.doc))

def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestWorkflowAction))
    return suite
