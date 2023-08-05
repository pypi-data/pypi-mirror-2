#
# Tests for quintagroup.plonegooglesitemaps
#

import re, sys
from urllib import urlencode
from StringIO import StringIO
import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.setup import portal_owner
from Products.PloneTestCase.setup import default_password

from XMLParser import parse, hasURL

import quintagroup.plonegooglesitemaps
from quintagroup.plonegooglesitemaps.config import PROJECTNAME
from quintagroup.plonegooglesitemaps.config import ping_googlesitemap

quintagroup.plonegooglesitemaps.config.testing = 1
quintagroup.plonegooglesitemaps.config.UPDATE_CATALOG = True


class MixinTestCase:
    """ Define layer and common afterSetup method with package installation.
        Package installation on plone site setup impossible because of
        five's registerPackage directive not recognized on module initializing.
    """
    layer = PloneSite

    def afterSetUp(self):
        self.loginAsPortalOwner()


class TestCase(MixinTestCase, ptc.PloneTestCase):
    """ For unit tests """

class FunctionalTestCase(MixinTestCase, ptc.FunctionalTestCase):
    """ For functional tests """

# Initialize all needed zcml directives
fiveconfigure.debug_mode = True
from Products import Five, CMFCore, GenericSetup
zcml.load_config('meta.zcml', Five)
zcml.load_config('meta.zcml', CMFCore)
zcml.load_config('meta.zcml', GenericSetup)
zcml.load_config('permissions.zcml', Five)

# Force quintagroup.plonegooglesitemaps zcml initialization
zcml.load_config('configure.zcml', quintagroup.plonegooglesitemaps)
zcml.load_config('overrides.zcml', quintagroup.plonegooglesitemaps)
fiveconfigure.debug_mode = False

# Install quintagroup.plonegooglesitemaps package and Plone site
# with the default profile for the package
PRODUCT = 'quintagroup.plonegooglesitemaps'
ptc.installPackage(PRODUCT)
ptc.setupPloneSite( products=(PRODUCT,))
