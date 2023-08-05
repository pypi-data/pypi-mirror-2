# Copyright 2009-2010 numero, theothernumber.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''
Created on 14 Apr 2010

@author: numero
'''

import sys, os
sys.path.append( os.path.join( os.getcwd(), '..' ) )
from pymongo import Connection
from pymongo.errors import ConnectionFailure, OperationFailure
from hashlib import md5

from prospero.util import check_password
import prospero.settings as settings
import prospero.enum as enum
import time

DIGEST = "digest"
PASSWORD = "password"

class SafeDigestAuthMixin(object):
    """Allows HTTP Digest auth to be applied to an arbitrary external library
        
        
    
    """
    
    def H(self, data):
        return md5(data).hexdigest()

    def KD(self, secret, data):
        return self.H(secret + ":" + data)

    def A1(self, auth_pass):
        # If 'algorithm' is "MD5" or unset, A1 is:
        # A1 = unq(username-value) ":" unq(realm-value) ":" passwd

        username = self.params["username"]
        return "%s:%s:%s" % (username, self.realm, auth_pass)

        # Not implemented: if 'algorithm' is 'MD5-Sess', A1 is:
        # A1 = H( unq(username-value) ":" unq(realm-value) ":" passwd )
        # ":" unq(nonce-value) ":" unq(cnonce-value)

    def A2(self):
        """
        If the "qop" directive's value is "auth" or is unspecified, then A2 is:
        A2 = Method ":" digest-uri-value
        Else,
        A2 = Method ":" digest-uri-value ":" H(entity-body)
        
        """
        if self.params['qop'] == 'auth' or self.params['qop'] == None or self.params['qop'] == '':
            return self.request.method + ":" + self.request.uri
        elif self.params['qop'] == 'auth-int':
            print "UNSUPPORTED 'qop' METHOD\n"
            #return self.request.method + ":" + self.request.uri + H(self.request.body)
        else:
            print "A2 GOT BAD VALUE FOR 'qop': %s\n" % self.params['qop']

    def response(self, auth_pass):
        if self.params.has_key("qop"):
            return self.KD(auth_pass,
                           self.params["nonce"]
                           + ":" + self.params["nc"]
                           + ":" + self.params["cnonce"]
                           + ":" + self.params["qop"]
                           + ":" + self.H(self.A2()))
        else:
            return self.KD(auth_pass, \
                           self.params["nonce"] + ":" + self.H(self.A2()))

    def _parseHeader(self, authheader):
        try:
            n = len("Digest ")
            authheader = authheader[n:].strip()
            items = authheader.split(", ")
            keyvalues = [i.split("=", 1) for i in items]
            keyvalues = [(k.strip(), v.strip().replace('"', '')) for k, v in keyvalues]
            self.params = dict(keyvalues)
        except:
            self.params = []

    def _createNonce(self):
        return md5("%d:%s" % (time.time(), self.realm)).hexdigest()

    def createAuthHeader(self):
        self.set_status(401)
        nonce = self._createNonce()
        self.set_header("WWW-Authenticate", "Digest algorithm=MD5 realm=%s qop=auth nonce=%s" % (self.realm, nonce))
        self.finish()

        return False

    def get_authenticated_user(self, get_creds_callback, realm):
        if not hasattr(self,'realm'):
            self.realm = realm

        try:
            auth = self.request.headers.get('Authorization')
            if auth == None:
                return self.createAuthHeader()
            elif not auth.startswith('Digest '):
                return self.createAuthHeader()
            else:
                self._parseHeader(auth)
                required_params = ['username', 'realm', 'nonce', 'uri', 'response', 'qop', 'nc', 'cnonce']
                for k in required_params:
                    if not self.params.has_key(k):
                        #print "REQUIRED PARAM %s MISSING\n" % k
                        return self.createAuthHeader()
                    elif self.params[k] is None or self.params[k] == '':
                        #print "REQUIRED PARAM %s IS NONE OR EMPTY\n" % k
                        return self.createAuthHeader()
                    else:
                        continue
                        #print k,":",self.params[k]

            creds = get_creds_callback(self.params['username'])
            if not creds:
                self.send_error(400)
            else:
                expected_response = self.response(creds)
                actual_response = self.params['response']

            if expected_response and actual_response:
                if expected_response == actual_response:
                    self._current_user = self.params['username']
                    #print "Digest Auth user '%s' successful for realm '%s'. URI: '%s', IP: '%s'" % (self.params['username'], self.realm, self.request.uri, self.request.remote_ip)
                    return True
                else:
                    self.createAuthHeader()

        except Exception as out:
            #print "FELL THROUGH: %s\n" % out
            #print "AUTH HEADERS: %s" % auth
            #print "SELF.PARAMS: ",self.params,"\n"
            #print "CREDS: ", creds
            #print "EXPECTED RESPONSE: %s" % expected_response
            #print "ACTUAL RESPONSE: %s" % actual_response
            return self.createAuthHeader()


def digest_auth(realm, auth_func):
    """A decorator used to protect methods with HTTP Digest authentication.

"""
    def digest_auth_decorator(func):
        def func_replacement(self, *args, **kwargs):
            if self.get_authenticated_user(auth_func, realm):
                return func(self, *args, **kwargs)
        return func_replacement
    return digest_auth_decorator

def get_digest(username):
    """A callback function provided to bind HTTP Digest Authentication from the Mixin to the mongo authentication store
    """
    auth_handler = MongoAuthorisationService()
    return auth_handler.get_credential(username, settings.DIGEST_CREDENTIAL_TYPE)

def enforce_authorisation(authorisation_level, failure_exception):
    """A decorator used to protect methods with Mongo Authorisation Handler

    """
    def authorisation_wrapper(func):
        def func_replacement(self, *args, **kwargs):
            db_name = ""
            collection_name = ""
            username = ""
            if len(args) > 0 and args[0] is not None:
                db_name = str(args[0])
            if len(args) > 1 and args[1] is not None:
                collection_name = str(args[1])
            if hasattr(self, "current_user"):
                username = self.current_user
                
            if self.validate_authorisation(username, db_name, collection_name, authorisation_level):
                return func(self, *args, **kwargs)
            else:
                raise failure_exception
        return func_replacement
    return authorisation_wrapper
    

class AuthenticationService(object):
    
    def get_credential(self, username, credential_type, ):
        raise NotImplementedError
    
    def validate_authentication(self, username, credential, credential_type):
        raise NotImplementedError
    
    
    def validate_authorisation(self, username, db_name, collection_name,  action ):
        raise NotImplementedError
    
class MongoAuthorisationService(AuthenticationService):
    
    @property
    def a_c(self):
        try:
            return Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        except ConnectionFailure:
            return None
        
    def get_credential(self, username, credential_type="password"):
        
        collection = self.a_c[settings.AUTH_DB][settings.AUTH_COLLECTION]
        
        if collection:
        
            query = {"username":username}
            
            result_obj = collection.find_one(query)
            
            enc_password = result_obj[credential_type]
            
            print enc_password
            
            if result_obj and enc_password:
            
                return enc_password
            else:
                return None
        else:
            return None
        
    def validate_authentication(self, username, credential, credential_type="password"):
        
        collection = self.a_c[settings.AUTH_DB][settings.AUTH_COLLECTION]
        
        if collection:
        
            query = {"username":username}
            
            result_obj = collection.find_one(query)
            
            if result_obj:
            
                enc_password = result_obj[credential_type]
            
                password_result = check_password(credential, enc_password)
        
            if result_obj and password_result:
            
                return result_obj
            else:
                return None
        else:
            return None
        
    def validate_authorisation(self, username, db_name=None, collection_name=None,  action=enum.ACTION_ALL ):
            
        collection = self.a_c[settings.AUTH_DB][settings.PERMISSION_COLLECTION]
        
        if collection:
            
            user_action_query = {"username":username }
            if action:
                user_action_query[action] = ""
            if db_name:
                user_action_query["db"] = db_name
            if collection_name:
                user_action_query["collection"] = collection_name
            
            result_obj = collection.find_one(user_action_query)
            
            if result_obj:
                return True
            else:
                return None
        else:
            return None

