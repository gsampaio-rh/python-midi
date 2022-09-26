#!/usr/bin/env python
"""
Play MIDI file on output port.

"""
import sys
import mido
import time
from mido import MidiFile
from kafka import KafkaProducer

FILE_NAME = "midi-files/drums-808-start-metro-139.mid"

KAFKA_SERVER = 'localhost:9092'
TOPIC_NAME = 'midi'

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

if len(sys.argv) == 3:
    portname = sys.argv[2]
else:
    portname = None

with mido.open_output(portname) as output:
    try:
        midifile = MidiFile(FILE_NAME)
        t0 = time.time()
        for message in midifile.play():
            print(message)
            # output.send(message)
            producer.send(TOPIC_NAME, message.bin())
        print('play time: {:.2f} s (expected {:.2f})'.format(
                time.time() - t0, midifile.length))

    except KeyboardInterrupt:
        print()
        producer.flush()
        output.reset()

producer.flush()
