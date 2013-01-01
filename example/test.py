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
from mimolib import MimoRestClient


#********
#  MIMO
#********

import urllib

#Create the MimoRestClient class instance.

mimo = MimoRestClient(
    'NfXwj_-nso1NYdpZ',
    'xv-lHx9FusqgBWbEWkjDSn5x',
    'https://staging.mimo.com.ng/',
    authentication_url='oauth/v2/authenticate',
    token_url='oauth/v2/token', auth_params=("mimo", "mimo"),
    json_request=True)

#Get the MIMO Authentication URL

code_url = mimo.get_code_url(url="https://www.google.com/")
print ("Open mimo Authorized url in browser ---",code_url)

code = raw_input('Copy code from browser: ')
data = dict(url=urllib.quote_plus("https://www.google.com/"))

#Gets Authentication code from MIMO Payment Gateway .

resp = mimo.request_oauth_token(code, params=data)
print ("Mimo Access token key ===",resp)

# Search
search_resp = mimo.search_user(username="mimo-python")
print ("Search User Response ===",search_resp)

# Transfer funds
transfer_funds_resp = mimo.transfer_funds(100.00, "transfer amount")
print ("Transfer Funds Response===",transfer_funds_resp)


# Refund endpoint
refund_endpoint_resp = mimo.refund_funds(100.00, "refund amount", 12164)
print ("Refund Funds Response===",refund_endpoint_resp)

# Void funds endpoint
transfer_voidfunds_resp = mimo.void_transfer(12166)
print ("Void Transfer Funds Response===",transfer_voidfunds_resp)



