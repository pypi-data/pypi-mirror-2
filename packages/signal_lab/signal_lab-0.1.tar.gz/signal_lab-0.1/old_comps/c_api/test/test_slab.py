

import _test_slab
import unittest
from sys import stderr

def addtests( testcase, name ):
    for item in dir(_test_slab):
        if item.startswith(name):
            func = getattr(_test_slab, item )
            setattr(testcase, "test_%(item)s" %vars(), func )


class DictTester( unittest.TestCase ):
    pass

addtests( DictTester, 'dict' )

class EnvironTester( unittest.TestCase ):
    pass

addtests( DictTester, 'env' )

class ListTester( unittest.TestCase ):
    pass

addtests( ListTester, 'list' )

class OptionsTester( unittest.TestCase ):
    pass

addtests( ListTester, 'option' )


if __name__ == '__main__':
    
    
    dict_testsuite = unittest.defaultTestLoader.loadTestsFromTestCase(DictTester)
    env_testsuite = unittest.defaultTestLoader.loadTestsFromTestCase(EnvironTester)
    list_testsuite = unittest.defaultTestLoader.loadTestsFromTestCase(ListTester)
    opts_testsuite = unittest.defaultTestLoader.loadTestsFromTestCase(OptionsTester)
    
    all_tests = unittest.TestSuite([ dict_testsuite,
                                    env_testsuite,
                                    list_testsuite
                                    
                                    ])
    
    ttr = unittest.TextTestRunner(stream=stderr, descriptions=2, verbosity=2)
    ttr.run(all_tests)
    