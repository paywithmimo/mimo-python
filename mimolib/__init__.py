#!/usr/bin/env python
# -*- coding: utf-8 -*-

####################################################################
 # MIMO REST API Library for Python
 #
 # MIT LICENSE
 #
 # Permission is hereby granted, free of charge, to any person obtaining
 # a copy of this software and associated documentation files (the
 # "Software"), to deal in the Software without restriction, including
 # without limitation the rights to use, copy, modify, merge, publish,
 # distribute, sublicense, and/or sell copies of the Software, and to
 # permit persons to whom the Software is furnished to do so, subject to
 # the following conditions:
 #
 # The above copyright notice and this permission notice shall be
 # included in all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 # EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 # MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 # NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 # LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 # OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 # WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 # 
 # @package   MIMO
 # @copyright Copyright (c) 2012 Mimo Inc. (http://www.mimo.com.ng)
 # @license   http://opensource.org/licenses/MIT MIT
 # @version   1.2.6
 # @link      http://www.mimo.com.ng
 ##########################################################################
'''

mimo-python: python SDK for Mimo's API
======================================

mimo-python is a simple python module to support
Mimo's API with OAuth 2.0 standard

'''
import requests
from requests.auth import HTTPBasicAuth

__title__ = 'MimoRestClient'
__version__ = '1.0.0'



import json
import urllib
from urllib import urlencode

class MimoRestClient:
    """MimoRestClient class used to support various MIMO Payment API.

    In order to use this class MIMO should have created client_id and client_secret key. This class
    provided various method supported by the MIMO Payment Gateway.It uses JSON API to parse the API.

    Attributes:
        self: Current class.
        client_id: An string client id provided by MIMO Payment Gateway.
        client_secret: An string client secret key provided by MIMO Payment Gateway.
        client_url: An string MIMO Payment Gateway url.
    """
    def __init__(self, client_id, client_secret, client_url, 
                 authentication_url="/oauth/v2/authenticate",
                 token_url="/oauth/v2/token", 
                 search_url="/partner/user/card_id",
                 transfer_url="/partner/transfers", 
                 refund_url="/partner/refunds",
                 void_endpoint_url="/partner/transfers/void",
                 encoding="utf-8", **kwargs):
        """Inits SampleClass with client_id,client_secret,client_url and various 
           URL used for MIMO API."""
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_url = client_url
        self.authentication_url = client_url + authentication_url
        self.token_url = client_url + token_url
        self.search_url = client_url + search_url
        self.transfer_url = client_url + transfer_url
        self.refund_url = client_url+ refund_url 
        self.void_endpoint_url = client_url+ void_endpoint_url
        self.headers = None
        self.auth_params = None
        self.json_request = False
        self.encoding = encoding
        if kwargs.get("json_request", False):
            self.json_request = True
            self.headers = {'content-type': 'application/json'}
        if kwargs.get("auth_params", False):
            self.auth_params = kwargs["auth_params"] # must be like-("mimo", "mimo")
        #self.session = requests.session(auth=self.auth_params)
        self.session = requests.session()
        self.session.auth = self.auth_params

    def get_session_cookies_dict(self):
        """Performs operation of reading the session cookies."""
        return requests.utils.dict_from_cookiejar(self.session.cookies)

    def set_cookies(self, cookie_dict):
        """Performs operation of setting cookie data."""
        for k,v in cookie_dict.iteritems():
            if not isinstance(v, str):
                cookie_dict[k] =  str(v)
        requests.utils.add_dict_to_cookiejar(self.session.cookies,
                                             cookie_dict)
    
    def encode_url(self, url):
        """Performs operation of encoding the URL and escape characters."""
        return urllib.quote_plus(url)

    def get_url(self, params, url):
        """Performs operation to get URL."""
        params = urlencode(params)
        url = "%(url)s?"%{'url' : url} + params
        return url

    def POST_request(self, url, params, **kwargs):
        """Performs operation of posting the request to the server in JSON format.
            Args:
                self: Current self class
                url: URL where request needs to be posted
                params: Request parameters to be posted.
        
            Returns:
                JSON response received from the server
        
            Raises:
                Exception: An error occurred while posting request or parsing response.
        """
        kwargs = kwargs and kwargs or {}
        self.headers.update(kwargs.get("headers", {}))
        try:
            if self.json_request:
                data = json.dumps(params, encoding=self.encoding)
            else:
                data = params

            response = self.session.post(url, data=data, headers=self.headers)
	    return self.parse_response(response)
        except requests.exceptions as e:
            print ("Request Exception occurred :",e)
            raise Exception(e)

    def GET_request(self, url, **kwargs):
        """Performs operation of HTTP GET on the URL provided.
            Args:
                self: Current self class
                url: URL where request needs to be posted
           
            Returns:
                JSON response received from the server
        
            Raises:
                Exception: An error occurred while posting request or parsing response.
        """
        try:
            response = self.session.get(url)
	    return self.parse_response(response)
        except requests.exceptions as e:
            print ("Request Exception occure :",e)
            raise Exception(e)

    def parse_response(self, resp):
        """Performs operation of parsing the HTTP Response.
            Args:
                self: Current self class
                resp: HTTP Response object
        
            Returns:
                JSON content received from the server
        """
        content = {}
        if resp.content:
            if isinstance(resp.content, basestring):
                try:
                    content = json.loads(resp.content)
                except ValueError:
                    content = resp.content
	    else:
		content = resp.content
        return content    

    def get_code_url(self, **kwargs):
        """Performs operation of constructing the Authentication URL for MIMO Payment Gateway.
            Args:
                self: Current self class
        
            Returns:
                String of Authentication URL for MIMO Payment Gateway
        """
        data = {'client_id': self.client_id,
                'response_type': "code"}
        data.update(kwargs)
        params = '?' + urlencode(data)
        return self.authentication_url + params

    def request_oauth_token(self, code, **kwargs):
        """Performs operation doing OATH with MIMO Payment Gateway. It also sets the cookies.
            Args:
                self: Current self class
                code: Authentication code.
           
            Returns:
                String HTTP response received from the server
        
            Raises:
                NameError: If url or redirect_url varaible missing in kwargs input.
                Exception: An error occurred while posting request or parsing response.
        """
        if 'params' not in kwargs:
            raise NameError('params is missing in arguments (kwargs as dict)')
#        if "code" not in kwargs["params"]:
#            raise NameError('code is missing in arguments (kwargs as dict)')
        if "redirect_uri" in kwargs["params"] or "url" in kwargs["params"]:
            pass
        else:
            raise NameError('Either redirect_uri or url is missing in arguments (kwargs as dict)')
        kwargs["params"].update(client_id = self.client_id,
                               client_secret = self.client_secret,
                               grant_type = "authorization_code",
                               code = code)
        response_content = self.POST_request(self.token_url, kwargs["params"])
        self.set_cookies(response_content)
        return response_content


    def search(self, **kwargs):
        """Performs operation doing search by username,email,phone and account number with MIMO Payment Gateway.
            Args:
                self: Current self class
          
            Returns:
                String JSON response received from the server
        
            Raises:
                ValueError: If variables in input are empty.
                Exception: An error occurred while posting request or parsing response.
        """
        kwargs = kwargs and kwargs or {}
        if kwargs.keys() <= 1:
            raise ValueError('search value is missing in arguments (kwargs as dict)')

        if not kwargs.get("access_token", False):
            kwargs.update({'access_token':self.get_session_cookies_dict().get("access_token", False)})
        url = self.get_url(kwargs, self.search_url)
        return self.GET_request(url)


    def transfer_funds_endpoint(self, amount, notes, **kwargs):
        """Performs operation doing transfer of funds with MIMO Payment Gateway.
            Args:
                self: Current self class
                amount: Double amount to be transferred.
                notes: String memo notes to be attached with this transfer
          
            Returns:
                String JSON response received from the server
        
            Raises:
                Exception: An error occurred while posting request or parsing response.
        """
        kwargs = kwargs and kwargs or {}
        if "access_token" not in kwargs:
            kwargs.update({'access_token':self.get_session_cookies_dict().get("access_token", False)})
	
        kwargs.update({"amount":amount, "notes":notes})
	response_content = self.POST_request(self.transfer_url, kwargs)
	self.set_cookies({"transaction_id":response_content.get("transaction_id")})
        return response_content


    def refund_endpoint(self, amount, notes, transaction_id=False, **kwargs):
        """Performs operation doing refund of funds with MIMO Payment Gateway.
            Args:
                self: Current self class
                amount: Double amount to be transferred.
                notes: String memo notes to be attached with this transfer
          
            Returns:
                String JSON response received from the server
        
            Raises:
                Exception: An error occurred while posting request or parsing response.
        """
        kwargs = kwargs and kwargs or {}
        if "access_token" not in kwargs:
            kwargs.update({'access_token':self.get_session_cookies_dict().get("access_token", False)})

        kwargs.update({
                                 "amount":amount,
                                 "transaction_id":transaction_id and transaction_id or self.get_session_cookies_dict().get("transaction_id", False),
                                 "notes":notes
                                 })
        response_content = self.POST_request(self.refund_url, kwargs)
        self.set_cookies({"transaction_id":response_content.get("transaction_id")})
        return response_content

    def transfer_voidfunds_endpoint(self, transaction_id=False, **kwargs):
        """Performs operation doing voiding of transfer funds transaction which has not yet being completed with MIMO Payment Gateway.
            Args:
                self: Current self class
                transaction_id: Integer transaction id to be voided.
          
            Returns:
                String JSON response received from the server
        
            Raises:
                Exception: An error occurred while posting request or parsing response.
        """
        kwargs = kwargs and kwargs or {}
        if "access_token" not in kwargs:
            kwargs.update({'access_token':self.get_session_cookies_dict().get("access_token", False)})

        kwargs.update({"transaction_id":transaction_id and transaction_id or 	
				self.get_session_cookies_dict().get("transaction_id", False)})

        return self.POST_request(self.void_endpoint_url, kwargs)

