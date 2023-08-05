try:
    import json
except:
    import simplejson as json

from exceptions import Exception

class FreelancerResponseError(Exception):
    pass

class FreelancerResponse(object):
    """
    Base class for Freelancer API response decoders. Requires the 'formats'
    attribute and __new__ method to be defined. formats is a tuple of strings
    describing the formats the class can handle.

    Example:
    
        # First, let's create our new response handler. It should subclass
        # FreelancerResponse, but technically doesn't need to.
        class MyCustomDecoderRing(FreelancerResponse):

            # Specifying which formats a response handler can parse is required.
            # If a call is made to Freelancer in XML and you don't indicate that
            # you can handle XML, the raw response will just be returned. In this case,
            # we'll just use json.
            formats = ('json')

            # FreelancerResponse uses __new__ as its interface within Freelancer.
            # This is where you recieve and decode the content from the API call.
            # __new__ is always passed the content as the first argument, and then a
            # series of keyword arguments for auxilary information, like resp
            # (i.e., http status) as a dictionary, uri as a string, format as a
            # string, and query as a dictionary.
            def __new__(self, content, *args, **kwargs):
                # Now we can parse the raw response from the api however we want
                parsed = some_function(content)

                return content

        # With our new response handler ready (yeah, that's all it takes), we can put
        # it into action by telling Freelancer to use it.
        consumer = ('your key', 'your secret')
        access_token = ('pudding', 'pie')
        client = FreelancerClient(consumer, token)
        freelancer = Freelancer(client, response=MyCustomDecoderRing)

        # And that's all it takes. Now, your calls will be parsed how you want them
        # to be.
        search_results = freelancer.Project.searchProjects()
    """

    formats = ()

    def __new__(self, content, *args, **kwargs):
        return content

class FreelancerJsonResponse(FreelancerResponse):

    formats = ('json',)

    def __new__(self, content, *args, **kwargs):
        try:
            return json.loads(content)
        except ValueError:
            raise FreelancerResponseError('No json to decode')