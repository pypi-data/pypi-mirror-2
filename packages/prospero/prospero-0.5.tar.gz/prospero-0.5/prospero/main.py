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

import settings
import handlers
import security.handlers
import tornado
import tornado.httpserver
import tornado.web
 
class Prospero(tornado.web.Application):
 
    def __init__(self):
        settings_dict = {'cookie_secret': settings.SECRET,
                    'xsrf_cookies': False,
                    'template_path': settings.TEMPLATE_PATH,
                    'static_path': settings.STATIC_PATH,
                    'debug': settings.DEBUG}
        tornado.web.Application.__init__(self, handlers.urls+security.handlers.urls, **settings_dict)
 
def run():
    try:
        server = tornado.httpserver.HTTPServer(Prospero())
        server.listen(settings.PORT)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
 
if __name__ == '__main__':
    run()
        
 