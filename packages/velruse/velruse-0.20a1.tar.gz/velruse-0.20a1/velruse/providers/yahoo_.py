import logging

try:
     from urlparse import parse_qs
except ImportError:
     from cgi import parse_qs


import oauth2 as oauth
from openid.extensions import ax

from velruse.providers.oid_extensions import OAuthRequest
from velruse.providers.openidconsumer import ax_attributes
from velruse.providers.openidconsumer import OpenIDResponder

YAHOO_OAUTH = 'https://api.login.yahoo.com/oauth/v2/get_token'
log = logging.getLogger(__name__)


class YahooResponder(OpenIDResponder):
    def __init__(self, consumer=None, oauth_key=None, oauth_secret=None, *args,
                 **kwargs):
        """Handle Yahoo Auth

        This also handles making an OAuth request during the OpenID
        authentication.

        """
        super(YahooResponder, self).__init__(*args, **kwargs)
        self.consumer = consumer
        self.oauth_secret = oauth_secret

    @classmethod
    def parse_config(cls, config):
        """Parse config data from a config file

        We call the super's parse_config first to update it with our additional
        values.

        """
        conf = OpenIDResponder.parse_config(config)
        params = {}
        key_map = {'Consumer Key': 'consumer', 'Consumer Secret': 'oauth_secret',
                   'Realm': 'realm', 'Endpoint Regex': 'endpoint_regex'}
        yahoo_vals = config['Yahoo']
        if not isinstance(yahoo_vals, dict):
            return conf
        for k, v in key_map.items():
            if k in yahoo_vals:
                params[v] = yahoo_vals[k]
        conf.update(params)
        return conf

    def _lookup_identifier(self, req, identifier):
        """Return the Yahoo OpenID directed endpoint"""
        return 'https://me.yahoo.com/'

    def _update_authrequest(self, req, authrequest):
        # Add on the Attribute Exchange for those that support that            
        ax_request = ax.FetchRequest()
        for attrib in ax_attributes.values():
            ax_request.add(ax.AttrInfo(attrib))
        authrequest.addExtension(ax_request)

        # Add OAuth request?
        if 'oauth' in req.POST:
            oauth_request = OAuthRequest(consumer=self.consumer)
            authrequest.addExtension(oauth_request)
        return None

    def _get_access_token(self, request_token):
        consumer = oauth.Consumer(key=self.consumer, secret=self.oauth_secret)
        token = oauth.Token(key=request_token, secret='')
        client = oauth.Client(consumer, token)
        resp, content = client.request(YAHOO_OAUTH, "POST")
        if resp['status'] != '200':
            log.error("OAuth token validation failed. Status: %s, Content: %s",
                resp['status'], content)
            return None

        access_token = dict(parse_qs(content))

        return {'oauthAccessToken': access_token['oauth_token'], 
                'oauthAccessTokenSecret': access_token['oauth_token_secret']}
