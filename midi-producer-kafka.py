import argparse
import json
import random
from signal import signal, SIGINT
import string
from sys import exit
from sys import getsizeof
import time
from datetime import datetime

from mido import MidiFile
from confluent_kafka import Producer

from file_wildcards import files_from_wildcard


def handle_arguments():
    parser = argparse.ArgumentParser(description='Sends/produces MIDI file notes into a Kafka topic')

    parser.add_argument("-m", "--midi-files",
                        help="Folder with MIDI files to play",
                        required=True)

    parser.add_argument("-b", "--bootstrap-servers",
                        help="Bootstrap servers (defaults to 'localhost:9092')",
                        default="localhost:9092")

    parser.add_argument("-t", "--notes-topic",
                        help="Topic to produce (play) notes to (defaults = 'midi_notes')",
                        default="midi")

    parser.add_argument("--record-size",
                        help="Additional payload to add to each MIDI note message to match the cluster/application average message size",
                        type=int,
                        default=0)

    return parser.parse_args()

def delivery_report(err, msg):
    # print('delivery', err, msg)
    print('message offset', msg.offset()) 
    print('message value', msg.value()) 
    print('message size', msg.__len__()) 
    print('message latency', msg.latency()) 
    print('-----------Delivered to Kafka-----------')
    print('----------------------------------------')
    
    if err is not None:
        print('Message delivery failed: {}'.format(err))

def play_notes(producer, topic, midi_file, additional_payload_size):
    print(f"Midi File {midi_file}")
    print(f"Midi File Length {MidiFile(midi_file).length}")
    for midi_msg in MidiFile(midi_file).play():
        # print(f"Midi Message Tempo {midi_msg.time}")

        if not midi_msg.is_meta and midi_msg.type in ('note_on', 'note_off'):
            # print("KAFKA MESSAGE")
            payload = ''.join(random.choices(string.ascii_uppercase + string.digits, k=additional_payload_size)) \
                if additional_payload_size else ''
            kafka_msg = json.dumps({
                'time': midi_msg.time,
                'type': midi_msg.type,
                'channel': midi_msg.channel,
                'note': midi_msg.note,
                'velocity': midi_msg.velocity,
                'hex': midi_msg.hex(),
                # 'bytes': str(midi_msg.bin()),
                'extra_payload': payload
            })

            print('****************************************')
            print('*************Read from Midi*************')
            now = datetime.now()
            print(now)
            print(kafka_msg)

            # kafka_msg_json = json.loads(kafka_msg)
            # print(kafka_msg_json["hex"])
            producer.produce(topic, value=kafka_msg.encode('utf-8'), key=midi_file, callback=delivery_report)
            producer.poll(0)

def main():
    def ctrl_c_handler(signal_received, frame):
        # Handle any cleanup here
        print('Thank you for using Midi Player!')
        p.flush()
        exit(0)

    signal(SIGINT, ctrl_c_handler)
    args = handle_arguments()

    if args.midi_files.find('*') != -1:
        files_to_play = files_from_wildcard(args.midi_files)
    else:
        files_to_play = [args.midi_files]

    p = Producer({
                'bootstrap.servers': args.bootstrap_servers
                # 'batch.size': 100,
                # 'linger.ms': 0,
                # 'compression.type': 0,
                # 'max.in.flight.requests.per.connection': 0,
                # 'acks': 1
                })

    for f in files_to_play:
        play_notes(producer=p, topic=args.notes_topic, midi_file=f, 
                additional_payload_size=args.record_size)

    p.flush()

if __name__ == "__main__":
    main()
