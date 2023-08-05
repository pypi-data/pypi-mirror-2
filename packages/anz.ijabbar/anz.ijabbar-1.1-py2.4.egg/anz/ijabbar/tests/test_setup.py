# python
import os, sys

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from anz.ijabbar.tests.base import AnzIJabbarTestCase

class TestProductInstall( AnzIJabbarTestCase ):

    def test_skinLayersInstalled( self ):
        subIds = self.portal.portal_skins.objectIds()
        ids = [ 'anz_ijabbar', ]
        for id in ids:
            self.assert_( id in subIds )

    def test_propertiesInstalled( self ):
        self.assert_( 'anz_ijabbar_properties' in \
                      self.folder.portal_properties.objectIds() )
        
        properties = self.folder.portal_properties.anz_ijabbar_properties
        
        # todo
        # test each property
        '''
        # test 'typesToList' property
        self.assert_( hasattr(properties,'typesToList') )
        
        self.assertEqual( properties.getPropertyType('typesToList'), 'lines' )
        self.assertEqual( properties.getProperty('typesToList'), () )
        '''

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest( makeSuite(TestProductInstall) )
    return suite

if  __name__ == '__main__':
    framework()