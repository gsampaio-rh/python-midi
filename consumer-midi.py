#!/usr/bin/env python
"""
Consume MIDI from Kafka

"""
import sys
import mido
import time
from mido import MidiFile
from kafka import KafkaConsumer

TOPIC_NAME = 'midi'

if len(sys.argv) == 3:
    portname = sys.argv[2]
else:
    portname = None

consumer = KafkaConsumer(TOPIC_NAME)
for kafkamessage in consumer:
  print(kafkamessage.value.decode("utf-8"))
  message = mido.Message.from_str(kafkamessage.value.decode("utf-8"))
  print (message)
  mido.open_output(portname).send(message)
  
