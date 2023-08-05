#!/usr/bin/env python
"""NDG XACML Context unit test package 

NERC DataGrid
"""
__author__ = "P J Kershaw"
__date__ = "26/03/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id: test_context.py 7443 2010-09-03 13:42:43Z pjkersha $"
import unittest
from os import path
import logging
logging.basicConfig(level=logging.DEBUG)

from ndg.xacml.test import XACML_NDGTEST1_FILEPATH
from ndg.xacml.parsers.etree.factory import ReaderFactory
from ndg.xacml.core import Identifiers
from ndg.xacml.core.context.pdpinterface import PDPInterface
from ndg.xacml.core.context.pdp import PDP
from ndg.xacml.core.context.handler import CtxHandlerInterface
from ndg.xacml.core.attribute import Attribute
from ndg.xacml.core.attributevalue import (AttributeValue, 
                                           AttributeValueClassFactory)
from ndg.xacml.core.context.request import Request
from ndg.xacml.core.context.response import Response
from ndg.xacml.core.context.result import Result, Decision
from ndg.xacml.core.context.subject import Subject
from ndg.xacml.core.context.resource import Resource
from ndg.xacml.core.context.action import Action

attributeValueFactory = AttributeValueClassFactory()
AnyUriAttributeValue = attributeValueFactory(AttributeValue.ANY_TYPE_URI)
StringAttributeValue = attributeValueFactory(AttributeValue.STRING_TYPE_URI)

ROLE_ATTRIBUTE_ID = "urn:ndg:security:authz:1.0:attr"
SUBJECT_ID = 'https://my.name.somewhere.ac.uk'

class TestContextHandler(CtxHandlerInterface):
    """Test implementation of Context Handler which includes an implemented PIP
    interface"""
    
    def __init__(self):
        """Add an attribute to hold a reference to a policy information point"""
        
        super(TestContextHandler, self).__init__()
        self.pip = None        
        
    def handlePEPRequest(self, myRequest):
        """Handle request from Policy Enforcement Point
        
        @param pepRequest: request from PEP, derived class determines its type
        e.g. SAML AuthzDecisionQuery
        @type myRequest: type
        @return: PEP response - derived class determines type
        @rtype: None
        """
        
        # Convert myRequest to XACML context request - var assignment here is 
        # representative of this process rather than actually doing anything.
        xacmlRequest = myRequest
        
        if self.pdp is None:
            raise TypeError('No "pdp" attribute set')
        
        # Add a reference to this context so that the PDP can invoke queries
        # back to the PIP
        xacmlRequest.ctxHandler = self 
               
        xacmlResponse = self.pdp.evaluate(xacmlRequest)
        
        # Convert XACML context response to domain specific request
        myResponse = xacmlResponse
        
        return myResponse
    
    def pipQuery(self, request, designator):
        '''PIP adds admin attribute value for given attribute ID and for any 
        subject'''
        if designator.attributeId == ROLE_ATTRIBUTE_ID:
            attrVal = StringAttributeValue(value='admin')
            return [attrVal]
        else:
            return None


class XacmlContextBaseTestCase(unittest.TestCase):
    """Base class containing common methods for test initialisation"""
    
    def _createRequestCtx(self, 
                          resourceId, 
                          includeSubject=True,
                          subjectRoles=('staff',),
                          roleAttributeId=ROLE_ATTRIBUTE_ID,
                          action='read'):
        """Create an example XACML Request Context for tests"""
        request = Request()
        
        if includeSubject:
            subject = Subject()
            openidSubjectAttribute = Attribute()
            
            
            openidSubjectAttribute.attributeId = "urn:esg:openid"
            openidSubjectAttribute.dataType = AnyUriAttributeValue.IDENTIFIER
            
            openidSubjectAttribute.attributeValues.append(
                                                        AnyUriAttributeValue())
            openidSubjectAttribute.attributeValues[-1].value = SUBJECT_ID
                                        
            
            subject.attributes.append(openidSubjectAttribute)
    
            for role in subjectRoles:
                roleAttribute = Attribute()
                
                roleAttribute.attributeId = roleAttributeId
                roleAttribute.dataType = StringAttributeValue.IDENTIFIER
                
                roleAttribute.attributeValues.append(StringAttributeValue())
                roleAttribute.attributeValues[-1].value = role 
            
                subject.attributes.append(roleAttribute)
                                      
            request.subjects.append(subject)
        
        resource = Resource()
        resourceAttribute = Attribute()
        resource.attributes.append(resourceAttribute)
        
        resourceAttribute.attributeId = Identifiers.Resource.RESOURCE_ID
                            
        resourceAttribute.dataType = AnyUriAttributeValue.IDENTIFIER
        resourceAttribute.attributeValues.append(AnyUriAttributeValue())
        resourceAttribute.attributeValues[-1].value = resourceId

        request.resources.append(resource)
        
        request.action = Action()
        actionAttribute = Attribute()
        request.action.attributes.append(actionAttribute)
        
        actionAttribute.attributeId = Identifiers.Action.ACTION_ID
        actionAttribute.dataType = StringAttributeValue.IDENTIFIER
        actionAttribute.attributeValues.append(StringAttributeValue())
        actionAttribute.attributeValues[-1].value = action
        
        return request
        
    def _createPDPfromPolicy(self):
        pdp = PDP.fromPolicySource(XACML_NDGTEST1_FILEPATH, ReaderFactory)
        return pdp    


class XacmlContextTestCase(XacmlContextBaseTestCase):
    """Test PDP, PAP, PIP and Context handler"""
    
    def test01CreateRequest(self):
        requestCtx = self._createRequestCtx("http://localhost")
        self.assert_(requestCtx)
        
    def test02CreateResponse(self):
        response = Response()
        result = Result()
        response.results.append(result)
        result.decision = Decision()
        result.decision.value = Decision.NOT_APPLICABLE
        
    def test03AbstractCtxHandler(self):
        self.assertRaises(TypeError, CtxHandlerInterface, 
                          "Context handler is an abstract base class")
        
    def test04CreateCtxHandler(self):
        ctxHandler = TestContextHandler()
        
    def test05PDPInterface(self):
        self.assertRaises(TypeError, PDPInterface)
        
    def test06CreatePDP(self):
        pdp = PDP()
        self.assert_(pdp)
        
    def test07CreatePDPfromPolicy(self):
        pdp = self._createPDPfromPolicy()
        self.assert_(pdp)
    
    
class XacmlEvalPdpWithPermitOverridesPolicy(XacmlContextBaseTestCase):
    """Test PDP with permit overrides rule combining algorithm"""
    
    NOT_APPLICABLE_RESOURCE_ID = 'https://localhost'
    
    # This could be any applicable resource value, provided there's no rule to
    # override and enable access
    PRIVATE_RESOURCE_ID = 'http://localhost/private-resource'
    
    PUBLIC_RESOURCE_ID = 'http://localhost/resource-only-restricted'
    NOT_APPLICABLE_RESOURCE_ID = 'https://localhost'
        
    SINGLE_SUBJECT_ROLE_RESTRICTED_ID = \
        'http://localhost/single-subject-role-restricted'
    ACTION_AND_SINGLE_SUBJECT_ROLE_RESTRICTED_ID = \
        'http://localhost/action-and-single-subject-role-restricted'
    AT_LEAST_ONE_SUBJECT_ROLE_RESTRICTED_ID = \
        'http://localhost/at-least-of-subject-role-restricted'
        
    def setUp(self):
        self.pdp = self._createPDPfromPolicy()
        
    def test01NotApplicable(self):
        # Set a resource Id that doesn't match the main target
        request = self._createRequestCtx(
                                    self.__class__.NOT_APPLICABLE_RESOURCE_ID)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.NOT_APPLICABLE, 
                        "Expecting not applicable decision")
        
    def test02PublicallyAccessibleResource(self):
        # Test a resource which has no subject restrictions
        request = self._createRequestCtx(self.__class__.PUBLIC_RESOURCE_ID,
                                         includeSubject=False)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision")
        
    def test03PrivateResource(self):
        request = self._createRequestCtx(
                                    self.__class__.PRIVATE_RESOURCE_ID)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 
                        "Expecting Deny decision")

    def test04SingleSubjectRoleRestrictedResource(self):
        # Access based on a resource ID and single subject role
        request = self._createRequestCtx(
                            self.__class__.SINGLE_SUBJECT_ROLE_RESTRICTED_ID)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision")  

    def test05SingleSubjectRoleRestrictedResourceDeniesAccess(self):
        # Subject doesn't have the required role for access
        request = self._createRequestCtx(
                            self.__class__.SINGLE_SUBJECT_ROLE_RESTRICTED_ID,
                            subjectRoles=('student',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 
                        "Expecting Deny decision")  

    def test06ActionAndSingleSubjectRoleRestrictedResource(self):
        # Test restriction based on action type as well as subject role
        request = self._createRequestCtx(
                    self.__class__.ACTION_AND_SINGLE_SUBJECT_ROLE_RESTRICTED_ID)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision")

    def test07ActionAndSingleSubjectRoleRestrictedResourceDeniesAccess(self):
        # Test subject requests invalid action type
        request = self._createRequestCtx(
                    self.__class__.ACTION_AND_SINGLE_SUBJECT_ROLE_RESTRICTED_ID,
                    action='write')
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 
                        "Expecting Deny decision")  

    def test08AtLeastOneSubjectRoleResource(self):
        # Test at least one member function
        request = self._createRequestCtx(
                    self.__class__.AT_LEAST_ONE_SUBJECT_ROLE_RESTRICTED_ID,
                    action='write')
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting Permit decision")             

    def test09AtLeastOneSubjectRoleResourceDeniesAccess(self):
        # Test at least one member function where subject doesn't have one of
        # the required roles
        request = self._createRequestCtx(
                    self.__class__.AT_LEAST_ONE_SUBJECT_ROLE_RESTRICTED_ID,
                    subjectRoles=('student',))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 
                        "Expecting Deny decision")             
    
    def test10PipAddsRequiredAttributeValToEnableAccess(self):
        # The PDP is part of a context handler with a PIP which adds subject
        # attributes under prescribed conditions on the evaluation of 
        # subject attribute designators.  In this case the addition of the PIP
        # adds an attribute value to one of the subject's attributes which means
        # they're granted access where otherwise access would be denied
        ctxHandler = TestContextHandler()
        ctxHandler.pdp = self.pdp
        
        request = self._createRequestCtx(
                    self.__class__.AT_LEAST_ONE_SUBJECT_ROLE_RESTRICTED_ID,
                    subjectRoles=('student',))
        
        response = ctxHandler.handlePEPRequest(request)
        self.failIf(response is None, "Null response")
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 
                        "Expecting PERMIT decision")         
        
                                
if __name__ == "__main__":
    unittest.main()