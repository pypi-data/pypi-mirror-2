# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# test_decorators.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Mar 27 13:58:57 2007
#
#----------------------------------------------------------------------------# 

import unittest
import doctest
from decorators import *

#----------------------------------------------------------------------------#

def suite():
    test_suite = unittest.TestSuite((
            unittest.makeSuite(DecoratorsTestCase),
        ))
    return test_suite

#----------------------------------------------------------------------------#

@memoized
def get_example():
    return Example()

class Example(object):
    def __init__(self):
        self.value = 3
        return

class DecoratorsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_memoized(self):
        """Tests for proper caching behaviour with a simple class."""
        x = get_example()
        self.assertEqual(x.value, 3)

        y = get_example()
        assert x is y

        x.value = 5
        self.assertEqual(y.value, 5)

        return

    def test_one_shot(self):
        x = [1]

        @one_shot
        def f():
            return x.pop()

        self.assertEqual(f(), 1)
        self.assertEqual(x, [])
        self.assertEqual(f(), 1)
        self.assertEqual(f(), 1)
        return
    
    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

