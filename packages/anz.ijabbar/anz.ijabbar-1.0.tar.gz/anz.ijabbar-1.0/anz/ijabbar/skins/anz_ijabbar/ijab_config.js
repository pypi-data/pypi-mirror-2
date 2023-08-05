var iJabConf =
{
    client_type:"xmpp",
    app_type:"bar",
    theme:"standard",
    debug:false,
    avatar_url:"http://samespace.anzsoft.com/portal_memberdata/portraits/{username}",
    enable_roster_manage:true,
    enable_talkto_stranger:true,
    expand_bar_default:false,
    enable_login_dialog:true,
    hide_online_group:false,
    disable_option_setting:false,
    disable_msg_browser_prompt:false,
    xmpp:{
        domain:"anzsoft.com",
        http_bind:"http://samespace.anzsoft.com:5280/http-bind/",
        host:"",
        port:5222,
        server_type:"ejabberd",
        auto_login:false,
        none_roster:false,
        get_roster_delay:true,
        username_cookie_field:"username",
        token_cookie_field:"SID",
        anonymous_prefix:"",
        max_reconnect:3,
        enable_muc:true,
        muc_servernode:"conference.anzsoft.com",
        vcard_search_servernode:"vjud.anzsoft.com",
        gateways:
        [
        	{
        		icon:"http://example.com/msn.png",
        		name:"MSN Transport",
        		description:"",
        		servernode:"msn-transport.anzsoft.com"
        	}
        ]       
    },
    disable_toolbox:false,
    tools:
    [
    	{
    		href:"http://www.google.com",
    		target:"_blank",
    		img:"http://www.google.cn/favicon.ico",
    		text:"Google Search"
    	},
    	{
    		href:"http://www.xing.com/",
    		target:"_blank",
    		img:"http://www.xing.com/favicon.ico",
    		text:"Xing"
    	}
    ],
    shortcuts:
    [
    	{
    		href:"http://www.anzsoft.com/",
    		target:"_blank",
    		img:"http://www.anzsoft.com/favicon.ico",
    		text:"Go to anzsoft"
    	},
    	{
    		href:"http://www.google.com",
    		target:"_blank",
    		img:"http://www.google.cn/favicon.ico",
    		text:"Google Search"
    	}
    ],
    ijabcometd:{
    }
};