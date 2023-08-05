'''
Created on 23 Apr 2010

@author: numero
'''

import sys, os
sys.path[0:0] = [""]
sys.path.append( os.path.join( os.getcwd(), '..' ) )
import unittest
import test_auth_handlers, test_auth, test_handlers, test_ident, test_manage
from test_utils import TestProsperoServer
from prospero.util import Watcher

if __name__ == "__main__":
    
    #Watcher()
    #import sys;sys.argv = ['', 'Test.testName']
    testsuite = [unittest.TestLoader().loadTestsFromTestCase(test_auth_handlers.Test),
                 unittest.TestLoader().loadTestsFromTestCase(test_auth.Test),
                 unittest.TestLoader().loadTestsFromTestCase(test_ident.Test),        
                 unittest.TestLoader().loadTestsFromTestCase(test_handlers.Test),
                 unittest.TestLoader().loadTestsFromTestCase(test_manage.Test),
                 ]
    
    alltests = unittest.TestSuite(testsuite)
    
    testServer = TestProsperoServer(9998)
    testServer.start()
    
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    testServer.stop()