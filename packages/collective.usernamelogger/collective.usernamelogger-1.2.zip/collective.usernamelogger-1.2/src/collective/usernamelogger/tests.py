from unittest import TestCase, defaultTestLoader
from zope.testing import doctest
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from collective.testcaselayer.ptc import BasePTCLayer, ptc_layer

optionflags = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

ptc.setupPloneSite()


class Layer(BasePTCLayer):
    """ set up basic testing layer """

    def afterSetUp(self):
        # load zcml for this package and its dependencies
        fiveconfigure.debug_mode = True
        from collective import usernamelogger
        zcml.load_config('configure.zcml', package=usernamelogger)
        fiveconfigure.debug_mode = False
        # after which the required packages can be initialized
        ptc.installPackage('collective.usernamelogger', quiet=True)

layer = Layer(bases=[ptc_layer])


class FunctionalTestCase(ptc.FunctionalTestCase):
    """ base class for functional tests """

    layer = layer


class UsernameTests(TestCase):

    def username(self, value):
        from collective.usernamelogger import username
        from base64 import encodestring
        return username('__ac=%s' % encodestring(value))

    def testSessionCookieWithColon(self):
        self.assertEquals(self.username('john:secret'), 'john')

    def testSessionCookieWithColonInHex(self):
        self.assertEquals(self.username('6a6f686e:736563726574'), 'john')

    def testSessionCookieWithSpaces(self):
        self.assertEquals(self.username('\xd2\xe7\x9bh\x81\xd6=U\xd1\x8f\x07'
            '\xa1\xb2*JdC\x14\x8a\xab john'), 'john')

    def testSessionCookieWithExclamationMark(self):
        self.assertEquals(self.username('\xa35\xeeE\xad\x93\xd1\x0b\xff\x0f'
            '\xf1\x1b\xb1\xb1c7\x85\xf1U\x00\x1f"\'Ci\x16\xd6$nF894e3aa223john'
            '!'), 'john')


def test_suite():
    suite = defaultTestLoader.loadTestsFromName(__name__)
    suite.addTest(
        ztc.FunctionalDocFileSuite(
           'browser.txt', package='collective.usernamelogger',
           test_class=FunctionalTestCase, optionflags=optionflags)
    )
    return suite
