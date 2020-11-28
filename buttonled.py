#
# Mqttagent that play musicbox
#

import paho.mqtt.client as mqtt
import random
import time
import re
import configparser
import os.path
import json

import traceback

import subprocess
from timepattern import *

config = configparser.RawConfigParser()


SMARTBUTTON = "home/agents/smartbuttons"
ALERTE_TOPIC="home/agents/ledbox/alert"

#############################################################
## MAIN

conffile = os.path.expanduser('~/.mqttagents.conf')
if not os.path.exists(conffile):
   raise Exception("config file " + conffile + " not found")

config.read(conffile)


username = config.get("agents","username")
password = config.get("agents","password")
mqttbroker = config.get("agents","mqttbroker")

client2 = mqtt.Client()

# client2 is used to send events to wifi connection in the house 
client2.username_pw_set(username, password)
client2.connect(mqttbroker, 1883, 60)

client = mqtt.Client();
client.username_pw_set(username, password)

BUTTON = "home/esp13/sensors/+"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    client.subscribe(BUTTON)

t = TimePatternRecognizer()
t.addTimePattern(TimePattern("modenuit",[ ([0,0],'interrupt2'), ([0,2],'interrupt3') ]))
t.addTimePattern(TimePattern("modejour",[ ([0,0],'interrupt1'), ([0,2],'interrupt4') ]))
t.addTimePattern(TimePattern("play",[ ([0,0],'interrupt1'), ([0,2],'interrupt3') ]))

publishedTopics = { "modenuit": 
                        { ALERTE_TOPIC: "100,0,0", \
                                       "home/agents/smoothlights":"0,0,0", \
                                      "home/esp11/actuators/relay1":"1", \
                                      "home/agents/musicbox/play":"1"},\
                    "modejour": 
                        { ALERTE_TOPIC: "0,100,0", \
                                       "home/agents/smoothlights":"100,100,100", \
                                      "home/esp11/actuators/relay1":"0", \
                                      "home/agents/musicbox/play":"1"},\
                    "play": 
                        { ALERTE_TOPIC: "100,100,100", \
                                "home/agents/musicbox/play":"1"}}

latesttime = time.time()

def on_message(client, userdata, msg):
   global t
   global latesttime
   global publishedTopics

   try:
      index_latests = msg.topic.rfind("/")
      latest = msg.topic[index_latests + 1:]

      currentTime = time.time()

      # print(str(currentTime) + " " + latest + " -> " + str(msg.payload))
      if msg.payload.decode("utf-8") != "1":
          return
      t.event_arrived( ( (currentTime - latesttime), latest ))
      latesttime = currentTime;
      popedPattern = list(t.pop_matched_patterns())
      if len(popedPattern) > 0:
         for p in popedPattern:
             print("pattern hit " + str(p.name))
             if p.name in publishedTopics:
                 for k,v in publishedTopics[p.name].items():
                     print("send " + str(k) + "->" + str(v))
                     client2.publish(k,v)

   except:
      traceback.print_exc();

client.on_connect = on_connect
client.on_message = on_message
client.connect(mqttbroker, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

client2.loop_start()
client.loop_start()

lastvalue = None

while True:
   try:
      time.sleep(3)
      client2.publish(SMARTBUTTON + "/health", "1")


   except Exception:
        traceback.print_exc()



