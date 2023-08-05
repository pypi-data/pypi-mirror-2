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
Created on 27 Apr 2010

@author: numero
'''
import sys, os
import prospero.enum as enum
import prospero.settings as settings
import local_settings as security_settings
from tornado.web import HTTPError, RequestHandler
from ident import MongoIdentityService
import ident

from tornado.options import define, options

class BaseHandler(RequestHandler):

    def render(self, template_name, **kwargs):
        """ Overriden Render method, which decorates the template path to hook it into 
            the settings-defined path configuration
        """
        path = os.path.join(settings.TEMPLATE_PATH, template_name)
        super(BaseHandler, self).render(path, **kwargs)

    
class CreateUserHandler(BaseHandler):
    
    
    def get(self):
        #Render Template
        self.render("security/create_user.html", info_messages=[], old_username="")
    
    def post(self):
        #Check Auth and Auth
        username = self.get_argument('username')
        password = self.get_argument('password')
        password_confirm = self.get_argument('password_confirm')
        list
        validity_check = False
        password_check = False
        username_check = False
        error_messages = [("Username should be %s characters" % security_settings.USERNAME_LENGTH),
                          ("Password should be %s characters" % security_settings.PASSWORD_LENGTH),
                          ("Passwords should match")]
        
        if len(username) > security_settings.USERNAME_LENGTH:
            username_check = True
            error_messages.pop()
            
        
        if len(password) > security_settings.PASSWORD_LENGTH and password == password_confirm:
            password_check = True
            error_messages.pop()
            error_messages.pop()
        
        validity_check = username_check and password_check
        
        
        if validity_check:
            identity_service = MongoIdentityService()
            create_user_result = identity_service.create_user(username, password)
            identity_service.add_credential(username, password, settings.DIGEST_CREDENTIAL_TYPE)
            
            if create_user_result:
                self.render("security/create_user.html", info_messages=["User Successfully Created"], old_username="")
            else:
                self.render("security/create_user.html", info_messages=["User Creation Error"], old_username=username)
        else:
            
            self.render("security/create_user.html", info_messages=error_messages, old_username=username)

class GetUsersHandler(BaseHandler):
    
    
    def get(self):
        identity_engine = MongoIdentityService()
        
        users = identity_engine.get_users(fields=[u"username"])
        
        users_stripped = []
        for user in users:
            users_stripped.append(user[u"username"])
        
        #Return Current Permissions
        
        self.render("security/list_users.html", info_messages=[], user_list=users_stripped)
    
    
class CreateUserPermissionsHandler(BaseHandler):
    
    def get(self, username):
        #Pass User
        #Pass DB, Collection, Permission
        #Return DB, Collections, Options for Each
        
        identity_engine = MongoIdentityService()
        
        user = identity_engine.get_user(username)
        
        user_stripped = object()
        user_stripped = user[u"username"]
        
        available_permissions = self.retrieve_permission_list(username)
        
        self.render("security/create_permission.html", info_messages=[], user=user_stripped, permission_list=available_permissions)
    
    
    def reduce(self, available_permissions, current_user_permissions):
        for permission in current_user_permissions:
            for i, available_permission in enumerate(available_permissions):
                if available_permission.db == permission[u"db"]  and available_permission.action in permission:
                    if (u"collection" in permission and available_permission.collection == permission[u"collection"]) or not (u"collection" in permission): 
                        del available_permissions[i]
                    
                        break
                
        return available_permissions
    
    def retrieve_permission_list(self, username):
        identity_engine = MongoIdentityService()
        available_permissions = identity_engine.get_available_permissions()
        
        user_permissions = identity_engine.get_user_permissions(username)
        
        available_permissions = self.reduce(available_permissions, user_permissions)      
        
        return available_permissions
    
    def post(self, username):
        #User
        
        #Permissions
        
        identity_engine = MongoIdentityService()
        
        user = identity_engine.get_user(username)
        
        user_stripped = object()
        user_stripped = user[u"username"]
        
        available_permissions_argument = self.get_argument('available_permissions')
  
        db_name, collection_name, action = available_permissions_argument.split()
        
        
        if collection_name == "None":
            collection_name = None
        
        result = identity_engine.create_user_permission(username, action, db_name, collection_name)
        
        available_permissions = self.retrieve_permission_list(username)
        
        self.render("security/create_permission.html", info_messages=[], user=user_stripped, permission_list=available_permissions)
    
    
class DeleteUserPermissionsHandler(BaseHandler):
    
    def get(self, username):
        #Pass User
        #Pass DB, Collection, Permission
        #Return DB, Collections, Options for Each
        
        identity_engine = MongoIdentityService()
        
        user = identity_engine.get_user(username)
        
        user_stripped = object()
        user_stripped = user[u"username"]
        
        
        user_permissions = identity_engine.get_user_permissions(username)
        new_permissions = map(self.convert_permissions, user_permissions)
        #Return Current Permissions
        
        self.render("security/delete_permission.html", info_messages=[], user=user_stripped, permission_list=new_permissions)
    
    def convert_permissions(self, permission):
        action = None
    
        action = self.get_action(permission, enum.ACTION_LIST)
        
        
        db_name = "None"
        collection_name = "None"
        if u"db" in permission:
            db = permission[u"db"]

        if u"collection" in permission:
            collection = permission[u"collection"]
        
        new_permission = ident.PermissionVO(db, collection, action)
        
        return new_permission
    
    def get_action(self, dictionary, list):
        action = None
        
        for item in list:
            if item in dictionary:
                action = item
                break
        
        return action

    
    def post(self, username):
        identity_engine = MongoIdentityService()
        
        user = identity_engine.get_user(username)
        
        user_stripped = object()
        user_stripped = user[u"username"]
        
        current_permissions_argument = self.get_argument('current_permissions')

        db_name, collection_name, action = current_permissions_argument.split()
        
        if collection_name == "None":
            collection_name = None
        
        identity_engine.delete_user_permission(username, db_name, collection_name)
        
        user_permissions = identity_engine.get_user_permissions(username)
        new_permissions = map(self.convert_permissions, user_permissions)
        
        self.render("security/delete_permission.html", info_messages=[], user=user_stripped, permission_list=new_permissions)
    
urls = [(r'/manage/users/', GetUsersHandler),
        (r'/manage/user/create/', CreateUserHandler),
        (r'/manage/permissions/([^/]+)/create/', CreateUserPermissionsHandler),
        (r'/manage/permissions/([^/]+)/delete/', DeleteUserPermissionsHandler),
        ]