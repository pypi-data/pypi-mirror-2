from collective.amberjack.core.interfaces import IMicroStepsManager
from collective.amberjack.core.tests.base import AmberjackCoreTestCase
from collective.amberjack.core.micro_steps_manager import registry
from plone.registry import Record
from plone.registry import field
from zope.component import getUtility, provideUtility
import unittest
from zope.component.globalregistry import base


    
class TourManagerTestCase(AmberjackCoreTestCase):

    def test_getSteps_single_registration(self):
        steps = (('name1', 'selector1'),('name2', 'selector2'),)
        microsteps = field.Tuple(title=u'microstep')
        record_microstep = Record(microsteps)
        record_microstep.value = steps
        registry.records['collective.amberjack.core.microsteps'] = record_microstep
        re_steps = ()
        microstepsmanager = getUtility(IMicroStepsManager)
        for s in microstepsmanager.getSteps():
            re_steps = re_steps + s
        
        self.assertNotEqual(re_steps, steps)
        
    def test_getSteps_double_registration(self):
        steps_a = (('name1', 'selector1'),('name2', 'selector2'),)
        steps_b = (('name3', 'selector3'),('name4', 'selector4'),)
        
        # set the steps
        microsteps = field.Tuple(title=u'microstep')
        record_microstep = Record(microsteps)
        record_microstep.value = steps_a
        registry.records['collective.amberjack.core.microsteps'] = record_microstep
        registry.records['collective.amberjack.core.microsteps'].value += steps_b
        
        # get teh steps
        microstepsmanager = getUtility(IMicroStepsManager)
        re_steps = ()
        for s in microstepsmanager.getSteps():
            re_steps = re_steps + s
        self.assertNotEqual(re_steps, steps_a+steps_b)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TourManagerTestCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
