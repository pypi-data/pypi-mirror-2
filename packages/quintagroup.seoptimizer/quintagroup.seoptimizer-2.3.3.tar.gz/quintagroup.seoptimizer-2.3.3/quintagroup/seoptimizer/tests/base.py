"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
"""
import re
from AccessControl.SecurityManagement import newSecurityManager

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from Products.CMFCore.utils import getToolByName
from config import PROJECT_NAME

# When ZopeTestCase configures Zope, it will *not* auto-load products
# in Products/. Instead, we have to use a statement such as:
#   ztc.installProduct('SimpleAttachment')
# This does *not* apply to products in eggs and Python packages (i.e.
# not in the Products.*) namespace. For that, see below.
# All of Plone's products are already set up by PloneTestCase.

@onsetup
def setup_product():
    """Set up the package and its dependencies.

    The @onsetup decorator causes the execution of this body to be
    deferred until the setup of the Plone site testing layer. We could
    have created our own layer, but this is the easiest way for Plone
    integration tests.
    """

    # Load the ZCML configuration for the example.tests package.
    # This can of course use <include /> to include other packages.

    fiveconfigure.debug_mode = True
    import quintagroup.seoptimizer
    zcml.load_config('configure.zcml', quintagroup.seoptimizer)
    zcml.load_config('overrides.zcml', quintagroup.seoptimizer)
    fiveconfigure.debug_mode = False

    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML. Thus, we do it here. Note the use of installPackage()
    # instead of installProduct().
    # This is *only* necessary for packages outside the Products.*
    # namespace which are also declared as Zope 2 products, using
    # <five:registerPackage /> in ZCML.

    # We may also need to load dependencies, e.g.:
    #   ztc.installPackage('borg.localrole')

    ztc.installPackage(PROJECT_NAME)

# The order here is important: We first call the (deferred) function
# which installs the products we need for this product. Then, we let
# PloneTestCase set up this product on installation.

setup_product()
ptc.setupPloneSite(products=[PROJECT_NAME])


class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """

class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """

    #def afterSetUp(self):
        #roles = ('Member', 'Contributor')
        #self.portal.portal_membership.addMember('contributor',
                                                #'secret',
                                                #roles, [])

#class TestErase(TestCase):
    ## we use here nested layer for not to make an impact on
    ## the rest test cases, this test case check uninstall procedure
    ## thus it has to uninstall package which will be required to
    ## be installed for other test cases
    #class layer(PloneSiteLayer):
        #@classmethod
        #def setUp(cls):
            #app = ztc.app()
            #portal = app.plone

            ## elevate permissions
            #user = portal.getWrappedOwner()
            #newSecurityManager(None, user)

            #tool = getToolByName(portal, 'portal_quickinstaller')
            #if tool.isProductInstalled(PROJECT_NAME):
                #tool.uninstallProducts([PROJECT_NAME,])

            ## drop elevated perms
            #noSecurityManager()

            #transaction.commit()
            #ztc.close(app)

