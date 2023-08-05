from collective.amberjack.core.interfaces import ITourDefinition
from collective.amberjack.core.tests.base import AmberjackCoreTestCase
from collective.amberjack.core.tour import Tour, Step
from zope.component import getUtility, provideUtility
from zope.schema._bootstrapfields import WrongType
from zope.schema.interfaces import InvalidURI
import unittest
from zope.component.globalregistry import base

def registerTour(tour=None):
    if not tour:
        tour = {'tourId': u'dummy_id',
                'title': u'Dummy title',
                'steps': ()}
    tour = Tour(**tour) 
    provideUtility(component=tour, provides=ITourDefinition, name=tour.tourId)
        
def createStep(step):
    Step(**step)
    
class TourTestCase(AmberjackCoreTestCase):

    def afterSetUp(self):
        #Remove all tour definitions
        utilities = base.getUtilitiesFor(ITourDefinition)
        for utility in utilities:
            base.unregisterUtility(component=utility[1], provided=ITourDefinition, name=utility[0])        

    def test_tour_registration_validation(self):
        self.assertRaises(AttributeError, registerTour, {'tourId': u'dummy_id'},)
        self.assertRaises(WrongType, registerTour, {'tourId': 'dummy_id'},)
        self.assertRaises(AttributeError, registerTour, {'tourId': u'id',
                                                         'title': u'title',
                                                         'steps': None},)
        
        self.assertRaises(TypeError, registerTour, {'tourId': u'id',
                                                    'title': u'title',
                                                    'steps': (None,)},)
        

    def test_proper_tour_registration(self):
        registerTour({'tourId': u'id',
                      'title': u'title',
                      'steps': ({'url': u'/opt/var',
                                 'xpath': u'xpath expression',
                                 'xcontent': u'xcontent',
                                 'title': u'title',
                                 'text': u'text',
                                 'steps': ()},
                                 ),
                      })
        tour = getUtility(ITourDefinition, name=u'id')
        self.assertEqual(tour.title, u'title')


    def test_step_validation(self):
        self.assertRaises(AttributeError, createStep, {'url': u'/path',
                                                       'xcontent': u'xcontent',
                                                       'title': u'title',
                                                       'text': u'text',
                                                       'steps': ()},)



def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TourTestCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
