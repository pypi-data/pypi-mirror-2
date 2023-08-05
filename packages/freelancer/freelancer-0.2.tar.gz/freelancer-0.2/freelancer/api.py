from exceptions import Exception
from urllib import urlencode
from response import *

class FreelancerError(Exception):
    """Exception raised during initialization errors of FreelancerMethod"""
    pass

class FreelancerMethod(object):

    def __init__(self, client, domain='api.freelancer.com', uri='', *args, **kwargs):
        if not hasattr(client, 'request'):
            raise FreelancerError('Incompatiable client passed')

        self.client = client
        self.domain = domain
        self.uri = uri
        self.protocol = kwargs.get('protocol', 'http')
        self.raw = kwargs.get('raw', False)
        self.format = kwargs.get('format', 'json')
        self.response = kwargs.get('response', FreelancerJsonResponse)

        if not hasattr(self.response, 'formats'):
            raise FreelancerError('Response handlers need to specify a formats attribute')

    def __getattr__(self, name):
        try:
            return object.__getattr__(self, name)
        except AttributeError:
            uri = self.uri + '/' + name if self.uri else name
            kwargs = {
                'format': self.format,
                'protocol': self.protocol,
                'raw': self.raw,
                'response': self.response
            }
            return FreelancerMethod(self.client, self.domain, uri, **kwargs)

    def __call__(self, *args, **kwargs):

        if not len(kwargs) and len(args) == 1 and isinstance(args[0], dict):
            kwargs = args[0]
            
        method = kwargs.get('method', 'GET')
        if kwargs.get('method', False):
            del kwargs['method']
            
        qs = urlencode(kwargs)
        url = "%s://%s/%s.%s?%s" % (self.protocol, self.domain, self.uri, self.format, qs)

        resp, content = self.client.request(url, method)

        if not self.format in self.response.formats or self.raw:
            return content
        else:
            return self.response(content, resp=resp, uri=self.uri, format=self.format, query=kwargs)

class Freelancer(FreelancerMethod):
    """
    python-freelancer is a flexible and simple Python wrapper for the
    Freelancer.com API targeted at the minimalist within us all.

    Make API calls to freelancer.com by accessing attributes of this class. By
    default, returns dicts and lists decoded from json. Expandable by subclassing
    freelancer.response.FreelancerResponse.

    All API methods available at http://developer.freelancer.com/API can be
    accessed in the same manner as the examples below.

    Examples:

        freelancer = Freelancer(FreelancerClient(consumer_keys, token))

        # Search projects
        freelancer.Project.searchProjects()

        # Get current user account details
        freelancer.Profile.getAccountDetails()

        # API call parameters are passed either as keyword arguments or a
        # dictionary.
        # As kwargs:
        freelancer.Project.searchProjects(status='Open', count=3, bugetmin='Any')

        # As a dictionary:
        params = {
            'status': 'Open',
            'count': 3,
            'bugetmin': 'Any'
        }
        freelancer.Project.searchProjects(params)

        # If you need to POST your call, add it as a parameter via 'method'
        freelancer.Project.searchProjects(status='Open', method='POST')
    """
    def __init__(self, client, domain='api.freelancer.com', uri='', *args, **kwargs):
        """
        Creates a new interface to the freelancer.com api

        Arguments:
        client -- An initialized instance of FreelancerClient or FreelancerOauth
        domain -- domain to where api calls should be made (default api.freelancer.com)
        uri -- base uri for request

        Keyword arguments:
        protocol -- protocol for request (default http)
        format -- format of request, only json and xml are available (default json)
        raw -- bool flag to skip decoding response (default false)
        response -- object that handles decoding and returning response (default FreelancerJsonResponse)
        """
        FreelancerMethod.__init__(self, client, domain, uri, *args, **kwargs)