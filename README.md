# Timed Sequence Event Regex



This repository contains a simple implementation for detecting timed-based sequences of events. 

Given a sequence of events in time, given some Time Patterns , the recognizer raise the name of the pattern if the timed events match the sequence.

Applications are, for example :

- using a simple button to trigger several actions (depending on how it is pressed). 
- when a presence detector is triggered and then a button pressed on the desk, light the desk  

... many applications



A 5 mins example

```python
#
# this is an example of using the time pattern module
#

import json
from functools import *
from timepattern import *

# event sequence, it assume we start at epoch 0, 
# first number is the relative time between the previous event
# for example here : (3,'a'),(1,'a')
#    means the first 'a' event is at timestamp 3 (start from 0)
#    then the following 'a' event is at 3+1 = 4
# and so on

a = [ (3,'a'),(1,'a'),(3,'a'),(1,'a'), (3,'a'),(1,'a') ]

# pattern definition
b = [ ([0,0],'a'), ([1,2], 'a')]


## other example to play with
# a = [ (3,'a'), (5,'b'), (2,'c'), (2,'a'), (3,'a'), (2,'a') ]
# 
# # pattern
# b = [ ([0,0],'a'), ([5,10], 'a'), ([0,3], 'a') ]
# 


t = TimePatternRecognizer()
t.addTimePattern(TimePattern("1-2SecondsBetween", b))

epoch = 0
for i in a:
    epoch = epoch + 1

    t.event_arrived(i)

    # result of the epoch
    print("Epoch :" + str(epoch) + " " + \
          ",".join(map(lambda x: x.name, t.pop_matched_patterns())))  


```

The output result is :

```
Epoch :1 
Epoch :2 1-2SecondsBetween
Epoch :3 
Epoch :4 1-2SecondsBetween
Epoch :5 
Epoch :6 1-2SecondsBetween

```



### Timed pattern definition

The timed pattern is described as a list of time range (the from and to time), and a name pattern for the event.  



## Grammar



TimeTuple: `([minTimeFromLastEvent, waitTime], EVENTPATTERN)`

TimedPattern : `[` TimeTuple, TimeTuple, TimeTuple ....   `]`



Currently EVENTPATTERN is the name of the event, or `^`EVENTNAME for negation

