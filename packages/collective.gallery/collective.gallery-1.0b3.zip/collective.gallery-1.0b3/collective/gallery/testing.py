from Products.PloneTestCase import ptc
from Testing import ZopeTestCase
from collective.testcaselayer import ptc as tcl_ptc
from collective.testcaselayer import common

class Layer(tcl_ptc.BasePTCLayer):
    """Install collective.foo"""

    def afterSetUp(self):
        ZopeTestCase.installPackage('collective.gallery')

        import collective.gallery
        self.loadZCML('configure.zcml', package=collective.gallery)

        self.addProfile('collective.gallery:default')

layer = Layer([common.common_layer])
