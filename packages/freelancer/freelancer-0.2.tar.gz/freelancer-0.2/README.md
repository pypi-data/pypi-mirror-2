# Overview

python-freelancer is a flexible and simple Python wrapper for the Freelancer.com API targeted at the minimalist within us all. This means you get:

* A minimalist, yet full, design: less than ~300 lines of code across the api, client, oauth, and response packages
* Simplified Oauth exchange through the <code>FreelancerOauth</code> worker class and it's wrapper functions
* Full access to the Freelancer.com API through <code>Freelancer</code> whose methods are dynamically bound to Freelancer.com's RESTful API.
* Customized response handlers without untidying your code through subclassing <code>FreelancerResponse</code>

python-freelancer requires [oauth2](http://github.com/simplegeo/python-oauth2/) and was partly inspired by [Mike Verdone's Python Twitter Tools](http://github.com/sixohsix/twitter).

# Obtaining access tokens through FreelancerOauth

Directly interacting with the <code>FreelancerOauth</code> worker is one way you can obtain a user's access keys.

    from freelancer.oauth import FreelancerOauth

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

<code>access_token</code> is a tuple of a oauth token and token secret that can be saved to your database or written to a file for later use.

# Obtaining access tokens (the easy way) through freelancer.oauth.get_authorize_url and freelancer.oauth.get_access_token

freelancer.oauth has two wrapper functions for the FreelancerOauth class to simplify things a little. These functions use <code>FreelancerOauth</code> in nearly the same way as the <code>FreelancerOauth</code>.

    from freelancer.oauth import from freelancer.oauth import get_authorize_url, get_access_token

    # Define you consumer key tuple or list just like when using FreelancerOauth
    consumer = ('your key', 'your secret')

    # Next we'll retrieve the url needed to authorize the application. This step
    # generates the request token for you. You need to pass a consumer tuple or
    # list and a callback url. All keyword arguments are appropriately passed if
    # given (mainly applicable to 'domain')
    redirect_to = get_authorize_url(consumer, 'http://example.com/authorized/?')

    ...

    # After the user authorizes the app and is passed back to the callback url,
    # you can retrieve the access token. Just like when directly interacting with
    # the FreelancerOauth worker, you need to pass it the request token and verifier.
    request_token = 'whatever'
    verifier = 'whatever'
    access_token = get_access_token(consumer, request_token, verifier)

<code>get_access_token</code> returns a tuple of a token and token secret just like the previous example.

# Making API calls with Freelancer

All of the API methods available through freelancer.com are available to the <code>Freelancer</code> implementation. Every method is literally mapped to the RESTful API. This means that if you wanted to access /Profile/getAccountDetails.json, you'd just need to call freelancer.Profile.getAccountDetails().

    from freelancer.client import FreelancerClient
    from freelancer.api import Freelancer

    # To use the Freelancer class, you need to initialize it with a
    # FreelancerClient worker. FreelancerClient handles the actual http requests.
    # It's initialized the same way as FreelancerOauth except it also requires
    # an access token to be passed for requests to be successful.
    consumer = ('your key', 'your secret')
    access_token = ('pudding', 'pie')
    client = FreelancerClient(consumer, token)
    freelancer = Freelancer(client)

    # After initialization, you're set and can start making calls. This will
    # fetch the current user's account details as decoded json (the default
    # response format for Freelancer)
    profile = freelancer.Profile.getAccountDetails()

    # FreelancerOauth subclasses FreelancerClient, and can also be used to
    # initialize Freelancer
    client = FreelancerOauth(consumer, token)
    freelancer = Freelancer(client)

    # Actually, any object with the 'request' attribute can be passed to
    # Freelancer. Though, if the object can't properly make an oauth class, it
    # won't work. See oauth2.Client.request to see how the base class is implemented.
    class ExampleRequestClass(FreelancerClient):
        pass

    client = ExampleRequestClass(consumer, token)
    freelancer = Freelancer(client)

    # API call parameters can be passed in two ways. The first is through
    # keyword arguments:
    search_results = freelancer.Project.searchProjects(status='Open', count=3, bugetmin='Any')

    # The second method is through a dictionary passed as the first argument:
    params = {
        'status': 'Open',
        'count': 3,
        'bugetmin': 'Any'
    }
    search_results = freelancer.Project.searchProjects(params)

    # Know that mixing and matching keyword arguments and a single dictionary of
    # arguments will not have the desired effect. Use one or the other.

    # If you need to POST your request, you can by passing 'method' to your call.
    search_results = freelancer.Project.searchProjects(status='Open', count=3, bugetmin='Any', method='POST')

    # You can visit the [freelancer.com developer wiki](http://developer.freelancer.com/API)
    # for a listing of available methods.

# Creating your own response handlers through FreelancerResponse

The default format for requests from the freelancer.com API is json and that's decoded in Python via the json module into a series of dictionaries and lists. That's not always ideal, and you can easily parse the response into whatever you want within <code>Freelancer</code>. You can do this through subclassing <code>FreelancerResponse</code> in <code>freelancer.response</code> and initializing <code>Freelancer</code> with it.

    import json
    from freelancer.response import FreelancerResponse
    from freelancer.api import Freelancer

    # First, let's create our new response handler. It should subclass
    # FreelancerResponse, but technically doesn't need to.
    class MyCustomDecoderRing(FreelancerResponse):

        # Specifying which formats a response handler can parse is required.
        # If a call is made to Freelancer in XML and you don't indicate that
        # you can handle XML, the raw response will just be returned. In this case,
        # we'll just use json.
        formats = ('json')

        # FreelancerResponse uses __new__ as its interface within Freelancer.
        # This is where you receive and decode the content from the API call.
        # __new__ is always passed the content as the first argument, and then a
        # series of keyword arguments for auxiliary information, like resp
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

# Using the Freelancer API explorer interactive shell

python-freelancer comes with an API explorer in the form of an interactive shell.
It can be accessed through the freelancer command from terminal. This is a full-
featured shell, allowing for mock requests, Oauth exchanges, and API calls.

Usage is <code>freelancer [token_file]</code>

When using the shell with no token file available, you should run
oauth.getToken() first if you plan on using the api module.

    freelancer>> oauth.getToken()
    ...
    freelancer>> oauth.save({'file':'/full/path/to/token/file/freelancer.token'})
    freelancer>> api.Profile.getAccountDetails()

After saving the token file, you can load it for use from within the shell.

    freelancer>> oauth.({'file':'/full/path/to/token/file/freelancer.token'})
    freelancer>> api.Profile.getAccountDetails()

If you don't want to make actual API calls, you can alternatively use the mock
module and not the oauth and api modules

    freelancer>> mock.Profile.getAccountDetails()

Calling any module's help() function will print out its help text

    freelancer>> oauth.help()

Use the admin.exit() method to leave the shell

    freelancer>> admin.exit()

# Example CLI script to test python-freelancer and obtain your access tokens

    # First import what we need
    from freelancer.oauth import get_authorize_url, get_access_token
    from freelancer.api import Freelancer

    # Set our consumer key tuple and pass it and a callback to get_authorize_url
    consumer = ('your key', 'your secret')

    print "Visit this url to authorize this application:"
    print get_authorize_url(consumer, 'oob')
    print

    # Now you input the request token and verifier, and we'll fetch the access
    # token for you
    oauth_token = raw_input('What is your oauth token? ')
    verifier = raw_input('What is your verifier? ')
    access_token = get_access_token(consumer, oauth_token, verifier)

    print
    print "You can now use these access tokens to access the API:"
    print "     oauth_token: %s" % access_token[0]
    print "     oauth_token_secret: %s" % access_token[1]
    print
    print "Performing Profile/getAccountDetails.json to test your access key..."

    # Now let's try to do a request to make sure everything actually worked.
    fl = Freelancer(FreelancerClient(consumer, access_token))
    resp = fl.Profile.getAccountDetails()

    if resp.get('json-result', False):
        print "Success! YEAH!"
    else:
        print "failure. :("
        print
        print "Here's a full dump of the response: "
        print resp