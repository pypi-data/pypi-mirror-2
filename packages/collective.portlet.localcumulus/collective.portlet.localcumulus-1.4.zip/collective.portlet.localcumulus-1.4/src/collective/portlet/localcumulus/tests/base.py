from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup


################################################################################
"""


Lot of files generated by the collective.generic packages  will try to load user defined objects in user specific files.
The final goal is to regenerate easyly the test infrastructure on templates updates without impacting
user-specific test boilerplate.
We do not use paster local commands (insert/update) as it cannot determine witch is specific or not and we prefer to totally
separe generated stuff and what is user specific



If you need to edit something in this file, you must have better to do it in:


    - user_base.py


Objects that you can edit and get things overidden are:


    - user_base.py

        * method: setup_collective_portlet_localcumulus()

            method to setup the plone site

        * class: collective_portlet_localcumulus_TestCase

            Base plone test case like PloneTestCase

        * class: collective_portlet_localcumulus_FunctionalTestCase:

            Functionnal TestBase barely based on the previous TestCase.

"""
################################################################################


TESTED_PRODUCTS = ()
for product in TESTED_PRODUCTS:
    ztc.installProduct(product)

@onsetup
def setup_localcumulusPloneSite():
    """Set up the additional products required for the collective.portlet) site localcumulus.

    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    # ------------------------------------------------------------------------------------
    # Get five errors if any for making debug easy.
    # ------------------------------------------------------------------------------------
    fiveconfigure.debug_mode = True

    # ------------------------------------------------------------------------------------
    # Import all our python modules required by our packages
    # ------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------
    # - Load the ZCML configuration for the collective.portlet.localcumulus package.
    # ------------------------------------------------------------------------------------


    import plone.memoize
    zcml.load_config('configure.zcml', plone.memoize)

    # ------------------------------------------------------------------------------------
    # - Load the python packages that are registered as Zope2 Products via Five
    #   which can't happen until we have loaded the package ZCML.
    # ------------------------------------------------------------------------------------


    # ------------------------------------------------------------------------------------
    # Load our own localcumulus
    # ------------------------------------------------------------------------------------
    import collective.portlet.localcumulus


    ztc.installPackage('collective.portlet.localcumulus')

    # ------------------------------------------------------------------------------------
    # Reset five debug mode as we do not use it anymore
    # ------------------------------------------------------------------------------------
    fiveconfigure.debug_mode = False


class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """

class FunctionalTestCase(TestCase):
    """Functionnal base TestCase."""

# try to load user code
try: from collective.portlet.localcumulus.tests.user_base import setup_localcumulusPloneSite
except: pass

try:from collective.portlet.localcumulus.tests.user_base import TestCase
except: pass

try:from collective.portlet.localcumulus.tests.user_base import FunctionalTestCase
except: pass

# The order here is important: We first call the (deferred) function which
# installs the products we need for the collective.portlet package. Then, we let
# PloneTestCase set up this product on installation.
def setup_site():
    setup_localcumulusPloneSite()
    ptc.setupPloneSite(products=[\
        'quintagroup.portlet.cumulus',
        'collective.portlet.localcumulus'

                                ]
    )
# vim:set ft=python:
