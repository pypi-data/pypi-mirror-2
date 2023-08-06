"""Google Responder

A Google responder that authenticates against Google using OpenID, or optionally
can use OpenId+OAuth hybrid protocol to request access to Google Apps using OAuth2.

"""
try:
     from urlparse import parse_qs
except ImportError:
     from cgi import parse_qs


from openid.extensions import ax
import oauth2 as oauth

from velruse.providers.oid_extensions import OAuthRequest
from velruse.providers.oid_extensions import UIRequest
from velruse.providers.openidconsumer import ax_attributes, alternate_ax_attributes, attributes
from velruse.providers.openidconsumer import OpenIDResponder

GOOGLE_OAUTH = 'https://www.google.com/accounts/OAuthGetAccessToken'


class GoogleResponder(OpenIDResponder):
    def __init__(self, consumer=None, oauth_key=None, oauth_secret=None, request_attributes=None, *args,
                 **kwargs):
        """Handle Google Auth
        
        This also handles making an OAuth request during the OpenID
        authentication.
        
        """
        super(GoogleResponder, self).__init__(*args, **kwargs)
        self.consumer = consumer
        self.oauth_secret = oauth_secret
        if request_attributes:
            self.request_attributes = request_attributes.split(",")
        else:
            self.request_attributes = ['country', 'email', 'first_name', 'last_name', 'language']

    @classmethod
    def parse_config(cls, config):
        """Parse config data from a config file
        
        We call the super's parse_config first to update it with our additional
        values.
        
        """
        conf = OpenIDResponder.parse_config(config)
        params = {}
        key_map = {'OAuth Consumer Key': 'consumer', 'OAuth Consumer Secret': 'oauth_secret', 'Protocol': 'protocol',
                'Realm': 'realm', 'Endpoint Regex': 'endpoint_regex', "Request Attributes": 'request_attributes' }
        google_vals = config['Google']
        if not isinstance(google_vals, dict):
            return conf
        for k, v in key_map.items():
            if k in google_vals:
                params[v] = google_vals[k]
        conf.update(params)
        if 'Schema' in config['OpenID'] and config['OpenID']['Schema'] in globals():
            globals()["attributes"] = globals()[config['OpenID']['Schema']]

        return conf
    
    def _lookup_identifier(self, req, identifier):
        """Return the Google OpenID directed endpoint"""
        return "https://www.google.com/accounts/o8/id"
    
    def _update_authrequest(self, req, authrequest):
        """Update the authrequest with Attribute Exchange and optionally OAuth
        
        To optionally request OAuth, the request POST must include an ``oauth_scope``
        parameter that indicates what Google Apps should have access requested.
        
        """
        ax_request = ax.FetchRequest()
        for attr in self.request_attributes:
            ax_request.add(ax.AttrInfo(attributes[attr], required=True))
        authrequest.addExtension(ax_request)
        
        # Add OAuth request?
        if 'oauth_scope' in req.POST:
            oauth_request = OAuthRequest(consumer=self.consumer, scope=req.POST['oauth_scope'])
            authrequest.addExtension(oauth_request)
        
        if 'popup_mode' in req.POST:
            kw_args = {'mode': req.POST['popup_mode']}
            if 'popup_icon' in req.POST:
                kw_args['icon'] = req.POST['popup_icon']
            ui_request = UIRequest(**kw_args)
            authrequest.addExtension(ui_request)
        return None
    
    def _get_access_token(self, request_token):
        """Retrieve the access token if OAuth hybrid was used"""
        consumer = oauth.Consumer(key=self.consumer, secret=self.oauth_secret)
        token = oauth.Token(key=request_token, secret='')
        client = oauth.Client(consumer, token)
        resp, content = client.request(GOOGLE_OAUTH, "POST")
        if resp['status'] != '200':
            return None
        
        access_token = dict(parse_qs(content))
        
        return {'oauthAccessToken': access_token['oauth_token'], 
                'oauthAccessTokenSecret': access_token['oauth_token_secret']}
