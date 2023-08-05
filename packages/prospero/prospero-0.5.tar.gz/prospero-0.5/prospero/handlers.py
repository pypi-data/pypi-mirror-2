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
Created on 7 Apr 2010

@author: numero
'''
from pymongo import Connection, json_util,  objectid
from pymongo.errors import InvalidId
from pymongo.son import SON
from pymongo.errors import ConnectionFailure
 
from tornado.web import HTTPError
import tornado.web

AMFLOADED = True
PYGMENTSLOADED = True

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters.html import HtmlFormatter
except ImportError:
    PYGMENTSLOADED = False
    
try:
    from amfast.encoder import Encoder
except ImportError:
    AMFLOADED = False

import os, simplejson


import settings, enum
import security.auth as auth


class Serialiser(object):

    NAME = "Serialiser"
    def __init__(self):
        pass
        
    def serialise(self, parent, **kwargs):
        raise NotImplementedError

class JSONSerialiser(Serialiser):
    
    NAME = "JSONSerialiser"
    mimetype = "application/json"
    
    def serialise(self, parent, **kwargs):
        return simplejson.dumps(kwargs, default=json_util.default)
    
    
class AMFSerialiser(Serialiser):
    
    NAME = "AMFSerialiser"
    
    mimetype = "application/amf"
    
    def serialise(self, parent, **kwargs):
        encoder = Encoder(amf3=True)
        encoded = encoder.encode(kwargs)
        return encoded
    
class HTMLSerialiser(Serialiser):
    
    
    NAME = "HTMLSerialiser"
    
    mimetype = "application/html"
    
    def __init__(self, template_name = None):
        self.template_name = template_name
        
    
    def serialise(self, parent, **kwargs):
        
        self.handler = tornado.web.RequestHandler()
        self.handler.render_string(self.template_name, kwargs)

class HighlightedHTMLSerialiser(HTMLSerialiser):
    
    
    NAME = "HighlightedHTMLSerialiser"
    
    mimetype = "text/html"
    
    def __init__(self, template_name = None):
        self.template_name = template_name
        self.lexer = get_lexer_by_name("javascript")
        self.formatter = HtmlFormatter()

        
    
    def serialise(self, parent, **kwargs):
        if parent:
            json_input = simplejson.dumps(kwargs, 
                                          default=json_util.default, 
                                          indent=4)
            
            result = highlight(json_input, self.lexer, self.formatter)
            
            docs = {"result":result}
            
            return parent.render_string(self.template_name, **docs)
        else:
            return None
         
class SerialiserFactory(object):
    
    DEFAULT = "*/*"

    def __init__(self):
        self.serialisers = {JSONSerialiser.mimetype:JSONSerialiser()}
        
        if AMFLOADED:
            self.serialisers[AMFSerialiser.mimetype] = AMFSerialiser()
        if PYGMENTSLOADED:
            self.serialisers[HighlightedHTMLSerialiser.mimetype] = HighlightedHTMLSerialiser(settings.GENERIC_TEMPLATE)
            self.serialisers[SerialiserFactory.DEFAULT] = HighlightedHTMLSerialiser(settings.GENERIC_TEMPLATE)


    def get_serialiser(self, name_list):
        """Retrieve the first serialiser whose mime-type
           matches the first mime-type on the list
            
        """
        for name in name_list:
            if name in self.serialisers:
                return self.serialisers[name]
            else:
                return None
    

class BaseHandler(auth.SafeDigestAuthMixin, auth.MongoAuthorisationService, tornado.web.RequestHandler):
    """BaseHandler  - Super Class for all Prospero Handlers

        Provides common persistence and serialisation functions

    """
    
    @property
    def c(self):
        """Create a PyMongo Connection Handle

        Uses the HOST and PORT from settings to return a pymongo.Connection object

        Returns None if ConnectionFailure occurs
        """
        try:
            return Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        except ConnectionFailure:
            return None
        
        
    @property
    def serialiser_names(self):
        names = self.get_mimetype()
        if names:
            names = names.split(",")
        else:
            names = ["*/*"]
        
        return names
    
    def get_mimetype(self):
        if "Accept" in self.request.headers: 
            mimetype = self.request.headers["Accept"]
            return mimetype
        else:
            return None

    def render(self, template_name, **kwargs):

        path = os.path.join(settings.TEMPLATE_PATH, template_name)
        super(BaseHandler, self).render(path, **kwargs)

    def respond_back_result(self, result):
        """ Transforms MongoDB command result to JSON. """
        if result:
            self.write(simplejson.dumps(str(result)))

        self.finish()
        
    def serialise(self, serialiser_name, **kwargs):       
        serialiser = SerialiserFactory().get_serialiser(serialiser_name)
        
        if serialiser:
            return serialiser.serialise(self, **kwargs)
        else:
            return None
        

        
    def get_son(self, str):      
        """Transform a String into SON 
        
            1) Transform to JSON
            2) Transform to PyMongo SON
        """
        
        result = None
        try:
            result = simplejson.loads(str)
        except (ValueError, TypeError):
            result = ('{"ok" : 0, "errmsg" : "couldn\'t parse json: %s"}' % str)
            return result

        if getattr(result, '__iter__', False) == False:
            result = ('{"ok" : 0, "errmsg" : "type is not iterable: %s"}' % str)
            return result
            
        # can't deserialize to an ordered dict!
        if '$pyhint' in result:
            temp = SON()
            for pair in result['$pyhint']:
                temp[pair['key']] = pair['value']
            result = temp

        return result

class DatabaseHandler(BaseHandler):

    @auth.digest_auth(settings.AUTH_REALM, auth.get_digest)
    @auth.enforce_authorisation(enum.ACTION_READ, HTTPError(401))
    def get(self, db_name):
        connection = self.c
        if db_name and connection:
            if db_name in connection.database_names():
                
                result = { "name": db_name,
                          "collections" : connection[db_name].collection_names()
                            }

                result_encoded = self.serialise(self.serialiser_names, docs=result)
                self.write(result_encoded)
            else:
                raise HTTPError(404)
        else:
            raise HTTPError(400)

class CollectionHandler(BaseHandler):

    @auth.digest_auth(settings.AUTH_REALM, auth.get_digest)
    @auth.enforce_authorisation(enum.ACTION_READ, HTTPError(401))
    def get(self, db_name, collection_name):
        connection = self.c
        if db_name and collection_name and connection:
            if collection_name in connection[db_name].collection_names():
                
                result = { "name": collection_name,
                          "index" : connection[db_name][collection_name].index_information(),
                            }
                
                
                result_encoded = self.serialise(self.serialiser_names, docs=result)
                self.write(result_encoded)
            else:
                raise HTTPError(404)
        else:
            raise HTTPError(400)

class ItemHandler(BaseHandler):    

    
    def read_query_result(self, cursor, limit=-1):        
        
        """Read a set of results in from the datastore into a buffer.
        
          :Parameters:
          - `cursor`: the datastore cursor to retrieve the results from
          - `limit` (optional): the number of results to return
        """
        result = []
        if limit > -1:
            cursor = cursor.limit(limit)
        count = 0
        for doc in cursor:
            if count <= limit or limit == -1:
                result.append(doc)
            else:
                break
            count = count +1 
        return result
        
        
    def build_query(self):
        """Build a Query based on the Request arguments
        
           If an argument is not set in the request, set it to a default value
        """
        
        spec = dict()
        fields = None
        skip = 0
        limit = -1
        timeout = True
        snapshot = False
        tailable = False
        count = False
        
        if "spec" in self.request.arguments:
            spec = self.get_son(self.get_argument("spec"))
        if "fields" in self.request.arguments:
            fields = self.get_son(self.get_argument("fields"))
        if "skip" in self.request.arguments:
            skip = int(self.get_argument("skip"))
        if "limit" in self.request.arguments:
            limit = int(self.get_argument("limit"))
        if "timeout" in self.request.arguments:
            timeout = bool(self.get_argument("timeout"))
        if "snapshot" in self.request.arguments:
            snapshot = bool(self.get_argument("snapshot"))
        if "tailable" in self.request.arguments:
            tailable = bool(self.get_argument("tailable"))
        if "count" in self.request.arguments:
            count = bool(self.get_argument("count"))

        return spec, fields, skip, limit, timeout, snapshot, tailable, count
    
    
    @auth.digest_auth(settings.AUTH_REALM, auth.get_digest)
    @auth.enforce_authorisation(enum.ACTION_READ, HTTPError(401))        
    def get(self, db_name, collection_name):
        connection = self.c
        if db_name and collection_name and connection:

            spec, fields, skip, limit, timeout, snapshot, tailable, count = self.build_query()

            if skip < 0 or limit < -1:
                raise HTTPError(401)

            docs = connection[db_name][collection_name].find(spec = spec, fields = fields, skip = skip, timeout = timeout, snapshot = snapshot, tailable = tailable)
            
            result = dict()
            
            if count:
                result["count"] = docs.count()
            else:
                result_value = self.read_query_result(docs, limit)
                result["docs"] = result_value
            
            
            result_encoded = self.serialise(self.serialiser_names, docs=result)
            self.write(result_encoded)

        else:
            raise HTTPError(400)
    
    
    @auth.digest_auth(settings.AUTH_REALM, auth.get_digest)
    @auth.enforce_authorisation(enum.ACTION_CREATE, HTTPError(401))     
    def post(self, db_name, collection_name):
        connection = self.c
        if db_name and collection_name and connection:
            docs = None
            if self.request.files and "docs" in self.request.files:
                docs = self.get_son(self.request.files["docs"][0]['body'])
            
            if docs:
                result_value = connection[db_name][collection_name].insert(docs)
                
                result = {"ok":1,
                          "objectids":result_value}
                
                
                result_encoded = self.serialise(self.serialiser_names, docs=result)
                self.write(result_encoded)
            else:
                raise HTTPError(400)

        else:
            raise HTTPError(400)
    
class ItemInstanceHandler(BaseHandler):
    

    @auth.digest_auth(settings.AUTH_REALM, auth.get_digest)
    @auth.enforce_authorisation(enum.ACTION_READ, HTTPError(401)) 
    def get(self, db_name, collection_name, item_id):
        connection = self.c
        if db_name and collection_name and item_id and connection:
            item_object_id = None
            try:
                item_object_id = objectid.ObjectId(item_id)
            except InvalidId as e:
                pass
            
            if item_object_id:
    
                doc = connection[db_name][collection_name].find_one(item_object_id)
              
    
                result_encoded = self.serialise(self.serialiser_names, docs=doc)
                if result_encoded:
                    self.write(result_encoded)
                else:
                    raise HTTPError(401)
            else:
                raise HTTPError(401)
        else:
            raise HTTPError(400)
   
class AuthHandler(BaseHandler):
    

        
    @auth.digest_auth(settings.AUTH_REALM, auth.get_digest)
    def get(self):
        self.write("ECHO")
            
class DoubleAuthHandler(BaseHandler):
    

        
    @auth.digest_auth(settings.AUTH_REALM, auth.get_digest)
    @auth.enforce_authorisation(enum.ACTION_READ, HTTPError(401))
    def get(self):
        self.write("ECHO")             
        
    @auth.digest_auth(settings.AUTH_REALM, auth.get_digest)
    @auth.enforce_authorisation(enum.ACTION_CREATE, HTTPError(401))
    def post(self):
        self.write("ECHO")       
           

urls = [(r'/ping/authentication/', AuthHandler),
        (r'/ping/authorisation/', DoubleAuthHandler),
        (r'/database/([^/]+)/collection/([^/]+)/doc/([^/]+)/', ItemInstanceHandler),
        (r'/database/([^/]+)/collection/([^/]+)/doc/', ItemHandler),
        (r'/database/([^/]+)/collection/([^/]+)/', CollectionHandler),
        (r'/database/([^/]+)/', DatabaseHandler),
        ]