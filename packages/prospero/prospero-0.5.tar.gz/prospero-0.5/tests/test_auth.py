'''
Created on 15 Apr 2010

@author: numero
'''

import sys,os,time
sys.path[0:0] = [""]
sys.path.append( os.path.join( os.getcwd(), '..' ) )
import unittest
import prospero.enum as enum
import prospero.security.auth as auth
from prospero.security.auth import MongoAuthorisationService
from pymongo import Connection

class Test(unittest.TestCase):

    def setUp(self):
        self.test_db = "manage"
        self.test_user_collection = "user"
        self.test_permissions_collection = "permissions"
        
        self.test_user_one_raw_password = "abc"
        self.test_user_one = {"username":"abc","password":"a24lkd$d50a9e64d485292917ab9526b968f1af34112c11"}
        
        self.users = [self.test_user_one]
        self.permissions = [{"db":self.test_db, "collection":self.test_user_collection, "username":"abc", enum.ACTION_READ:""}, 
                            {"username":"abc", enum.ACTION_READ:""},
                            {"db":self.test_db, "username":"abc", enum.ACTION_READ:""},
                            ]
        
        
        self.build_user_collection(self.get_collection(self.test_db, self.test_user_collection), self.users)
        
        self.build_permissions_collection(self.get_collection(self.test_db, self.test_permissions_collection), self.permissions)
        pass


    def tearDown(self):
        
        self.drop_collection(self.test_db, self.test_user_collection)
        
        self.drop_collection(self.test_db, self.test_permissions_collection)
        
        #self.drop_mongo_database(self.test_db)
        pass
    
    def get_collection(self, db_name, collection_name, host="127.0.0.1", port=27017):
        connection = Connection(host, port)
        
        return connection[db_name][collection_name]
    
    def build_user_collection(self, collection, users):
        result_value = collection.insert(users)     

    def build_permissions_collection(self, collection, permissions):
        #print permissions
        result_value = collection.insert(permissions)
        #print result_value

    def drop_collection(self, db_name, collection_name, host="127.0.0.1", port=27017):
        connection = Connection(host, port)
        
        result_value = connection[db_name].drop_collection(collection_name)
        
        pass
    
    def drop_mongo_database(self, db_name, host="127.0.0.1", port=27017):
        connection = Connection(host, port)
        
        connection.drop_database(db_name)


    def test_authentication_success(self):
        handler = MongoAuthorisationService()
        
        result = handler.validate_authentication(self.test_user_one["username"], self.test_user_one_raw_password)

        self.assertTrue(result)
    
    
    def test_authentication_failure(self):
        handler = MongoAuthorisationService()
        
        result = handler.validate_authentication(self.test_user_one["username"], "wrong_password")

        self.assertFalse(result)
        
    def test_authorisation_success(self):
        time.sleep(1)        
        
        handler = MongoAuthorisationService()
    
        result = handler.validate_authorisation(self.test_user_one["username"],self.test_db, self.test_user_collection,enum.ACTION_READ)

        self.assertTrue(result)
        
    def test_authorisation_success_system(self):
        time.sleep(1)        
        
        handler = MongoAuthorisationService()
        
        result = handler.validate_authorisation(self.test_user_one["username"],"", "",enum.ACTION_READ)

        self.assertTrue(result)
        
        
    def test_authorisation_failure_system(self):
        handler = MongoAuthorisationService()
        
        result = handler.validate_authorisation(self.test_user_one["username"],"", "",enum.ACTION_DELETE)

        self.assertFalse(result)


        
    def test_authorisation_success_db(self):
        time.sleep(1)        
        
        handler = MongoAuthorisationService()
        
        result = handler.validate_authorisation(self.test_user_one["username"],self.test_db, None,enum.ACTION_READ)

        self.assertTrue(result)
            
    def test_authorisation_failure_db(self):
        handler = MongoAuthorisationService()
        
        result = handler.validate_authorisation(self.test_user_one["username"],self.test_db, "",enum.ACTION_DELETE)

        self.assertFalse(result)
    
    def test_authorisation_failure(self):
        handler = MongoAuthorisationService()
        
        result = handler.validate_authorisation(self.test_user_one["username"],self.test_db, self.test_user_collection,enum.ACTION_DELETE)

        self.assertFalse(result)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_authorisation_success']
    unittest.main()