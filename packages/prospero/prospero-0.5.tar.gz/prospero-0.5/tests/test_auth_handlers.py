'''
Created on 18/04/2010

@author: numero
'''
import sys,os
sys.path[0:0] = [""]
sys.path.append( os.path.join( os.getcwd(), '..' ) )
import unittest
from test_utils import TestProsperoServer, check_dictionaries_match
import simplejson as json
import time
from pymongo import Connection
from copy import deepcopy
import prospero.settings as settings
import prospero.security.auth as auth
import prospero.util as util
import prospero.enum as enum
from restclient import GET, POST

class Test(unittest.TestCase):

    def setUp(self):
        self.port = 9998
        self.base_url = "http://localhost:%s" % self.port
        
        self.auth_path = "/ping/authentication/"
        self.authorisation_path = "/ping/authorisation/"
        
        self.test_db = "manage"
        self.test_user_collection = "user"
        self.test_permissions_collection = "permissions"
        
        self.setup_data()

    def setup_data(self):
        self.test_user_one_username = "abc"
        self.test_user_one_raw_password = "abc"
        digest_name = settings.DIGEST_CREDENTIAL_TYPE
        digest = util.create_http_digest(self.test_user_one_username, settings.AUTH_REALM, self.test_user_one_raw_password)
        self.test_user_one = {"username": self.test_user_one_username, digest_name: digest}

        self.users = [self.test_user_one]
        
        self.permissions = [{"db":self.test_db, "collection":self.test_user_collection, "username":"abc", enum.ACTION_READ:""}, 
                            {"db":"", "collection":"", "username":"abc", enum.ACTION_READ:""},
                            {"db":self.test_db, "collection":"", "username":"abc", enum.ACTION_READ:""},
                            ]
        
        self.build_user_collection(self.get_collection(self.test_db, self.test_user_collection), self.users)
        self.build_permissions_collection(self.get_collection(self.test_db, self.test_permissions_collection), self.permissions)

    def get_collection(self, db_name, collection_name, host="127.0.0.1", port=27017):
        connection = Connection(host, port)
        
        return connection[db_name][collection_name]
    
    def build_user_collection(self, collection, users):
        result_value = collection.insert(users)     
        
    def build_permissions_collection(self, collection, permissions):
        result_value = collection.insert(permissions)   
    
    def tearDown(self):
        self.drop_mongo_data(self.test_db, self.test_user_collection)
    
    def drop_mongo_data(self, db_name, collection_name, host="127.0.0.1", port=27017):
        connection = Connection(host, port)
        
        result_value = connection[db_name].drop_collection(collection_name)
        
        connection.drop_database(db_name)
        pass

    def get_http_response(self, response_obj):
        return_value = response_obj[1]
        
        http_status = response_obj[0]["status"]
        
        return return_value, http_status


    def test_get_element_digest_auth_success(self):
                
        test_get_auth_url = self.base_url + self.auth_path
        
        
        response_obj = GET(test_get_auth_url, params = {},
                   async = False, credentials = ["abc","abc",""], resp = True)
        
        
        return_value, http_status = self.get_http_response(response_obj)
        
        
        self.assertEquals(http_status,"200")
        
    def test_get_element_digest_auth_failure(self):
                
        test_get_auth_url = self.base_url + self.auth_path
        
        response_obj = GET(test_get_auth_url, params = {},
                   async = False, credentials = ["abc","def",""], resp = True)
        
        
        return_value, http_status = self.get_http_response(response_obj)
        
        self.assertEquals(http_status,"401")

    def test_get_element_authorisation_success(self):
                
        test_get_auth_url = self.base_url + self.authorisation_path
        
        response_obj = GET(test_get_auth_url, params = {},
                   async = False, credentials = ["abc","abc",""], resp = True)
        
        
        return_value, http_status = self.get_http_response(response_obj)
        
        
        self.assertEquals(http_status,"200")
        
    def test_get_element_authorisation_failure(self):
                
        test_get_auth_url = self.base_url + self.authorisation_path
        
        response_obj = POST(test_get_auth_url, params = {},
                   async = False, credentials = ["abc","abc",""], resp = True)
        
        
        return_value, http_status = self.get_http_response(response_obj)
        
        self.assertEquals(http_status,"401")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_get_element_authorisation_failure']
    testServer = TestProsperoServer(9998)
    testServer.start()
    time.sleep(2)
    unittest.main()
    testServer.stop()