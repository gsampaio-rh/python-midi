import argparse
import json
from signal import signal, SIGINT
from sys import exit
from sys import getsizeof
from datetime import datetime

import rtmidi
import mido

from confluent_kafka import Consumer  #, KafkaError
from confluent_kafka import Message

def handle_arguments():
    parser = argparse.ArgumentParser(description='Plays/consumes MIDI notes from a Kafka topic')

    parser.add_argument("-b", "--bootstrap-servers",
                        help="Bootstrap servers (defaults to 'localhost:9092')",
                        default="localhost:9092")

    parser.add_argument("-t", "--notes_topic",
                        help="Topic to consume notes from (defaults = 'midi_notes')",
                        default="midi")
    
    parser.add_argument("-o", "--output-port",
                        help="Midi output port (defaults = 'midi_notes')",
                        default="midi")
    
    parser.add_argument('-v', '--virtual-midi',
                        help="Use Virtual Midi",
                        action="store_true")

    return parser.parse_args()


def print_note(note_value):
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    # octaves = ["subsubcontra", "sub-contra", "contra", "great", "small", "one-lined", "two-lined", "three-lined", "four-lined", "five-lined", "six-lined"]
    nb_notes = 12
    # 0 to 127 assigned to C1 to G9
    octave = int((note_value / nb_notes)) + 1
    note_index = note_value % nb_notes
    note = notes[note_index]
    print(f"{note} ({octave})")


def sound_note(kafka_msg, outport):
    json_mid_msg = json.loads(kafka_msg.value())
    # print(json_mid_msg)
    
    midi_msg = mido.Message.from_bytes(bytearray.fromhex(json_mid_msg['hex']))
    
    if not midi_msg.is_meta and midi_msg.type in ('note_on', 'note_off'):
        print('note', midi_msg.note)
        if  midi_msg.type in ('note_on'):
            print('type ✅', midi_msg.type)
        if  midi_msg.type in ('note_off'):
            print('type 🔴', midi_msg.type)
        print('velocity', midi_msg.velocity)
        print('time', midi_msg.time)
        print('channel', midi_msg.channel)
        # print('hex', midi_msg.hex) 
    
    print(midi_msg)
    # print_note(midi_msg)
    # print("Send to MIDI Output Port -> " + str(outport))
    if isinstance(outport, rtmidi.MidiOut):
        outport.send_message(midi_msg.bytes())
    else:
        mido.open_output(outport).send(midi_msg)
    


def receive_notes(bootstrap_servers, notes_topic, outport):
    c = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'kmidi',
        'auto.offset.reset': 'latest'
    })

    c.subscribe([notes_topic])

    while True:
        msg = c.poll(0.1)
        
        if msg is None:
            continue
        else:
            # print(msg)
            # print('message value', msg.value())
            print ('---------------------------')
            now = datetime.now()
            print('message offset', msg.offset()) 
            print(now)
            print('message size', msg.__len__()) 
            # print('message latency', msg.latency()) 

        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        
        sound_note(msg, outport)
        past = datetime.now()
        print('Latency Kafka - Sound',past - now)

    c.close()

def main():
    def ctrl_c_handler(signal_received, frame):
        # Handle any cleanup here
        print('Thank you for using Python Midi Player!')
        outport.close()
        exit(0)

    signal(SIGINT, ctrl_c_handler)
    args = handle_arguments()
    
    if args.output_port is None:
        outport = None
    else:
        if args.virtual_midi:
            midiout = rtmidi.MidiOut()
            outport = midiout.open_virtual_port("midivirtualoutput")
        else:
            outport = args.output_port

    print("Input Ports")
    print(mido.get_input_names())
    print("Output Ports")
    print(mido.get_output_names())

    print("Output Port -> ",outport)
    # print(type(outport))

    print("Waiting for notes...")
    receive_notes(args.bootstrap_servers, args.notes_topic, outport)

if __name__ == "__main__":
    main()
