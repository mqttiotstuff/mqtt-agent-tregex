#
# unit test for time pattern
#

import unittest
from timepattern import *

class Test(unittest.TestCase):

    def test_inner_pattern(self):

        print("Start inner test")
        a = [ (3,'a'),(1,'a'), (4,'b')] 
        
        # pattern recognized is a 'a' then [1,2] seconds and then a 'a'
        b = TimePattern("first", [ ([0,0],'a'), ([1,2], 'a')])
        c = TimePattern("onlyone", [ ([0,0],'a') ])
        d = TimePattern("other", [ ([0,0],'b') ])
        e = TimePattern("negative", [ ([0,0],'a'), ([3,4], '^a') ])
        

        t = TimePatternRecognizer()
        t.addTimePattern(b)
        t.addTimePattern(c)
        t.addTimePattern(d)
        t.addTimePattern(e)
        
   
        epoch = 0
        for i in a:
            epoch = epoch + 1

            t.event_arrived(i)
            strlist = [ str(x) for x in t.pop_matched_patterns() ]
            print("at epoch " +  str(epoch) + " " + str(i) +  " recognized :"+ str(strlist))
            print("  dump stack")
            t.dumpStack()
            print('==============')




    def test_pattern_recognition(self):

        # event sequence
        # this event sequence is :

        a = [ (3,'a'),(1,'a'),(3,'a'),(1,'a'), (3,'a'),(1,'a') ] 
        
        # pattern recognized is a 'a' then [1,2] seconds and then a 'a'
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
    suite.addTest(Test('test_inner_pattern'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())


