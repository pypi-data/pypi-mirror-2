"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
"""

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from Products.CMFCore.utils import getToolByName

from Products.Collage.interfaces import IDynamicViewManager


import os
from App import Common

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
    import collective.collage.imagetags
    zcml.load_config('configure.zcml', collective.collage.imagetags)
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

    ztc.installPackage('collective.collage.imagetags')

# The order here is important: We first call the (deferred) function
# which installs the products we need for this product. Then, we let
# PloneTestCase set up this product on installation.

setup_product()
ptc.setupPloneSite(products=['collective.collage.imagetags'])

class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """

from OFS.interfaces import IFolder
class ISpecialFolder(IFolder):
    pass

class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """

    def afterSetUp(self):
        roles = ('Member', 'Contributor')
        self.portal.portal_membership.addMember('contributor',
                                                'secret',
                                                roles, [])
                                                
class FunctionalTestCaseWithContent(FunctionalTestCase):

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        FunctionalTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()


    def afterSetUp(self):
        super(FunctionalTestCase, self).afterSetUp()
        self.loginAsPortalOwner()
        wtool = getToolByName(self.portal, 'portal_workflow')

        # Image file
        pkg_home = Common.package_home({'__name__': 'collective.collage.imagetags'})
        samplesdir = os.path.join(pkg_home, 'tests', 'samples')
        image_file = file(os.path.join(samplesdir, 'test_image.png')).read()
        
        # News item without image
        id = self.portal.invokeFactory('News Item', 'no-image')
        ob = getattr(self.portal, id)
        ob.setTitle('News item without image')
        wtool.doActionFor(ob, 'publish')
        ni = ob
        
        # News item with image
        id = self.portal.invokeFactory('News Item', 'with-image')
        ob = getattr(self.portal, id)
        ob.setTitle('News item with image')
        ob.setImage(image_file)
        wtool.doActionFor(ob, 'publish')
        wi = ob
        
        # Image
        id = self.portal.invokeFactory('Image', 'image')
        ob = getattr(self.portal, id)
        ob.setTitle('Test Image')
        ob.setImage(image_file)
        # Image is automatically published
        image = ob
        
        # Page (Document)
        id = self.portal.invokeFactory('Document', 'doc')
        ob = getattr(self.portal, id)
        ob.setTitle('Test Document')
        wtool.doActionFor(ob, 'publish')
        doc = ob

        # Pre-build a Collage with 4 aliases for each of the just created objects
        # and set the layout to make sure "Image tags" is a link during test
        id = self.portal.invokeFactory('Collage', 'collage')
        collage = getattr(self.portal, id)
        collage.setTitle('Collage')
        wtool.doActionFor(collage, 'publish')
        self.collage = collage

        # Row & Column
        id = collage.invokeFactory('CollageRow', '1')
        row = getattr(collage, id)
        id = row.invokeFactory('CollageColumn', '1')
        column = getattr(row, id)

        # Alias for doc with standard layout
        id = column.invokeFactory('CollageAlias', 'alias-1')
        alias1 = getattr(column, id)
        alias1.set_target(doc.UID())
        manager = IDynamicViewManager(alias1)
        manager.setLayout('standard')

        # Alias for image with standard layout
        id = column.invokeFactory('CollageAlias', 'alias-2')
        alias2 = getattr(column, id)
        alias2.set_target(image.UID())
        manager = IDynamicViewManager(alias2)
        manager.setLayout('standard')
        
        # Alias for newsitem with image with standard layout
        id = column.invokeFactory('CollageAlias', 'alias-3')
        alias3 = getattr(column, id)
        alias3.set_target(wi.UID())
        manager = IDynamicViewManager(alias3)
        manager.setLayout('standard')

        # Alias for newsitem withoug image with standard layout
        id = column.invokeFactory('CollageAlias', 'alias-4')
        alias4 = getattr(column, id)
        alias4.set_target(ni.UID())
        manager = IDynamicViewManager(alias4)
        manager.setLayout('standard')  

        # Check if there's only one registered layout for images
        # Workaround for Collage 1.3.0_b4 + Plone 4.05b
        manager = IDynamicViewManager(image)
        layouts = [x[0] for x in manager.getLayouts()]
        # There should be at least 'tags' and 'standard'
        register_more = len(layouts)==2 and 'tags' in layouts and 'standard' in layouts
        if register_more:
            import collective.collage.imagetags.tests.image_hack
            zcml.load_config("configure.zcml", package=collective.collage.imagetags.tests.image_hack)
