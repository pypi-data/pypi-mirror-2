# python
import os, sys
import cjson
from time import sleep

# zope
import transaction

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from anz.ijabbar.browser.viewlets import IJabbarViewlet
from anz.ijabbar.tests.base import AnzIJabbarTestCase

class TestIJabbarViewlet( AnzIJabbarTestCase ):

    def afterSetUp( self ):
        request = self.app.REQUEST
        context = self.folder
        self.viewlet = IJabbarViewlet( context, request, None, None )
    
    def test_update( self ):
        ap = self.portal.portal_properties.anz_ijabbar_properties
        
        # first time
        self.viewlet.update()
        iJabConf = cjson.decode( self.viewlet.iJabConf )
	self.assertEqual( iJabConf['expand_bar_default'], True )
        self.assertEqual( iJabConf['expand_bar_default'],
			  getattr(ap,'expand_bar_default') )
        
        # test cache
        self.viewlet.update()
        iJabConf = cjson.decode( self.viewlet.iJabConf )
	self.assertEqual( iJabConf['expand_bar_default'], True )
        self.assertEqual( iJabConf['expand_bar_default'],
			  getattr(ap,'expand_bar_default') )
        
        sleep( 3 )
	
        # modify
        self._setProperty( ap, 'expand_bar_default', False, 'boolean' )
	
	# Hack, we need a _p_mtime for the ap object, so we make sure that it
        # has one. We use a subtransaction, which means we can rollback
        # later and pretend we didn't touch the ZODB.
        transaction.commit()
	
	self.viewlet.update()
	iJabConf = cjson.decode( self.viewlet.iJabConf )
	self.assertEqual( iJabConf['expand_bar_default'], False )
	self.assertEqual( iJabConf['expand_bar_default'],
			  getattr(ap,'expand_bar_default') )
    
    def test_render( self ):
        ret = self.viewlet.render()
        self.assert_( ret.find('<div id="ijabbar"') != -1 )

    def _setProperty( self, sheet, id, value, type ):
	if sheet.hasProperty( id ):
	    sheet.manage_delProperties( ids=[id,] )
	
	sheet.manage_addProperty( id, value, type )
    
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest( makeSuite(TestIJabbarViewlet) )
    return suite

if  __name__ == '__main__':
    framework()