'''
Created on 7 Apr 2010

@author: numero
'''

import sys,os

sys.path[0:0] = [""]
sys.path.append( os.path.join( os.getcwd(), '..' ) )
import threading
import tornado.httpserver
import tornado.ioloop
import tornado.web
import prospero.settings as settings
from prospero.main import Prospero

def check_dictionaries_match( dict_one, dict_two):
    if len(dict_one) == len(dict_two):
        keys = zip(dict_one.keys(),dict_two.keys())
        
        keys_result = all(map(compare, keys))
        
        
        values = zip(dict_one.items(),dict_two.items())
        
        values_result = all(map(compare, values)) 
        
        return keys_result and values_result
        
    else:
        return False
    
def compare(item): 
    a = item[0]
    b = item [1]
    if a == b:
        return True
    else:
        return False

def run_in_thread(fn):
        def run(*k, **kw):
            t = threading.Thread(target=fn, args=k, kwargs=kw)
            t.start()
            
        return run


class TestProsperoServer():
    
    def __init__(self,port=None):
        if not port:
            port = settings.PORT
        else:
            self.port = port
    
    @run_in_thread
    def run_server(self):
        print "Starting Test Server on %s" % self.port
        server = tornado.httpserver.HTTPServer(Prospero())
        server.listen(self.port)
        tornado.ioloop.IOLoop.instance().start()
        #print "Started Test Server"
    
    def start(self):
        self.run_server()
  
    def stop(self):
        print "Stopping Test Server"
        tornado.ioloop.IOLoop.instance().stop()
        print "Stopped Test Server"
        
if __name__ == "__main__":
    a = {"a":1234, "b":5678}
    b = {"a":1234, "b":5678}
    print check_dictionaries_match(a, b)

