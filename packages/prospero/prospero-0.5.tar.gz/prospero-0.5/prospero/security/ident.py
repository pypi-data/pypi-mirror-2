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
Created on 17/04/2010

@author: numero
'''

import sys, os
from pymongo import Connection
from pymongo.errors import ConnectionFailure
import prospero.enum as enum
import prospero.settings as settings

from prospero.util import create_password, create_http_digest
from copy import deepcopy



DB_BLACKLIST = {"local":True, "admin":True}
COLLECTION_BLACKLIST = {"system.indexes":True}

class PermissionVO():
    
    def __init__(self, db_name, collection_name, action):
        self.db = db_name
        self.collection = collection_name
        self.action = action
        
    def __str__(self):
        return "%s %s %s" % (self.db, self.collection, self.action)
    
    def equals(self, vo):
        if vo.db == self.db and vo.collection == self.collection and vo.action == self.action:
            return True
        else:
            return False

class IdentityService(object):
    
    def create_user(self, username, credential, credential_type):
        """ 
            Create a User based on the given credentials
            
            credential type allows specification of multiple credential types for a user to authenticate with.
        """
        raise NotImplementedError
    
    def delete_user(self, username):
        raise NotImplementedError
    
    def change_user_password(self, username, credential, credential_type ):
        raise NotImplementedError
    
    def add_credential(self, username, credential, credential_type):
        raise NotImplementedError
    
    def disable_user(self, username):
        raise NotImplementedError
    
    def get_user(self, username):
        raise NotImplementedError
    
    def get_users(self, fields=None):
        raise NotImplementedError
    
    def create_user_permission(self, username, permission_value, db_name = None, collection_name = None):
        """
            Create User Permission 
            
            Create a permission for the designated database, collection set to the designated action value
        """
        raise NotImplementedError 
       
    def get_user_permissions(self, username, db_name = None, collection_name = None):
        raise NotImplementedError
        
    def delete_user_permission(self, username, db_name = None, collection_name = None):
        raise NotImplementedError
    
    def get_available_permissions(self):
        raise NotImplementedError
    
class MongoIdentityService(IdentityService):
    
    @property
    def c(self):
        try:
            return Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        except ConnectionFailure:
            return None
    
    def read_query_result(self, cursor, limit=None):
        result = []
        for doc in cursor:
            result.append(doc)
        return result
        
    def build_credential(self, username, credential, credential_type):
        if credential_type == settings.PASSWORD_CREDENTIAL_TYPE:
            return create_password(credential)
        elif credential_type == settings.DIGEST_CREDENTIAL_TYPE:
            return create_http_digest(username, settings.AUTH_REALM, credential)
        else:
            return credential
        
    def create_user(self, username, credential, credential_type="password"):
        
        collection = self.c[settings.AUTH_DB][settings.AUTH_COLLECTION]
        
        if collection:
        
            query = {"username":username}
            
            user_doesnot_exist = collection.find_one(query)
            
            if not user_doesnot_exist:
                
                create_user = {"username":username, credential_type : self.build_credential(username, credential, credential_type)}
                
                result_obj = collection.insert(create_user)
                
                if result_obj:
                
                    return result_obj
                else:
                    return None
            else:
                return None
        else:
            return None
        
    def add_credential(self, username, credential, credential_type="password"):
        
        collection = self.c[settings.AUTH_DB][settings.AUTH_COLLECTION]
        
        if collection:
        
            query = {"username":username}
            
            user = collection.find_one(query)
            
            if user:
                
                user[credential_type] = self.build_credential(username, credential, credential_type)
                
                result_obj = collection.save(user)
                
                if result_obj:
                
                    return result_obj
                else:
                    return None
            else:
                return None
        else:
            return None
        
    def delete_user(self, username):
        
        collection = self.c[settings.AUTH_DB][settings.AUTH_COLLECTION]
        
        if collection:
        
            query = {"username":username}
            
            user_doesnot_exist = collection.find_one(query)
            
            if user_doesnot_exist:
                
                target_user = {"username":username}
                
                result_obj = collection.remove(target_user)
                
                return True
            else:
                return None
        else:
            return None
        
    def get_user(self, username):
               
        collection = self.c[settings.AUTH_DB][settings.AUTH_COLLECTION]
        
        if collection:
        
            query = {"username":username}
            
            user = collection.find_one(query)
            
            if user:
                return user
            else:
                return None
        else:
            return None
        
    def get_users(self, fields=None):               
        collection = self.c[settings.AUTH_DB][settings.AUTH_COLLECTION]
        
        if collection:
            
            print fields
        
            users = collection.find(spec = {}, fields = fields)
            
            if users:
                return users
            else:
                return None
        else:
            return None
    
    def change_user_password(self, username, credential, credential_type="password"):
        
        collection = self.c[settings.AUTH_DB][settings.AUTH_COLLECTION]
        
        if collection:
        
            query = {"username":username}
            
            user = collection.find_one(query)
            
            if user:
                
                user[credential_type] = self.build_credential(username, credential, credential_type)
                
                result_obj = collection.save(user)
                
                if result_obj:
                
                    return result_obj
                else:
                    return None
            else:
                return None
        else:
            return None
      
    def create_user_permission(self, username, action, db_name = None, collection_name = None):
        collection = self.c[settings.AUTH_DB][settings.PERMISSION_COLLECTION]
        if collection:
            
            
            user = self.get_user(username)
            
            if user:
            
                permission_query = {"username":username, action: ""}
                
                if db_name:
                    permission_query["db"] = unicode(db_name)
                if collection_name:
                    permission_query["collection"] = unicode(collection_name)
                                    
                result_obj = collection.insert(permission_query)
                
                if result_obj:
                    return result_obj
                else:
                    return None
            
            else:
                return None
        else:
            return None
    
    def get_user_permissions(self, username, db_name = None, collection_name = None):
        collection = self.c[settings.AUTH_DB][settings.PERMISSION_COLLECTION]
        
        if collection:
        
            permission_query = {"username":username}
            
            if db_name:
                permission_query["db"] = db_name
            if collection_name:
                permission_query["collection"] = collection_name
            
            cursor = collection.find(permission_query)
            
            result_objs = self.read_query_result(cursor)
            
            return result_objs
        else:
            return None
    
    def delete_user_permission(self, username, db_name = None, collection_name = None):
        collection = self.c[settings.AUTH_DB][settings.PERMISSION_COLLECTION]
        
        if collection:
            user_permissions = self.get_user_permissions(username, db_name, collection_name)
            
            if len(user_permissions) > 0:
                
                result = []
                
                for permission in user_permissions:
                    
                    result.append(deepcopy(permission))
                    
                    collection.remove(permission)
                
                return user_permissions
            else:
                return []
        else:
            return None
    
    
    def get_available_permissions(self):    
        permission_list = []
        db_names = self.c.database_names()
        
        for db_name in db_names:
            
            if db_name not in DB_BLACKLIST:
            
                new_db_permissions = self.build_all_permissions(db_name, None)
                permission_list.extend(new_db_permissions)
                
                collections_names = self.c[db_name].collection_names()
                
                for collection_name in collections_names:
                    
                    if collection_name not in COLLECTION_BLACKLIST:
                        new_collection_permissions = self.build_all_permissions(db_name, collection_name)
                    
                        permission_list.extend(new_collection_permissions)
                
        return permission_list
            
    def build_all_permissions(self, db_name, collection):
        return [PermissionVO(db_name, collection, enum.ACTION_CREATE), 
                PermissionVO(db_name, collection, enum.ACTION_READ), 
                PermissionVO(db_name, collection, enum.ACTION_UPDATE), 
                PermissionVO(db_name, collection, enum.ACTION_DELETE), 
                PermissionVO(db_name, collection, enum.ACTION_ALL)]
            
            
        