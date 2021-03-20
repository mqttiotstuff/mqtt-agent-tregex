
import json
from functools import *

# check if the given time is in the base time with interval, 
# interval limits are included
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

        # handle the case with one event
        self.terminated = len(p) == 1
        self.recognized = len(p) == 1

    def consume(self, event):
        if self.terminated:
            return
        (eventt,eventr) = event
        self.currentTime += eventt

        assert len(self.p) > 1

        # next nt
        (te,ne) = self.p[self.pos + 1] 

        # te is an interval
        if (ne == eventr or (ne[0] == '^' and ne[1:] != eventr)) and isIn(self.currentRecognizedTime, te, self.currentTime):
            # recognize the next event
            self.pos += 1
            self.currentRecognizedTime = self.currentTime
        elif ne[0] == '^' and self.currentRecognizedTime + te[1] > self.currentTime :
            # negative time has elapsed
            self.pos += 1
            self.currentRecognizedTime = self.currentTime
        else:
            if self.currentTime > self.currentRecognizedTime + te[1]:
                self.terminated = True
                return


        if self.pos + 1 >= len( self.p):
            # reach the end of events, no next
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
#        if len(pattern)<2:
#            raise Exception("time pattern must have at least 2 elements")
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

        # spawn necessary next Recognizer for the event
        (t,e) = event

        for i in filter( lambda x: x.pattern[0][1] == e, self.patterns):
            rec = Recognition(i.name, i.pattern)
            self.stack.append(rec)

        # result of the epoch
        # self.dumpStack()

    def pop_matched_patterns(self):
        l = filter(lambda x: x.terminated and x.recognized, self.stack)
        # remove terminated
        self.stack = list(filter(lambda x: not x.terminated, self.stack))
        return l

    
