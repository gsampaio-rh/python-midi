#!/usr/bin/env python
#
# Copyright 2016 Confluent Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# Example Kafka Producer.
# Reads lines from stdin and sends to Kafka.
#

from confluent_kafka import Producer
import sys
import mido
import time
from mido import MidiFile

FILE_NAME = "midi-files/drums-808-start-metro-139.mid"

KAFKA_SERVER = 'localhost:9092'
TOPIC_NAME = 'midi'

if __name__ == '__main__':

    broker = "localhost:9092"
    topic = "midi"

    # Producer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    conf = {'bootstrap.servers': broker}

    # Create Producer instance
    p = Producer(**conf)

    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(err, msg):
      if err:
        sys.stderr.write('%% Message failed delivery: %s\n' % err)
      else:
        sys.stderr.write('%% Message delivered to %s [%d] @ %d\n' %
                          (msg.topic(), msg.partition(), msg.offset()))

    # Read lines from stdin, produce each line to Kafka
    try:
      midifile = MidiFile(FILE_NAME)
      t0 = time.time()
      for message in midifile.play():
        print(message)
        try:
          # Produce line (without newline)
          p.produce(topic, str(message), callback=delivery_callback)

        except BufferError:
          sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' %
                          len(p))

        # Serve delivery callback queue.
        # NOTE: Since produce() is an asynchronous API this poll() call
        #       will most likely not serve the delivery callback for the
        #       last produce()d message.
        p.poll(0)
      print('play time: {:.2f} s (expected {:.2f})'.format(
              time.time() - t0, midifile.length))

      # Wait until all messages have been delivered
      sys.stderr.write('%% Waiting for %d deliveries\n' % len(p))
      p.flush()

    except KeyboardInterrupt:
      print()
      p.flush()
      output.reset()  
