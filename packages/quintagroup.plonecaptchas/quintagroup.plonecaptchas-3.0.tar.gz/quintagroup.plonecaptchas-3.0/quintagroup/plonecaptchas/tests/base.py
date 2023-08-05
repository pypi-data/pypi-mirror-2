import os, sys, re
import unittest
import transaction

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import setup as ptc_setup
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup, PloneSite
from Products.PloneTestCase.PloneTestCase import portal_owner
from Products.PloneTestCase.PloneTestCase import default_password

from Products.CMFCore.utils import getToolByName

from quintagroup.captcha.core.tests.base import testPatch
from quintagroup.captcha.core.tests.testWidget import NOT_VALID
from quintagroup.captcha.core.tests.testWidget import IMAGE_PATT
from quintagroup.captcha.core.tests.testWidget import addTestLayer
from quintagroup.captcha.core.utils import getWord, decrypt, parseKey

from quintagroup.plonecaptchas.config import *

# TESTING CONSTANTS
CAPTCHA_KEY = 'captcha_key'
CAPTCHAS_COUNT = 165
LAYERS = ['captchas_discussion', 'captchas_sendto_form', 'captchas_join_form']

TOOL_ICON = 'skins/plone_captchas/tool.gif'
TOOL_ID = 'portal_captchas'
CONFIGLET_ID = "qpc_tool"
PROPERTY_SHEET = 'qPloneCaptchas'

# join_form profile prefix
JF_PROFILE_PREFIX = 'profile-quintagroup.plonecaptchas:join_form_plone_'

ptc.setupPloneSite()

class NotInstalled(PloneSite):
    """ Only package register, without installation into portal
    """

    @classmethod
    def setUp(cls):
        fiveconfigure.debug_mode = True
        import quintagroup.captcha.core
        import quintagroup.plonecaptchas
        zcml.load_config('configure.zcml', quintagroup.captcha.core)
        zcml.load_config('configure.zcml', quintagroup.plonecaptchas)
        fiveconfigure.debug_mode = False
        ztc.installPackage('quintagroup.plonecaptchas')
        ztc.installPackage('quintagroup.captcha.core')


class Installed(NotInstalled):
    """ Install product into the portal
    """
    @classmethod
    def setUp(cls):
        app = ztc.app()
        portal = app[ptc_setup.portal_name]

        # Sets the local site/manager
        ptc_setup._placefulSetUp(portal)
        # Install PROJECT
        qi = getattr(portal, 'portal_quickinstaller', None)
        qi.installProduct(PRODUCT_NAME)

        # Install Join Form layer, depends on Plone version
        js_layer = None
        if getattr(ptc_setup, 'PLONE33', 0):
            js_layer = JF_PROFILE_PREFIX+'33'
        elif getattr(ptc_setup, 'PLONE32', 0):
            js_layer = JF_PROFILE_PREFIX+'31_32'
        elif getattr(ptc_setup, 'PLONE31', 0):
            js_layer = JF_PROFILE_PREFIX+'31_32'
        elif getattr(ptc_setup, 'PLONE30', 0):
            js_layer = JF_PROFILE_PREFIX+'30'
        if js_layer is not None:
            gs = getattr(portal, 'portal_setup', None)
            gs.runAllImportStepsFromProfile(js_layer)

        transaction.commit()

    @classmethod
    def tearDown(cls):
        ptc_setup._placefulTearDown()
        

class TestCase(ptc.PloneTestCase):
    layer = Installed

class TestCaseNotInstalled(ptc.PloneTestCase):
    layer = NotInstalled


class FunctionalTestCase(ptc.FunctionalTestCase):
    layer = Installed

class FunctionalTestCaseNotInstalled(ptc.FunctionalTestCase):
    layer = NotInstalled
