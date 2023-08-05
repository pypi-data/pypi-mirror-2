import unittest

from freelancer.api import *
from freelancer.oauth import *
from freelancer.client import *
from freelancer.response import *

class TestFreelancerClient(unittest.TestCase):

    def setUp(self):
        self.freelancer_client = FreelancerClient(('pudding', 'pie'), ('pudding', 'pie'))

    def test_basic(self):
        self.assertRaises(ValueError, lambda: FreelancerClient(('pudding')))
        self.assertRaises(ValueError, lambda: FreelancerClient(('pudding', 'pie'), ('pudding')))
        self.assertRaises(ValueError, lambda: FreelancerClient(['pudding', 'pie'], Consumer('pudding', 'pie')))
        self.assertRaises(ValueError, lambda: FreelancerClient(['pudding'], ['pudding', 'pie']))
    
    def test_init(self):
        self.assertTrue(isinstance(self.freelancer_client.consumer, Consumer))
        self.assertTrue(isinstance(self.freelancer_client.token, Token))

class TestFreelancerOauth(unittest.TestCase):

    def setUp(self):
        self.consumer = ('b8720f555b3dd8ac538fd86ab67c9d4267373af5', '798dec89ac683b271e4a7aae56d41d9b7e019913')
        self.token = ('pudding', 'pie')
        self.domain = 'api.sandbox.freelancer.com'
        self.verifier = 'pudding pie'
        self.bad_consumer = ('pudding', 'pie')
        self.client = FreelancerOauth(self.consumer)
        self.app_url = 'http://www.sandbox.freelancer.com/users/api-token/auth.php'

    def test_get_request_token(self):
        self.assertRaises(FreelancerOauthError, lambda: FreelancerOauth(self.bad_consumer).get_request_token(domain=self.domain))
        self.assertEqual(self.client.get_request_token(domain=self.domain), self.client.request_token)
        self.assertTrue(isinstance(self.client.get_request_token(domain=self.domain), tuple))

    def test_get_authorize_url(self):
        self.assertRaises(ValueError, lambda: FreelancerOauth(self.bad_consumer).get_authorize_url())
        self.assertRaises(ValueError, lambda: FreelancerOauth(self.consumer).get_authorize_url(('pudding', 'pie', 'cake')))
        self.assertEqual(self.client.get_authorize_url(self.token, self.app_url), "%s?oauth_token=%s" % (self.app_url, self.token[0]))
        self.assertEqual(self.client.get_authorize_url(self.token, 'http://example.com/'), "%s?oauth_token=%s" % ('http://example.com/', self.token[0]))

        self.client = FreelancerOauth(self.consumer)
        request_token = self.client.get_request_token(domain=self.domain)
        self.assertEqual(self.client.get_authorize_url(request_token, self.app_url), "%s?oauth_token=%s" % (self.app_url, request_token[0]))
        self.assertEqual(self.client.request_token[0], request_token[0])

    def test_get_token_verifier(self):
        self.assertRaises(ValueError, lambda: FreelancerOauth(self.consumer).get_token_verifier('', domain=self.domain))
        self.assertRaises(ValueError, lambda: FreelancerOauth(self.consumer).get_token_verifier(self.verifier, domain=self.domain))
        self.assertRaises(ValueError, lambda: FreelancerOauth(self.consumer).get_token_verifier(['pudding'], domain=self.domain))

        self.assertRaises(FreelancerOauthError, lambda: FreelancerOauth(self.consumer).get_token_verifier(self.verifier, ('pie'), domain=self.domain))
        self.assertRaises(FreelancerOauthError, lambda: FreelancerOauth(self.consumer).get_token_verifier(self.verifier, 'pie', domain=self.domain))

        self.client = FreelancerOauth(self.consumer)
        request_token = self.client.get_request_token(domain=self.domain)
        self.assertRaises(FreelancerOauthError, lambda: self.client.get_token_verifier(self.verifier, domain=self.domain))
        self.assertRaises(FreelancerOauthError, lambda: self.client.get_token_verifier(self.verifier, self.token, domain=self.domain))

    def test_get_access_token(self):
        self.assertRaises(ValueError, lambda: FreelancerOauth(self.consumer).get_access_token('', domain=self.domain))
        self.assertRaises(ValueError, lambda: FreelancerOauth(self.consumer).get_access_token(self.verifier, domain=self.domain))
        self.assertRaises(ValueError, lambda: FreelancerOauth(self.consumer).get_access_token(['pudding'], domain=self.domain))

        self.assertRaises(FreelancerOauthError, lambda: FreelancerOauth(self.consumer).get_token_verifier(self.verifier, ('pie'), domain=self.domain))
        self.assertRaises(FreelancerOauthError, lambda: FreelancerOauth(self.consumer).get_token_verifier(self.verifier, 'pie', domain=self.domain))

        self.client = FreelancerOauth(self.consumer)
        request_token = self.client.get_request_token(domain=self.domain)
        self.assertRaises(FreelancerOauthError, lambda: self.client.get_access_token(self.verifier, domain=self.domain))
        self.assertRaises(FreelancerOauthError, lambda: self.client.get_access_token(self.verifier, self.token, domain=self.domain))

class TestFreelancerMethod(unittest.TestCase):
    
    def setUp(self):
        self.client = FreelancerOauth(('pudding', 'pie'))
        self.domain = 'example.com'
        self.uri = 'api'
        self.format = 'json'
        self.protocol = 'https'
        self.raw = True
        self.freelancer = FreelancerMethod(self.client, self.domain, self.uri, format=self.format, protocol=self.protocol, raw=self.raw)

    def test_basic(self):
        self.assertRaises(FreelancerError, lambda: FreelancerMethod({}))
        self.assertRaises(FreelancerError, lambda: FreelancerMethod(self.client, response=self.client))

    def test_init(self):
        self.assertEqual(self.freelancer.client, self.client)
        self.assertEqual(self.freelancer.domain, self.domain)
        self.assertEqual(self.freelancer.uri, self.uri)
        self.assertEqual(self.freelancer.format, self.format)
        self.assertEqual(self.freelancer.protocol, self.protocol)
        self.assertEqual(self.freelancer.raw, self.raw)

    def test_getattr(self):
        self.assertTrue(isinstance(self.freelancer.Project, FreelancerMethod))
        self.assertTrue(isinstance(self.freelancer.Project.getProjectFees, FreelancerMethod))
        self.assertTrue(not isinstance(self.freelancer.domain, FreelancerMethod))

    def test_method_inherit(self):
        self.assertEqual(self.freelancer.client, self.freelancer.Project.client)
        self.assertEqual(self.freelancer.domain, self.freelancer.Project.domain)
        self.assertEqual(self.freelancer.format, self.freelancer.Project.format)
        self.assertEqual(self.freelancer.protocol, self.freelancer.Project.protocol)
        self.assertEqual(self.freelancer.raw, self.freelancer.Project.raw)
        self.assertNotEqual(self.freelancer.uri, self.freelancer.Project.uri)
        self.assertTrue(self.freelancer.Project.uri < self.freelancer.Project.getProjectFees.uri)

    def test_uri_building(self):
        self.assertEqual(self.freelancer.uri, self.uri)
        self.assertEqual(self.freelancer.Project.uri, "%s/%s" % (self.uri, 'Project'))
        self.assertEqual(self.freelancer.Project.getProjectFees.uri, "%s/%s/%s" % (self.uri, 'Project', 'getProjectFees'))        

if __name__ == "__main__":
    unittest.main()