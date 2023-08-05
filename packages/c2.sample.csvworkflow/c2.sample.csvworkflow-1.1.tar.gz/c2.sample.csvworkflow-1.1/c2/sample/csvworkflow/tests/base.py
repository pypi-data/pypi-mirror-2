from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

ztc.installProduct('SimpleAttachment')
ztc.installProduct('RichDocument')

@onsetup
def setup_optilux_policy():
    fiveconfigure.debug_mode = True
    import c2.sample.csvworkflow
    zcml.load_config('configure.zcml', c2.sample.csvworkflow)
    fiveconfigure.debug_mode = False

    ztc.installPackage('c2.sample.csvworkflow')

setup_optilux_policy()
ptc.setupPloneSite(products=['c2.sample.csvworkflow'])

class C2CsvworkflowTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """
