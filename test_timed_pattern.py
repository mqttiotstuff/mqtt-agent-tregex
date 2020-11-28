#
# this is an example of using the time pattern module
#

import json
from functools import *
from timepattern import *

# event sequence
a = [ (3,'a'),(1,'a'),(3,'a'),(1,'a'), (3,'a'),(1,'a') ] 
# pattern
b = [ ([0,0],'a'), ([1,2], 'a')]


# a = [ (3,'a'), (5,'b'), (2,'c'), (2,'a'), (3,'a'), (2,'a') ]
# 
# # pattern
# b = [ ([0,0],'a'), ([5,10], 'a'), ([0,3], 'a') ]
# 


t = TimePatternRecognizer()
t.addTimePattern(TimePattern("name", b))

epoch = 0
for i in a:
    epoch = epoch + 1

    t.event_arrived(i)

    # result of the epoch
    print("Epoch :" + str(epoch) + " step " + str(i))
    t.dumpStack()


