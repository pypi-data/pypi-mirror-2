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
import os
import base64
 
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
RESOURCE_PATH = os.path.join(os.path.abspath(os.path.pardir), 'resources')
 
DEBUG = True
 
PORT = 9998
 
SECRET = base64.b64encode(os.urandom(32))
 
TEMPLATE_PATH = os.path.join(RESOURCE_PATH, 'templates')
STATIC_PATH = os.path.join(RESOURCE_PATH, 'static')
GENERIC_TEMPLATE = "generic_serialiser.html"
 
# MongoDB
MONGO_PORT = 27017
MONGO_HOST = 'localhost'

DOC_CONTAINER = "docs"
AUTH_DB = 'manage'
AUTH_COLLECTION = 'user'
PERMISSION_COLLECTION = 'permissions'
AUTH_REALM = "prospero"
PASSWORD_CREDENTIAL_TYPE = "password"
DIGEST_CREDENTIAL_TYPE = "digest__"+AUTH_REALM