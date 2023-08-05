from oauth2 import Consumer, Token, Client

class FreelancerClient(Client):
    """
    Creates a new worker to make signed Oauth requests to freelancer.com api.
    Requires a tuple or list of a consumer key and consumer secret, and a
    tuple or list of a token and token secret.

    Examples:

        # To initialize, pass your consumer key and secret and token and token
        # secret
        consumer = ('your key', 'your secret')
        token = ('pudding', 'pie')
        client = FreelancerClient(consumer, token)

        # This client can then be passed to Freelancer to make API calls
        freelancer = Freelancer(client)
        search_results = freelancer.Project.searchProjects()
    """

    def __init__(self, consumer, token=None):
        """
        Creates a new worker to make signed Oauth requests to freelancer.com api

        Arguments:
        consumer -- a tuple or list of a consumer secret and key
        token -- a tuple or list of a token and token secret
        """
        if not isinstance(consumer, Consumer) and self.__is_valid_token(consumer):
            consumer = Consumer(consumer[0], consumer[1])

        if token and not isinstance(token, Token) and self.__is_valid_token(token):
            token = Token(token[0], token[1])

        Client.__init__(self, consumer, token)

    def __is_valid_token(self, token):

        if (isinstance(token, tuple) or isinstance(token, list)) and len(token) == 2:
            return token

        raise ValueError('Invalid token, expecting a tuple, list, or oauth2 object')