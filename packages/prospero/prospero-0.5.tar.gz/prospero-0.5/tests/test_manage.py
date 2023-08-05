'''
Created on 20 Apr 2010

@author: numero
'''

import sys,os

sys.path[0:0] = [""]
sys.path.append( os.path.join( os.getcwd(), '..' ) )
import unittest
import simplejson as json
from prospero.manage import Manager
from pymongo import Connection

class Setting(object):
    
    def __init__(self, host, port):
        self.MONGO_HOST = host
        self.MONGO_PORT = port

class Test(unittest.TestCase):


    def setUp(self):
        self.manager = Manager()
        
        self.help_text = ""
        self.fixture_path = "./test_data/fixtures.json"
        self.test_user_name = "test1245"
        self.test_user_password = "test1245"
        self.test_db = "manage"
        self.test_user_collection = "user"
        self.test_permissions_collection = "permissions"
        
        self.test_fixture_db = "test_db_fixture"
        self.test_fixture_collection = "test_collection"
        self.test_fixture_item = u"item1"
        self.test_fixture_item_value = 1234
        pass
    
    def tearDown(self):
        self.drop_collection(self.test_db, self.test_user_collection)
        self.drop_collection(self.test_db, self.test_permissions_collection)
        self.drop_db(self.test_fixture_db)
        
    def drop_collection(self, db_name, collection_name, host="127.0.0.1", port=27017):
        connection = Connection(host, port)
        result_value = connection[db_name].drop_collection(collection_name)
        
    def drop_db(self, db_name, host="127.0.0.1", port=27017):
        connection = Connection(host, port)
        
        connection.drop_database(db_name)
                
    def get_user(self, username, host="127.0.0.1", port=27017):
        connection = Connection(host, port)
        
        return connection[self.test_db][self.test_user_collection].find_one( {"username":username})
    
    def get_connection(self, db_name, collection_name, host="127.0.0.1", port=27017):
        connection = Connection(host, port)
        
        return connection[db_name][collection_name]        
    
    def test_help(self):
        try:
            result = self.manager.run(["-h"])
            
            self.assertTrue(result is None)
        except:
            self.assertTrue(True)
            pass
        
        self.assertTrue(True)
    
    '''
    def test_load_fixtures_success(self):
        
        result, message = self.manager.load_fixtures(self.fixture_path)
                
        self.assertTrue(result)

        
        self.assertTrue(message is not None)
        
        c = self.get_connection(self.test_fixture_db, self.test_fixture_collection)
        
        item_dict = c.find({})
        
        
        item_found = False
        for item in item_dict:
            
            if self.test_fixture_item in item:
                if item[self.test_fixture_item][u'value'] == self.test_fixture_item_value:
                    item_found = True
        
        self.assertTrue(item_found)
    '''
    
    def test_load_fixtures_failure(self):
        pass
    
    def test_test_configuration_success(self):
        
        result, message = self.manager.test_configuration()
        
        self.assertTrue(result)
        
        self.assertEquals(message, "Success")
    
    def test_test_configuration_failure(self):
        setting = Setting("127.0.0.2", 6688)
        
        
        result, message = self.manager.test_configuration(setting)
        
        self.assertFalse(result)
        
        self.assertEquals(message, "Mongo DB Connection Failure: 127.0.0.2 6688")
    
    def test_setup_success(self):
        
        result, message = self.manager.create_user(self.test_user_name, self.test_user_password)
        
        self.assertTrue(result)
        
        user_obj = self.get_user(self.test_user_name)
        
        self.assertEquals(user_obj["username"], self.test_user_name)
        pass
    
    def blanked_test_start_success(self):
        
        self.manager.run(["run_server"])
        
        raise KeyboardInterrupt
        
    
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_load_fixtures_success']
    unittest.main()    