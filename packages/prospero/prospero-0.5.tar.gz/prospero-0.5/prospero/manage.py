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
Created on 25/04/2010

@author: numero
'''
import optparse, sys, os
from util import Watcher, UnixConsole, WindowsConsole
import main, settings, security.ident, enum, getpass
import simplejson
from pymongo import Connection
from pymongo.errors import ConnectionFailure, OperationFailure, AutoReconnect
#from simplejson.decoder import JSONDecodeError

import warnings
warnings.filterwarnings("ignore")


class BootStrap(object):
    
    def __init__(self):
        self.parser = optparse.OptionParser()
    
    def handle_input(self, args):
        self.parser.add_option("-t","-T","--test", action="store_true", dest="test", help="Test Run - Load all parameters and check all prerequisites are met", metavar="testrun", default=False )
        self.parser.add_option("-s","-S","--setup_server", action="store_true", dest="setup_server", help="Create User Collections and Permissions", metavar="setup_server", default=False )
        self.parser.add_option("-l","-L","--load_fixtures", dest="load_fixtures", help="Load Fixtures from JSON File", metavar="load_fixture", type="string" )
        
        options, residual_args = self.parser.parse_args(args)
        
        return options, residual_args 
    

class Manager(object):
    """ 
        The Manager Class handles the configuration and execution of Prospero web server.
        
        The class has a simple processing lifecycle; from a commandline
    """
    def __init__(self):               
        if os.name == 'nt':
            self.console = WindowsConsole()
        else:
            self.console = UnixConsole()
            
        self.starter = BootStrap()
        
        self.host=settings.MONGO_HOST
        self.port=settings.MONGO_PORT
    
    @property
    def c(self ):
        try:
            return Connection(self.host, self.port)
        except ConnectionFailure as e:
            return e
    
    def run(self, args):

        if len(args) > 0:
            
            options, residual_args = self.starter.handle_input(args)
            
            if options.load_fixtures is not None:
                self.console.write("Not Implemented")
                
                #self.console.write("Loading Fixtures")
                #result = self.load_fixtures(options.load_fixtures)
                #self.console.write("Result %s" % result)
                return 0
            if options.test:
                result, result_message = self.test_configuration()
                self.console.write("Test Configuration Success: %s" % result)
                self.console.write("Test Configuration Message: %s" % result_message)
                return 0
            if options.setup_server:
                result, result_message = self.setup_server()
                self.console.write("Test Setup Success: %s" % result)
                self.console.write("Test Setup Message: %s" % result_message)
                return 0
            
            if len(residual_args) > 0 and residual_args[0] == "run_server":
                
                Watcher()
                self.console.write("Starting Server...\n")
                main.run()
        else:
            self.console.write("No Args\nShutting Down...\n")
    
    def load_fixtures(self, file_path):
        result = False
        message = ""
        
        if os.path.exists(file_path):
            file_pointer = None
            try:
                file_pointer = open(file_path)
            except:
                result = False 
                message = "Could Not Load File"
                return result, message
            
            try:

                json_fixture = simplejson.load(file_pointer)
            except JSONDecodeError as e:
                return False, repr(e)
            
            sanitise_result, sanitised_message = self.sanitise_fixture(json_fixture)
            
            if sanitise_result:
                db_skipped, collection_skipped = self.insert_fixture(json_fixture)
                

                return True, self.create_result_string(db_skipped, collection_skipped)
            else:
                return sanitise_result, sanitised_message
        else:
            result = False 
            message = "Path Does Not Exist"
            
        return result, message
    
    def create_result_string(self, db_skipped, collection_skipped):
        result_string = "Db Skipped:"
        
        for db_name in db_skipped:
            result_string += db_name + "\n"
        
        result_string += "Collection Skipped:"
        
        for collection_name in collection_skipped:
            result_string += collection_name + "\n"
            
        return result_string
    
    def insert_fixture(self, json_fixture):
        db_skipped = []
        collection_skipped = []
        for db, db_contents in json_fixture.iteritems():
            if db in self.c.database_names():
                db_skipped.append(db)
            else:
                for collection, collection_contents in db_contents.iteritems():
                    if collection in self.c[db].collection_names():
                        collection_skipped.append(db)
                    else:
                        self.c[db][collection].insert(collection_contents)
        
        return db_skipped, collection_skipped        
        
    
    def sanitise_fixture(self, json_fixture):
        if settings.AUTH_DB in json_fixture:
            return False, "Uses reserved db: %s" % settings.AUTH_DB
        #elif settings.AUTH_COLLECTION in json_fixture[settings.AUTH_DB]:
        #    return False, "Uses reserved collection: %s" % settings.AUTH_COLLECTION
        #elif settings.PERMISSION_COLLECTION in json_fixture[settings.AUTH_DB]:
        #    return False, "Uses reserved collection: %s" % settings.PERMISSION_COLLECTION
        else:
            return True, ""
        
    def test_configuration(self, setting=None):
        if setting is None:
            setting = settings
            
        self.host = setting.MONGO_HOST
        self.port = setting.MONGO_PORT
        
        #Check DB Connection
        result_message = "Success"
        result = True
        connection_result = self.c
        
        if type(connection_result) == type(ConnectionFailure()) or type(connection_result) == type(AutoReconnect()) :
            result = False
            result_message = "Mongo DB Connection Failure: %s %s" % (self.host, self.port)
            
        return result, result_message
    
    def create_user(self, username, credential):
        user_service = security.ident.MongoIdentityService()
        self.console.write("Creating User\n")   
        user_result = user_service.create_user(username, credential)
        self.console.write("Setting Digest Password\n")
        user_digest_result = user_service.add_credential(username, credential, settings.DIGEST_CREDENTIAL_TYPE)
        self.console.write("Creating Permissions\n")
        create_authen_permission_result = user_service.create_user_permission(username, enum.ACTION_ALL, settings.AUTH_DB, settings.AUTH_COLLECTION)
        create_author_permission_result= user_service.create_user_permission(username, enum.ACTION_ALL, settings.AUTH_DB, settings.PERMISSION_COLLECTION)
        
        if user_result and user_digest_result and create_authen_permission_result and create_author_permission_result:
            return True, "Successfully Created User\n"
        else:
            return False, ""

    def prompt_user_input(self):        
        try:
            username_input = "Enter username: "         
            valid_username = False
            while not valid_username:
                username = raw_input(username_input) 
                valid_username = True
                if len(username) < 4:
                    username_input = "Username should be greater than 4 Characters: "
                    valid_username = False
                
                
            password = ""
            password_input = "Enter Password: "         
            valid_password = False
            while not valid_password:
                password = getpass.getpass(password_input)
                valid_password = True
                if len(password) < 4:
                    password_input = "Password should be greater than 4 Characters: "
                    valid_password = False
                    
            password_input = "Confirm Password: "         
            valid_password = False
            while not valid_password:
                second_password = getpass.getpass(password_input)
                if password == second_password:
                    valid_password = True
                else:
                    password_input = "Passwords Should Match: "
            
            return (username, password)
    
        except (KeyboardInterrupt, SystemExit):
            sys.exit(0)

    def setup_server(self):
        
        username, credential = self.prompt_user_input()

        return self.create_user(username, credential)

if __name__ == '__main__':
    args = sys.argv[1:]
    m = Manager()
    m.run(args)        
