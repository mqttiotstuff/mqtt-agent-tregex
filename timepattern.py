
import json
from functools import *

a = [ (3,'a'),(1,'a'),(3,'a'),(1,'a'), (3,'a'),(1,'a') ] 

# pattern
b = [ ([0,0],'a'), ([1,2], 'a')]


# a = [ (3,'a'), (5,'b'), (2,'c'), (2,'a'), (3,'a'), (2,'a') ]
# 
# # pattern
# b = [ ([0,0],'a'), ([5,10], 'a'), ([0,3], 'a') ]
# 

def isIn(basetime, interval, time):
    first = interval[0]
    second = interval[1]
    assert first <= second
    if time < first + basetime:
        return False
    if time > second + basetime:
        return False
    return True

class Recognition(object):
    def __init__(self,name, p):
        # le 1er element est reconnu
        self.name = name
        self.p = p
        self.pos = 0
        self.currentRecognizedTime = 0
        self.currentTime = 0
        self.terminated = False
        self.recognized = False

    def consume(self, event):
        if self.terminated:
            return
        (te,ne) = self.p[self.pos + 1] 
        (eventt,eventr) = event
        # te is an interval
        self.currentTime += eventt
        if ne == eventr and isIn(self.currentRecognizedTime, te, self.currentTime):
            # recognize the next event
            self.pos += 1
            self.currentRecognizedTime = self.currentTime
        else:
            if self.currentTime > self.currentRecognizedTime + te[1]:
                self.terminated = True
                return


        if self.pos + 1 >= len( self.p):
            # no next
            self.recognized = True
            self.terminated = True
            return
 
    def __str__(self):
        return "[ " + self.name + ", pos " + str(self.pos) + ", next pattern "+ \
                str( self.p[self.pos + 1] if self.pos + 1 < len(self.p) else "-"   ) + \
                ", time " + str(self.currentTime) + ", lastpatterntime " + \
                str(self.currentRecognizedTime) + ", recognized :" + str(self.recognized) + \
                ", terminated :"+ str(self.terminated) +  "]"
    

class TimePattern:
    def __init__(self, name, pattern):
        self.name = name
        self.pattern = pattern


class TimePatternRecognizer(object):

    def __init__(self):
        """ current recognition stack """
        self.stack = []
        """ list of timePattern """
        self.patterns = []

    def dumpStack(self):
        s = map( lambda x: str(x) , self.stack)
        print( reduce( lambda x,i: x +"," + i , s, ""))

    def addTimePattern(self, timePattern):
        assert timePattern is not None
        assert timePattern.name is not None
        self.patterns.append(timePattern)

    def event_arrived(self, event):
     
        # for the existing stack, consume the elements
        for l in self.stack:
            l.consume(event)

        # spawn necessary next Recognizer
        (t,e) = event

        for i in filter( lambda x: x.pattern[0][1] == e, self.patterns):
            rec = Recognition(i.name, i.pattern)
            self.stack.append(rec)

        # result of the epoch
        # self.dumpStack()

    def pop_matched_patterns(self):
        l = filter(lambda x: x.terminated and x.recognized, self.stack)
        self.stack = list(filter(lambda x: not x.terminated, self.stack))
        return l
