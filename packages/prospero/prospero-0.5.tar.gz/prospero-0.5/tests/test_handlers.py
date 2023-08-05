'''
Created on 7 Apr 2010

@author: numero
'''

import sys,os
import unittest
import time
from copy import deepcopy

import simplejson as json
from pymongo import Connection
from amfast.decoder import Decoder

sys.path[0:0] = [""]
sys.path.append( os.path.join( os.getcwd(), '..' ) )

from test_utils import TestProsperoServer, check_dictionaries_match

from prospero.security.ident import MongoIdentityService
import prospero.settings as settings
import prospero.enum as enum
from restclient import GET, POST

class Test(unittest.TestCase):


    def setUp(self):
        self.port = 9998
        self.base_url = "http://localhost:%s" % self.port
        
        self.test_user = "test_user"
        self.test_password = "test_password"
        
        self.test_db = "test_db"
        self.test_collection = "test_collection"
        
        self.db_path = "/database/%s/"
        self.collection_path = "/database/%s/collection/%s/"
        self.insert_item_path = "/database/%s/collection/%s/doc/"
        
        self.auth_path = "/auth/"
        
        self.test_doc = {u"foo" : u"bar"}
        self.test_doc_b = {u"baz" : u"bif"}
        self.test_doc_c = {u"bell" : u"bowl"}
        self.test_doc_multi = {u"foo" : u"bar", u"baz" : u"bif", u"bell" : u"bowl"}
        
        self.test_json_mimetype = "application/json"
        self.test_amf_mimetype = "application/amf"
        
        self.test_error_mimetype = "application/invalid___"
        
        self.insert_data = [self.test_doc]
        self.insert_data_multi = [self.test_doc, self.test_doc_b, self.test_doc_c]

        self.get_item_path = "/database/%s/collection/%s/doc/%s/"
        self.get_items_path = self.insert_item_path
        
        self.setup_permissions()
        
        
    def setup_permissions(self):
        identity_service = MongoIdentityService()
        
        identity_service.create_user(self.test_user, self.test_password, settings.DIGEST_CREDENTIAL_TYPE)
        
        identity_service.create_user_permission(self.test_user, enum.ACTION_READ,self.test_db)
        identity_service.create_user_permission(self.test_user, enum.ACTION_READ, self.test_db, self.test_collection) 
        identity_service.create_user_permission(self.test_user, enum.ACTION_CREATE, self.test_db, self.test_collection)
        
        
    def tearDown(self):
        self.drop_collection(self.test_db, self.test_collection)
        #self.drop_mongo_database(self.test_db)
        
        identity_service = MongoIdentityService()
        identity_service.delete_user_permission(self.test_user, self.test_db)
        identity_service.delete_user_permission(self.test_user, self.test_db, self.test_collection)
        
        identity_service.delete_user(self.test_user)
        
        
        pass
    
    def get_http_response(self, response_obj):
        return_value = response_obj[1]
        
        http_status = response_obj[0]["status"]
        
        return return_value, http_status
    
    def drop_collection(self, db_name, collection_name, host="127.0.0.1", port=27017):
        connection = Connection(host, port)
        
        result_value = connection[db_name].drop_collection(collection_name)
        pass
    
    def drop_mongo_database(self, db_name, host="127.0.0.1", port=27017):
        connection = Connection(host, port)
        
        connection.drop_database(db_name)

    
    def insert_docs(self, db_name, collection_name, docs, host="127.0.0.1", port=27017):
        insert_docs = deepcopy(docs)
        connection = Connection(host, port)
        
        result_value = connection[db_name][collection_name].insert(insert_docs)
        
        return result_value



    def test_get_database(self):
        self.insert_docs(self.test_db, self.test_collection, self.test_doc)
        
        test_get_db_url = self.base_url + (self.db_path % (self.test_db))
        
        
        return_value = GET(test_get_db_url, params = {}, accept = [self.test_json_mimetype], credentials = [self.test_user, self.test_password,""],
                   async = False )
        
        
        self.assertEquals(type(return_value).__name__, "str")
        
        decoded_return_value = json.loads(return_value)
        

        self.assertEquals(decoded_return_value[settings.DOC_CONTAINER]['name'], self.test_db)
        
    def test_get_collection(self):
        
        doc_id = self.insert_docs(self.test_db, self.test_collection, self.insert_data)
        
        test_get_collection_url = self.base_url + (self.collection_path % (self.test_db,self.test_collection))
        
        
        return_value = GET(test_get_collection_url, params = {},accept = [self.test_json_mimetype], credentials = [self.test_user, self.test_password,""],
                   async = False )
        
        
        self.assertEquals(type(return_value).__name__, "str")
        
        decoded_return_value = json.loads(return_value)
        

        self.assertEquals(decoded_return_value[settings.DOC_CONTAINER]['name'], self.test_collection)
        #self.assertEquals(decoded_return_value['collections'], [])

    def test_insert_element(self):
        test_insert_url = self.base_url + (self.insert_item_path % (self.test_db,self.test_collection))
        
        return_value = POST(test_insert_url, files = {'docs' : {"file":json.dumps(self.insert_data),"filename":"docs"}}, accept = [self.test_json_mimetype], credentials = [self.test_user, self.test_password,""],
                   async = False )

        self.assertEquals(type(return_value).__name__, "str")

        return_obj = json.loads(return_value)[settings.DOC_CONTAINER]

        self.assertEquals(return_obj['ok'], 1)
        
        
        self.assertTrue("objectids" in return_obj)

        self.assertTrue(return_obj["objectids"][0] is not None)
        
    def test_insert_elements(self):
        test_insert_url = self.base_url + (self.insert_item_path % (self.test_db,self.test_collection))
        
        return_value = POST(test_insert_url, files = {'docs' : {"file":json.dumps(self.insert_data_multi),"filename":"docs"}}, accept = [self.test_json_mimetype], credentials = [self.test_user, self.test_password,""],
                   async = False )

        self.assertEquals(type(return_value).__name__, "str")

        return_obj = json.loads(return_value)[settings.DOC_CONTAINER]

        self.assertEquals(return_obj['ok'], 1)
        
        
        self.assertTrue("objectids" in return_obj)
        
        self.assertEquals(len(return_obj["objectids"]),3)

        self.assertTrue(return_obj["objectids"][0] is not None)
        self.assertTrue(return_obj["objectids"][1] is not None)
        self.assertTrue(return_obj["objectids"][2] is not None)
        
    
    def test_insert_nodb_nocollection_error(self):
        test_insert_url = self.base_url + (self.insert_item_path % ("",""))
        
        response_obj = POST(test_insert_url, files = {'docs' : {"file":json.dumps(self.insert_data),"filename":"docs"}}, accept = [self.test_json_mimetype], credentials = [self.test_user, self.test_password,""],
                   async = False, resp = True )
        
        return_value, http_status = self.get_http_response(response_obj)

        self.assertEquals(type(return_value).__name__, "str")
        
        self.assertEquals(http_status,'404')   

    def test_insert_nodb_error(self):
        test_insert_url = self.base_url + (self.insert_item_path % ("",self.test_collection))
        
        response_obj = POST(test_insert_url, files = {'docs' : {"file":json.dumps(self.insert_data),"filename":"docs"}}, accept = [self.test_json_mimetype], credentials = [self.test_user, self.test_password,""],
                   async = False, resp = True )
        
        return_value, http_status = self.get_http_response(response_obj)

        self.assertEquals(type(return_value).__name__, "str")
        
        self.assertEquals(http_status,'404')
        
    def test_insert_nocollection_error(self):
        test_insert_url = self.base_url + (self.insert_item_path % (self.test_db,""))
        
        response_obj = POST(test_insert_url, files = {'docs' : {"file":json.dumps(self.insert_data),"filename":"docs"}}, accept = [self.test_json_mimetype], credentials = [self.test_user, self.test_password,""],
                   async = False, resp = True )
        
        return_value, http_status = self.get_http_response(response_obj)

        self.assertEquals(type(return_value).__name__, "str")
        
        self.assertEquals(http_status,'404')       
        
    def test_insert_nodocs_error(self):
        test_insert_url = self.base_url + (self.insert_item_path % ("",""))
        
        response_obj = POST(test_insert_url, async = False, resp = True, accept = [self.test_json_mimetype], credentials = [self.test_user, self.test_password,""],)
        
        return_value, http_status = self.get_http_response(response_obj)

        self.assertEquals(type(return_value).__name__, "str")
        
        self.assertEquals(http_status,'404')        
        
    def test_get_element(self):
        
        doc_id = self.insert_docs(self.test_db, self.test_collection, self.insert_data)
        
        item_id = str(doc_id[0])
        
        test_get_element_url = self.base_url + (self.get_item_path % (self.test_db, self.test_collection, item_id))
        return_value = GET(test_get_element_url, accept = [self.test_json_mimetype], async = False, credentials = [self.test_user, self.test_password,""], )

        self.assertEquals(type(return_value).__name__, "str")
        

        doc_obj = json.loads(return_value)[settings.DOC_CONTAINER]

        self.assertTrue(u'_id' in doc_obj)
        self.assertEquals(doc_obj[u'_id'][u'$oid'],unicode(item_id))
        
        del doc_obj[u'_id']
        #del self.test_doc[u'_id']
        
        self.assertTrue(check_dictionaries_match(doc_obj, self.test_doc))
  
  
    def test_get_element_error_nooid(self):
        
        doc_id = self.insert_docs(self.test_db, self.test_collection, self.insert_data)
        
        item_id = str(doc_id[0])
        
        test_get_element_url = self.base_url + (self.get_item_path % (self.test_db, self.test_collection, ""))
        response_obj = GET(test_get_element_url, async = False,accept = [self.test_json_mimetype], resp = True , credentials = [self.test_user, self.test_password,""])

        return_value, http_status = self.get_http_response(response_obj)

        self.assertEquals(type(return_value).__name__, "str")
        
        self.assertEquals(http_status,'404')        

  
    def test_get_elements(self):
        
        doc_ids = self.insert_docs(self.test_db, self.test_collection, self.insert_data_multi)
        
        item_id_one, item_id_two, item_id_three, = str(doc_ids[0]), str(doc_ids[1]), str(doc_ids[2])
        
        test_get_element_url = self.base_url + (self.get_items_path % (self.test_db, self.test_collection))

        return_value = GET(test_get_element_url, params={'spec' : str(json.dumps(self.test_doc))}, accept = [self.test_json_mimetype], async = False, credentials = [self.test_user, self.test_password,""] )

        self.assertEquals(type(return_value).__name__, "str")

        return_obj = json.loads(return_value)[settings.DOC_CONTAINER]
        self.assertTrue("docs" in return_obj)
        
        docs_obj = return_obj["docs"]
        
        self.assertEquals(len(docs_obj),1)
        
        self.assertEquals(str(docs_obj[0]["_id"][u"$oid"]),item_id_one)

        
    def test_get_element_custom_mimetype_amf(self):
        
        doc_id = self.insert_docs(self.test_db, self.test_collection, self.insert_data)
        
        item_id = str(doc_id[0])
        
        test_get_element_url = self.base_url + (self.get_item_path % (self.test_db, self.test_collection, item_id))
        response_obj = GET(test_get_element_url, async = False, accept = [self.test_amf_mimetype] , resp = True, credentials = [self.test_user, self.test_password,""])

        return_value, http_status = self.get_http_response(response_obj)

        self.assertEquals(type(return_value).__name__, "str")

        decoder = Decoder(amf3=True)
        doc_obj = decoder.decode(return_value)[settings.DOC_CONTAINER]
        

        self.assertTrue(u'_id' in doc_obj)
        
        del doc_obj[u'_id']
        
        self.assertTrue(check_dictionaries_match(doc_obj, self.test_doc))
        

    def test_get_element_custom_mimetype_invalid(self):
        
        doc_id = self.insert_docs(self.test_db, self.test_collection, self.insert_data)
        
        item_id = str(doc_id[0])
        
        test_get_element_url = self.base_url + (self.get_item_path % (self.test_db, self.test_collection, item_id))
        response_obj = GET(test_get_element_url, async = False, accept = [self.test_error_mimetype] , resp = True, credentials = [self.test_user, self.test_password,""])

        return_value, http_status = self.get_http_response(response_obj)

        self.assertEquals(http_status,"401")
    

    def test_get_elements_count(self):
        
        doc_ids = self.insert_docs(self.test_db, self.test_collection, self.insert_data_multi)
        
        item_id_one, item_id_two, item_id_three, = str(doc_ids[0]), str(doc_ids[1]), str(doc_ids[2])
        
        test_get_element_url = self.base_url + (self.get_items_path % (self.test_db, self.test_collection))

        return_value = GET(test_get_element_url, params={'spec' : str(json.dumps(self.test_doc)), 'count': "true"}, accept = [self.test_json_mimetype], async = False, credentials = [self.test_user, self.test_password,""] )

        self.assertEquals(type(return_value).__name__, "str")

        return_obj = json.loads(return_value)[settings.DOC_CONTAINER]
        self.assertTrue("count" in return_obj)
        
        count_obj = return_obj["count"]
        
        self.assertEquals(count_obj,1)
        
        
    def test_get_elements_limit(self):
        self.insert_docs(self.test_db, self.test_collection, self.insert_data_multi)
        self.insert_docs(self.test_db, self.test_collection, self.insert_data_multi)
        self.insert_docs(self.test_db, self.test_collection, self.insert_data_multi)
         
        test_get_element_url = self.base_url + (self.get_items_path % (self.test_db, self.test_collection))

        return_value = GET(test_get_element_url, params={'spec' : str(json.dumps(self.test_doc)), "limit": 1}, accept = [self.test_json_mimetype], async = False, credentials = [self.test_user, self.test_password,""] )

        self.assertEquals(type(return_value).__name__, "str")

        return_obj = json.loads(return_value)
        self.assertTrue("docs" in return_obj)
        
        docs_obj = return_obj["docs"]
        
        self.assertEquals(len(docs_obj),1)
        
        
    def test_get_elements_range(self):
        self.insert_docs(self.test_db, self.test_collection, self.insert_data_multi)
        self.insert_docs(self.test_db, self.test_collection, self.insert_data_multi)
        self.insert_docs(self.test_db, self.test_collection, self.insert_data_multi)
        
        test_get_element_url = self.base_url + (self.get_items_path % (self.test_db, self.test_collection))

        return_value = GET(test_get_element_url, params={'spec' : str(json.dumps(self.test_doc)), "range_start" : 0, "range_finish" : 1}, accept = [self.test_json_mimetype], async = False, credentials = [self.test_user, self.test_password,""], )

        self.assertEquals(type(return_value).__name__, "str")

        return_obj = json.loads(return_value)
        self.assertTrue("docs" in return_obj)
        
        docs_obj = return_obj["docs"]
        
        self.assertEquals(len(docs_obj),1)
        
        #self.assertEquals(str(docs_obj[0]["_id"][u"$oid"]),item_id_one)
        
    def test_get_elements_range_start_only(self):
        self.insert_docs(self.test_db, self.test_collection, self.insert_data_multi)
        self.insert_docs(self.test_db, self.test_collection, self.insert_data_multi)
        self.insert_docs(self.test_db, self.test_collection, self.insert_data_multi)
        
        test_get_element_url = self.base_url + (self.get_items_path % (self.test_db, self.test_collection))

        return_value = GET(test_get_element_url, params={'spec' : str(json.dumps(self.test_doc)), "skip" : 1}, accept = [self.test_json_mimetype], async = False, credentials = [self.test_user, self.test_password,""] )

        self.assertEquals(type(return_value).__name__, "str")

        return_obj = json.loads(return_value)[settings.DOC_CONTAINER]
        self.assertTrue("docs" in return_obj)
        
        docs_obj = return_obj["docs"]
        
        self.assertEquals(len(docs_obj),2)
        
        #self.assertEquals(str(docs_obj[0]["_id"][u"$oid"]),item_id_one)
        
    def test_get_elements_range_end_only(self):
        self.insert_docs(self.test_db, self.test_collection, self.insert_data_multi)
        self.insert_docs(self.test_db, self.test_collection, self.insert_data_multi)
        self.insert_docs(self.test_db, self.test_collection, self.insert_data_multi)
        
        test_get_element_url = self.base_url + (self.get_items_path % (self.test_db, self.test_collection))

        return_value = GET(test_get_element_url, params={'spec' : str(json.dumps(self.test_doc)), "skip": 1, "limit" : 1}, accept = [self.test_json_mimetype], async = False, credentials = [self.test_user, self.test_password,""] )

        self.assertEquals(type(return_value).__name__, "str")

        return_obj = json.loads(return_value)[settings.DOC_CONTAINER]
        self.assertTrue("docs" in return_obj)
        
        docs_obj = return_obj["docs"]
        
        self.assertEquals(len(docs_obj),1)
        
        #self.assertEquals(str(docs_obj[0]["_id"][u"$oid"]),item_id_one)

    def test_get_elements_range_negative(self):
        self.insert_docs(self.test_db, self.test_collection, self.insert_data_multi)
        self.insert_docs(self.test_db, self.test_collection, self.insert_data_multi)
        self.insert_docs(self.test_db, self.test_collection, self.insert_data_multi)
        
        test_get_element_url = self.base_url + (self.get_items_path % (self.test_db, self.test_collection))

        response_obj = GET(test_get_element_url, params={'spec' : str(json.dumps(self.test_doc)), "skip" : -1, "limit" : -3},  async = False, resp = True, credentials = [self.test_user, self.test_password,""],  )

        return_value, http_status = self.get_http_response(response_obj)

        self.assertEquals(http_status,"401")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_get_database']
    testServer = TestProsperoServer(9998)
    testServer.start()
    time.sleep(2)
    unittest.main()
    testServer.stop()