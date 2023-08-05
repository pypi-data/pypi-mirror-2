
# python
import cjson

# zope
from Acquisition import aq_inner, aq_base
from zope.interface import implements
from zope.component import getUtility, getMultiAdapter
from zope.viewlet.interfaces import IViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

# cmf
from Products.CMFCore.utils import getToolByName

# plone
from plone.memoize.interfaces import ICacheChooser

class IJabbarViewlet( BrowserView ):
    ''' A viewlet show ijab bar. '''
    implements( IViewlet )
    index = ViewPageTemplateFile( 'ijab_bar.pt' )
    
    def __init__(self, context, request, view, manager):
        super(IJabbarViewlet, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
    
    def update( self ):
        chooser = getUtility( ICacheChooser )
        cache = chooser( 'anz.ijabbar.ijabconf' )
        
        pp = getToolByName( self.context, 'portal_properties' )
        ap = getattr( aq_base(pp), 'anz_ijabbar_properties' )
        
        modified = str( ap.bobobase_modification_time() )
        
        iJabConf = cache.get( modified, None )
        if iJabConf is None:
            iJabConf = {}
            iJabConf['client_type'] = 'xmpp'
            iJabConf['app_type'] = 'bar'
            iJabConf['theme'] = getattr( ap, 'ijab_theme', 'standard' )
            iJabConf['debug'] = getattr( ap, 'enable_debug', False )
            iJabConf['avatar_url'] = getattr( ap, 'avatar_url', '' )
            iJabConf['enable_roster_manage'] = getattr( ap, \
                                            'enable_roster_management', False )
            iJabConf['enable_talkto_stranger'] = getattr( ap, \
                                            'enable_talkto_stranger', True )
            iJabConf['expand_bar_default'] = getattr( ap, \
                                            'expand_bar_default', True )
            iJabConf['enable_login_dialog'] = getattr( ap, \
                                            'enable_login_dialog', True )
            iJabConf['hide_online_group'] = getattr( ap, \
                                            'hide_online_group', False )
            iJabConf['disable_option_setting'] = not getattr( ap, \
                                            'enable_option_setting', False )
            iJabConf['disable_msg_browser_prompt'] = not getattr( ap, \
                                            'enable_browser_prompt', False )
            iJabConf['disable_toolbox'] = not getattr( ap, \
                                            'enable_toolbox', False )
            
            
            iJabConf['xmpp'] = {
                'domain': getattr( ap,
                                   'xmpp_domain', '' ),
                'http_bind': getattr( ap,
                                      'xmpp_httpbind_server_host',
                                      'http://www.ijab.im/http-bind/' ),
                'host': getattr( ap,
                                 'xmpp_server_host', '' ),
                'port': getattr( ap,
                                 'xmpp_server_port', 5222 ),
                'server_type': getattr( ap,
                                        'xmpp_server_type', 'ejabberd' ),
                'auto_login': True,
                'none_roster': False,
                'get_roster_delay': True,
                'username_cookie_field': '__ijab_name',
                'token_cookie_field': '__ijab_password',
                'anonymous_prefix': '',
                'max_reconnect': 3,
                'enable_muc': True,
                'muc_servernode': '',
                'vcard_search_servernode': '',
                'gateways': []
                }
            
            iJabConf['tools'] = [{
                'href': 'http://www.google.com',
                'target': '_blank',
                'img': 'http://www.google.cn/favicon.ico',
                'text': 'Google Search'
                }]
            iJabConf['shortcuts'] = [{
                'href': 'http://www.anzsoft.com/',
                'target': '_blank',
                'img': 'http://www.anzsoft.com/favicon.ico',
                'text': 'Go to anzsoft'
                },{
                'href': 'http://www.ijab.im/',
                'target': '_blank',
                'img': 'http://www.ijab.im/themes/magazeen/favicon.ico',
                'text': 'Go to ijab'
                }]
            iJabConf['ijabcometd'] = {}
            
            iJabConf = cjson.encode( iJabConf )
            
            # cache
            cache[modified] = iJabConf
        
        self.iJabConf = iJabConf
        
        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        self.site_url = portal_state.portal_url()
    
    def render( self ):
        # defer to index method, because that's what gets overridden by the
        # template ZCML attribute
        return self.index()
