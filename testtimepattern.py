#
# unit test for time pattern
#

import unittest
from timepattern import *

class Test(unittest.TestCase):
    def test_pattern_recognition(self):

        # event sequence
        a = [ (3,'a'),(1,'a'),(3,'a'),(1,'a'), (3,'a'),(1,'a') ] 
        # pattern
        b = TimePattern("first", [ ([0,0],'a'), ([1,2], 'a')])
        
        

        t = TimePatternRecognizer()
        t.addTimePattern(b)
        
   
        epoch = 0
        for i in a:
            epoch = epoch + 1
            t.event_arrived(i)
            strlist = [ str(x) for x in t.pop_matched_patterns() ]
            print("at epoch "+ str(epoch) + str(strlist))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(Test('test_pattern_recognition'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())


