from copy import copy
from datetime import date, timedelta
import unittest

from nose.tools import raises, assert_raises
from testconfig import config

from sharpy.client import Client
from sharpy.exceptions import AccessDenied, BadRequest, NotFound, CheddarFailure, NaughtyGateway, UnprocessableEntity, PreconditionFailed

from testing_tools.decorators import clear_users

class ClientTests(unittest.TestCase):
    client_defaults =  {
        'username': config['cheddar']['username'],
        'password': config['cheddar']['password'],
        'product_code': config['cheddar']['product_code'],
    }
    
    def get_client(self, **kwargs):
        client_kwargs = copy(self.client_defaults)
        client_kwargs.update(kwargs)
        
        c = Client(**client_kwargs)
        
        return c
    
    def try_client(self, **kwargs):
        args = copy(self.client_defaults)
        args.update(kwargs)
        client = self.get_client(**kwargs)
        
        self.assertEquals(args['username'], client.username)
        self.assertEquals(self.client_defaults['password'] ,client.password)
        self.assertEquals(self.client_defaults['product_code'], client.product_code)
        if 'endpoint' in args.keys():
            self.assertEquals(args['endpoint'], client.endpoint)
        else:
            self.assertEquals(client.default_endpoint, client.endpoint)
    
    def test_basic_init(self):
        self.try_client()
        
    def test_custom_endpoint_init(self):
        self.try_client(endpoint = 'http://cheddar-test.saaspire.com')
        
    
    def try_url_build(self, path, params=None):
        c = self.get_client()
        expected = u'%s/%s/productCode/%s' % (
            c.default_endpoint,
            path,
            c.product_code,
        )
        if params:
            for key, value in params.items():
                expected = u'%s/%s/%s' % (expected, key, value)

        result = c.build_url(path=path, params=params)

        self.assertEquals(expected, result)
        
    def test_basic_build_url(self):
        path = 'users'
        self.try_url_build(path)
        
    
    def test_single_param_build_url(self):
        path = 'users'
        params = {'key': 'value'}
        self.try_url_build(path, params)
        
    def test_multi_param_build_url(self):
        path = 'users'
        params = {'key1': 'value1', 'key2': 'value2'}
        self.try_url_build(path, params)
        
    def test_make_request(self):
        path = 'plans/get'
        client = self.get_client()
        response = client.make_request(path)
        
        self.assertEquals(response.status, 200)
    
    @raises(AccessDenied)
    def test_make_request_access_denied(self):
        path = 'plans/get'
        bad_username = self.client_defaults['username'] + '_bad'
        client = self.get_client(username=bad_username)
        client.make_request(path)
        
    @raises(BadRequest)
    def test_make_request_bad_request(self):
        path = 'plans'
        client = self.get_client()
        client.make_request(path)
        
    @raises(NotFound)
    def test_make_request_not_found(self):
        path = 'things-which-dont-exist'
        client = self.get_client()
        client.make_request(path)
        
    @clear_users
    def test_post_request(self):
        path = 'customers/new'
        data = {
            'code': 'post_test',
            'firstName': 'post',
            'lastName': 'test',
            'email': 'garbage@saaspire.com',
            'subscription[planCode]': 'FREE_MONTHLY',
        }
        client = self.get_client()
        client.make_request(path, data=data)
    

    def generate_error_response(self, auxcode, **overrides):
        '''
        Creates a request to cheddar which should return an error
        with the provided aux code.  See the urls below for details
        on simulating errors and aux codes:
        http://support.cheddargetter.com/kb/api-8/error-simulation
        http://support.cheddargetter.com/kb/api-8/error-handling
        '''
        path = 'customers/new'
        expiration = date.today() + timedelta(days=180)
        
        data = {
            'code': 'post_test',
            'firstName': 'post',
            'lastName': 'test',
            'email': 'garbage@saaspire.com',
            'subscription[planCode]': 'PAID_MONTHLY',
            'subscription[ccNumber]': '4111111111111111',
            'subscription[ccExpiration]': expiration.strftime('%m/%Y'),
            'subscription[ccCardCode]': '123',
            'subscription[ccFirstName]': 'post',
            'subscription[ccLastName]': 'test',
            'subscription[ccZip]': '0%d' % auxcode,
        }
        data.update(overrides)
        
        client = self.get_client()
        client.make_request(path, data=data)
    
    def assertCheddarError(self, auxcode, expected_exception):
        assert_raises(
            expected_exception,
            self.generate_error_response,
            auxcode=auxcode,
        )
        
    def assertCheddarErrorForAuxCodes(self, auxcodes, expected_exception):
        for auxcode in auxcodes:
            self.assertCheddarError(auxcode, expected_exception)
            
    @clear_users
    def test_cheddar_500s(self):
        auxcodes = (1000, 1002, 1003)
        expected_exception = CheddarFailure
        self.assertCheddarErrorForAuxCodes(auxcodes, expected_exception)
        
    @clear_users
    def test_cheddar_400(self):
        '''
        The cheddar docs at
        http://support.cheddargetter.com/kb/api-8/error-handling
        say that this aux code should return a 502 but in practice 
        the API returns a 400.  Not sure if this is a bug or typo in the
        docs but for now we're assuming the API is correct.
        '''
        self.assertCheddarError(auxcode=1001, expected_exception=BadRequest)
    
    @clear_users
    def test_cheddar_401s(self):
        auxcodes = (2000, 2001, 2002, 2003)
        expected_exception = AccessDenied
        self.assertCheddarErrorForAuxCodes(auxcodes, expected_exception)
            
    @clear_users
    def test_cheddar_502s(self):
        auxcodes = (3000, 4000)
        expected_exception = NaughtyGateway
        self.assertCheddarErrorForAuxCodes(auxcodes, expected_exception)
    
    @clear_users
    def test_cheddar_422s(self):
        auxcodes = (5000, 5001, 5002, 5003, 6000, 6001, 6002, 7000)
        expected_exception = UnprocessableEntity
        self.assertCheddarErrorForAuxCodes(auxcodes, expected_exception)
        
    @clear_users
    @raises(PreconditionFailed)
    def test_cheddar_412s(self):
        self.generate_error_response(auxcode=2345, firstName='')