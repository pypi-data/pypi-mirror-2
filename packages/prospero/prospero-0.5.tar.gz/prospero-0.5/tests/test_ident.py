'''
Created on 20 Apr 2010

@author: numero
'''

import sys,os

sys.path[0:0] = [""]
sys.path.append( os.path.join( os.getcwd(), '..' ) )
import unittest
from pymongo import Connection
import prospero.enum as enum
import prospero.security.ident as ident
import prospero.security.auth as auth
from prospero.security.ident import MongoIdentityService
from prospero.security.auth import MongoAuthorisationService


class Test(unittest.TestCase):


    def setUp(self):
        self.test_db = "manage"
        self.test_user_collection = "user"
        self.test_permissions_collection = "permissions"
        
        self.test_user_name = "abc"
        self.test_user_one_raw_password = "abc"
        
        
        self.test_invalid_user_name = "def"
        
        self.test_user_one_raw_password_changed = "def"
        self.test_user_one = {"username":"abc","password":"a24lkd$d50a9e64d485292917ab9526b968f1af34112c11"}
        
        self.handler = MongoIdentityService()
        self.auth_handler = MongoAuthorisationService()

        
    def tearDown(self):
        self.drop_collection(self.test_db, self.test_user_collection)
        self.drop_collection(self.test_db, self.test_permissions_collection)
        self.drop_mongo_database(self.test_db)

    def drop_mongo_database(self, db_name, host="127.0.0.1", port=27017):
        connection = Connection(host, port)
        
        connection.drop_database(db_name)

        
    def drop_collection(self, db_name, collection_name, host="127.0.0.1", port=27017):
        connection = Connection(host, port)
        result_value = connection[db_name].drop_collection(collection_name)

        
    def get_user(self, username, host="127.0.0.1", port=27017):
        connection = Connection(host, port)
        
        return connection[self.test_db][self.test_user_collection].find_one( {"username":username})

    def test_create_user_success(self):
        user_obj = self.handler.create_user(self.test_user_name, self.test_user_one_raw_password)
        
        user = self.get_user(self.test_user_name)
        
        self.assertTrue(user is not None)
        self.assertEquals(repr(user_obj), repr(user[u'_id']))
        self.assertEquals(self.test_user_name, user["username"])
    
    
    def test_create_user_failure(self):
        user_obj = self.handler.create_user(self.test_user_name, self.test_user_one_raw_password)
        
        user = self.handler.create_user(self.test_user_name, self.test_user_one_raw_password)
        
        self.assertTrue(user is None)

    def test_delete_user_success(self):
        user_obj = self.handler.create_user(self.test_user_name, self.test_user_one_raw_password)
        user = self.get_user(self.test_user_name)
        self.assertTrue(user is not None)
    
        result = self.handler.delete_user(self.test_user_name)
        
        self.assertTrue(result)

        user = self.get_user(self.test_user_name)
        self.assertTrue(user is None)        
        
    
    
    def test_delete_user_failure(self):
        result = self.handler.delete_user(self.test_user_name)
        
        self.assertTrue(result is None)

        user = self.get_user(self.test_user_name)
        self.assertTrue(user is None)     


    def test_change_credential_success(self):
        self.handler.create_user(self.test_user_name, self.test_user_one_raw_password)
        result_obj = self.handler.change_user_password(self.test_user_name, self.test_user_one_raw_password_changed)
        
        auth_result = self.auth_handler.validate_authentication(self.test_user_name, self.test_user_one_raw_password_changed)
        
        self.assertTrue(result_obj is not None)
        
        self.assertTrue(auth_result)
    
    def test_change_credential_failure(self):
        result_obj = self.handler.change_user_password(self.test_invalid_user_name, self.test_user_one_raw_password_changed)
        
        auth_result = self.auth_handler.validate_authentication(self.test_invalid_user_name, self.test_user_one_raw_password_changed)
        
        self.assertTrue(result_obj is None)
        
        self.assertFalse(auth_result)
    
    
    def test_create_user_permission_success(self):
        self.handler.create_user(self.test_user_name, self.test_user_one_raw_password)
        result_obj = self.handler.create_user_permission(self.test_user_name, enum.ACTION_ALL)
        
        
        self.assertTrue(result_obj is not None)
        
        auth_result = self.auth_handler.validate_authorisation(self.test_user_name)

        self.assertTrue(auth_result)
    
    
    def test_create_user_permission_failure(self):
        result_obj = self.handler.create_user_permission(self.test_user_name, enum.ACTION_ALL)
                
        self.assertTrue(result_obj is None)
        
        auth_result = self.auth_handler.validate_authorisation(self.test_user_name)

        self.assertFalse(auth_result)
    
    def test_get_user_permission_success(self):
        self.handler.create_user(self.test_user_name, self.test_user_one_raw_password)
        result_obj = self.handler.create_user_permission(self.test_user_name, enum.ACTION_ALL)
        
        permissions = self.handler.get_user_permissions(self.test_user_name)
        
        self.assertEquals(len(permissions),1)
    
    
    def test_get_user_permission_failure(self):
        self.handler.create_user(self.test_invalid_user_name, self.test_user_one_raw_password)
        
        result_obj = self.handler.create_user_permission(self.test_invalid_user_name, enum.ACTION_ALL)
        
        permissions = self.handler.get_user_permissions(self.test_user_name)
        
        self.assertEquals(len(permissions),0)
    
    def test_delete_user_permission_success(self):
        self.handler.create_user(self.test_user_name, self.test_user_one_raw_password)
        self.handler.create_user_permission(self.test_user_name, enum.ACTION_ALL)
        
        permissions = self.handler.get_user_permissions(self.test_user_name)
        self.assertEquals(len(permissions),1)
        
        result_obj = self.handler.delete_user_permission(self.test_user_name)
        
        self.assertTrue(result_obj is not None)
            
        self.assertEquals(len(result_obj),1)
        
        permissions = self.handler.get_user_permissions(self.test_user_name)
        self.assertEquals(len(permissions),0)
    
    
    def test_delete_user_permission_failure(self):
        self.handler.create_user(self.test_user_name, self.test_user_one_raw_password)
        self.handler.create_user_permission(self.test_user_name, enum.ACTION_ALL)
        
        permissions = self.handler.get_user_permissions(self.test_user_name)
        self.assertEquals(len(permissions),1)
        
        result_obj = self.handler.delete_user_permission(self.test_invalid_user_name)
        
        self.assertEquals(len(result_obj),0)
        
        permissions = self.handler.get_user_permissions(self.test_user_name)
        self.assertEquals(len(permissions),1)
    
    
    def test_get_available_permissions(self):
        self.handler.create_user(self.test_user_name, self.test_user_one_raw_password)
        result_obj = self.handler.create_user_permission(self.test_user_name, enum.ACTION_ALL)
        
        available_permissions = self.handler.get_available_permissions()

        self.assertEquals(len(available_permissions),30)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_get_available_permissions']
    unittest.main()