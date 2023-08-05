import urlparse

from client import FreelancerClient
from oauth2 import Token
from api import Freelancer
from exceptions import Exception

class FreelancerOauthError(Exception):
    """Exception raised during Oauth errors during exchanges with freelancer.com"""
    def __init__(self, msg=''):
         self.msg = msg

    def __str__(self):
        return ('Oauth request failed: %s' % (self.msg))
        
class FreelancerOauth(FreelancerClient):
    """
    FreelancerOauth is a utility class to simplify Oauth exchanges with freelancer.com

    Example:
        # Set your consumer keys as a tuple or list, and initialized the worker
        consumer = ('your key', 'your secret')
        oauth = FreelancerOauth(consumer)

        # Fetch your request tokens for this exchange. You can specify your callback
        # through the oauth_callback keyword argument.
        request_tokens = oauth->get_request_token(oauth_callback='http://example.com/?')

        # The default behavior is to authorize with the production enviroment of
        # freelancer.com. If you want to authorize with its sandbox, just pass
        # the 'domain' keyword argument with the domain you want to authorize against.
        request_tokens = oauth->get_request_token(oauth_callback='http://example.com/?', domain='api.sandbox.freelancer.com')

        # After the request tokens are set, you can build a proper authorization url
        # to redirect to.
        redirect_to = oauth->get_authorize_url()

        ...

        # Once the user authorizes the application on Freelancer and is redirected
        # to your callback, you can upgrade the request tokens to access tokens.
        # Reinitalize the FreelancerOauth worker if needed.
        consumer = ('your key', 'your secret')
        oauth = FreelancerOauth(consumer)

        # Since you most likely no longer have the request token's secret, you can
        # just pass the oauth request token as a string (retrieved from the GET
        # parameters passed to the callback url)
        request_token = 'whatever'

        # The verifier will also be retrieved differently depending on your situation.
        verifier = 'whatever'

        # And now you can get your tokens. If you need to authorize against the sandbox,
        # the 'domain' keyword argument is also accepted here.
        access_token = oauth->upgrade_to_access_token(verifier, request_token)
    """
    def __init__(self, consumer, token=None):
        """
        Creates a new utility class to make Oauth exchanges with freelancer.com

        Arguments:
        consumer -- a tuple or list of a consumer secret and key
        token -- a tuple or list of a token and token secret
        """
        FreelancerClient.__init__(self, consumer, token)
        self.request_token = None
        self.verifier = None
        self.access_token = None

    def get_request_token(self, *args, **kwargs):
        """
        Returns a tuple of oauth token, and oauth token secret

        Keyword Arguments:
        method_chain -- api call translated to list or tuple to access request token
        oauth_callback -- callback url to pass to freelancer.com
        """
        method_chain, kwargs = self.__pop_from_dict('method_chain', kwargs, ('RequestRequestToken','requestRequestToken'))

        api_call_qs, kwargs = self.__pop_from_dict('oauth_callback', kwargs, 'oob')
        kwargs['api_call_qs'] = {'oauth_callback': api_call_qs }

        resp = self.__api_call_from_chain(method_chain, **kwargs)
        self.request_token = self.__oauth_tuple_from_qs(resp)

        return self.request_token

    def get_authorize_url(self, request_token=False, app_url='http://www.freelancer.com/users/api-token/auth.php'):
        """
        Returns url for users to authorize application with

        Arguments:
        request_token -- string of a oauth token or a tuple or list of oauth token and secret
        app_url -- base url to use for authorization
        """
        self.request_token = self.__is_valid_token(request_token if request_token else self.request_token)
        return "%s?oauth_token=%s" % (app_url, self.request_token[0])

    def get_token_verifier(self, verifier, request_token=False, **kwargs):
        """
        Returns verifier to be used to retrieve access tokens

        Arguments:
        verifier -- verifier recieved from authorization
        request_token -- string of a oauth token or a tuple or list of oauth token and secret

        Keyword Arguments:
        method_chain -- api call translated to list or tuple to access request token
        """
        method_chain, kwargs = self.__pop_from_dict('method_chain', kwargs, ('RequestAccessToken','getRequestTokenVerifier'))

        self.request_token = self.__is_valid_token(request_token if request_token else self.request_token)
        token = Token(self.request_token[0], self.request_token[1])

        if verifier and isinstance(verifier, str):
            token.set_verifier(verifier)
        else:
            raise ValueError('Incorrect verifier type, expecting string')
        
        FreelancerClient.__init__(self, self.consumer, token)
        resp = self.__api_call_from_chain(method_chain, **kwargs)
        access_verifier = self.__oauth_verifier_from_qs(resp)
        self.verifier = access_verifier

        return access_verifier

    def get_access_token(self, verifier, request_token=False, **kwargs):
        """
        Returns a tuple of access tokens for a user

        Arguments:
        verifier -- verifier recieved from authorization
        request_token -- string of a oauth token or a tuple or list of oauth token and secret

        Keyword Arguments:
        method_chain -- api call translated to list or tuple to access request token
        """
        method_chain, kwargs = self.__pop_from_dict('method_chain', kwargs, ('RequestAccessToken', 'requestAccessToken'))
        
        self.request_token = self.__is_valid_token(request_token if request_token else self.request_token)
        token = Token(self.request_token[0], self.request_token[1])
        token.set_verifier(verifier)
        FreelancerClient.__init__(self, self.consumer, token)

        resp = self.__api_call_from_chain(method_chain, **kwargs)
        self.access_token = self.__oauth_tuple_from_qs(resp)

        return self.access_token

    def upgrade_to_access_token(self, verifier, request_token=False, **kwargs):
        """
        Returns a tuple of access tokens for a user

        Arguments:
        verifier -- verifier recieved from authorization
        request_token -- string of a oauth token or a tuple or list of oauth token and secret

        Keyword Arguments:
        method_chain -- api call translated to list or tuple to access request token
        """
        method_chain = kwargs.get('method_chain',
            (('RequestAccessToken','getRequestTokenVerifier'),
            ('RequestAccessToken', 'requestAccessToken')))
        kwargs['method_chain'] = method_chain[0]

        access_verifier = self.get_token_verifier(verifier, request_token, **kwargs)
        
        kwargs['method_chain'] = method_chain[1]
        access_token = self.get_access_token(access_verifier, request_token, **kwargs)

        token = Token(access_token[0], access_token[1])
        FreelancerClient.__init__(self, self.consumer, token)

        return access_token

    def __get_api_call(self, method_chain, **kwargs):
        kwargs['raw'] = True
        fl = Freelancer(self, **kwargs)

        for method in method_chain:
            fl = getattr(fl, method)

        return fl

    def __api_call_from_chain(self, method_chain, **kwargs):
        api_call_qs, kwargs = self.__pop_from_dict('api_call_qs', kwargs, {})
        fl = self.__get_api_call(method_chain, **kwargs)
        content = fl(**api_call_qs)

        return content

    def __del_if_exists(self, name, dictionary):
        if dictionary.get(name, False):
            del dictionary[name]

        return dictionary

    def __pop_from_dict(self, name, kwargs, default=False):
        pop = kwargs.get(name, default)
        kwargs = self.__del_if_exists(name, kwargs)

        return (pop, kwargs)

    def __oauth_tuple_from_qs(self, raw):
        qs = dict(urlparse.parse_qsl(raw))
        try:
            tup = (qs['oauth_token'], qs['oauth_token_secret'])
            return tup
        except KeyError:
            raise FreelancerOauthError(raw)

    def __oauth_verifier_from_qs(self, raw):
        qs = dict(urlparse.parse_qsl(raw))
        try:
            verifier = qs['verifier']
            return verifier
        except KeyError:
            raise FreelancerOauthError(raw)

    def __is_valid_token(self, token):
        if not token or token == None:
            raise ValueError('Invalid token, expecting a single token a tuple or list of 2')

        if not (isinstance(token, tuple) or isinstance(token, list)):
            token = (token, '')

        if len(token) > 2 or len(token) < 1:
            raise ValueError('Invalid token, expecting a single token a tuple or list of 2')
        elif len(token) == 1:
            token = (token[0], '')

        return token

def get_authorize_url(consumer, callback='oob', app_url='http://www.freelancer.com/users/api-token/auth.php', **kwargs):
    """
    Returns authorization url for an application

    Arguments:
    consumer -- a tuple or list of a consumer secret and key
    callback -- callback url to pass to freelancer.com
    app_url -- base url to use for authorization

    Keyword Arguments:
    Are all passed to FreelancerMethod.__call__()
    """
    flo = FreelancerOauth(consumer)

    kwargs['oauth_callback'] = callback
    request_token = flo.get_request_token(**kwargs)

    return flo.get_authorize_url(request_token, app_url)

def get_access_token(consumer, request_token, verifier, **kwargs):
    """
    Returns a tuple of access tokens for a user

    Arguments:
    consumer -- a tuple or list of a consumer secret and key
    request_token -- string of a oauth token or a tuple or list of oauth token and secret
    verifier -- verifier recieved from authorization

    Keyword Arguments:
    Are all passed to FreelancerMethod.__call__()
    """
    flo = FreelancerOauth(consumer)

    return flo.upgrade_to_access_token(verifier, request_token, **kwargs)
