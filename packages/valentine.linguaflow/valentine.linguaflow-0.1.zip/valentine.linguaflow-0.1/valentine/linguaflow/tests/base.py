from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_valentine_linguaflow():

    fiveconfigure.debug_mode = True
    import Products.Five
    import valentine.linguaflow
    zcml.load_config('meta.zcml', Products.Five)
    zcml.load_config('configure.zcml', valentine.linguaflow)
    zcml.load_config('testing.zcml', valentine.linguaflow.tests)
    fiveconfigure.debug_mode = False

    ptc.installProduct('PloneLanguageTool')
    ptc.installProduct('LinguaPlone')


setup_valentine_linguaflow()

ptc.setupPloneSite(products=['PloneLanguageTool','LinguaPlone', 'valentine.linguaflow'], extension_profiles=('valentine.linguaflow:default','valentine.linguaflow.tests:testing'))

class ValentineLinguaflowTestCase(ptc.PloneTestCase):
    """ """

class ValentineLinguaflowFunctionalTestCase(ptc.FunctionalTestCase):
    """ """
