import argparse
import logging
from signal import signal, SIGINT
from sys import exit
from datetime import datetime

import rtmidi

import mido
from mido import MidiFile

from file_wildcards import files_from_wildcard


def handle_arguments():
    parser = argparse.ArgumentParser(description='Sends/produces MIDI file notes into a Kafka topic')

    parser.add_argument("-m", "--midi-files",
                        help="Folder with MIDI files to play",
                        required=True)
    
    parser.add_argument("-o", "--output-port",
                        help="Midi output port (defaults = 'midi_notes')",
                        default="midi")

    parser.add_argument('-d', '--debug',
                        help="Print lots of debugging statements",
                        action="store_const", dest="loglevel", const=logging.DEBUG,
                        default=logging.WARNING)
    
    parser.add_argument('-v', '--verbose',
                        help="Be verbose",
                        action="store_const", dest="loglevel", const=logging.INFO)

    return parser.parse_args()

def play_notes(midi_file, outport):
    # print(f"Playing {midi_file}... at {speed_ratio}")
    print(f"Midi File {midi_file}")
    print(f"Midi File Length {MidiFile(midi_file).length}")
    tnotes = 0
    for midi_msg in MidiFile(midi_file).play():
        print(f"Midi Message Tempo {midi_msg.time}")

        if not midi_msg.is_meta and midi_msg.type in ('note_on', 'note_off'):
            print ('---------------------------')
            print('note', midi_msg.note)
            if  midi_msg.type in ('note_on'):
                print('type ✅', midi_msg.type)
            if  midi_msg.type in ('note_off'):
                print('type 🔴', midi_msg.type)
            print('velocity', midi_msg.velocity)
            print('time', midi_msg.time)
            print('channel', midi_msg.channel)
            now = datetime.now()
            print(now)
            
            # mido.open_output(outport).send(midi_msg)
            outport.send_message(midi_msg.bytes())
            tnotes = tnotes + 1
            print('counter ->',tnotes)
            print ('---------------------------')
            print()


def main():
    def ctrl_c_handler(signal_received, frame):
        # Handle any cleanup here
        print('Thank you for using Midi Player!')
        outport.reset()
        outport.close()
        exit(0)

    signal(SIGINT, ctrl_c_handler)
    args = handle_arguments()

    logging.basicConfig(level=args.loglevel)

    if args.midi_files.find('*') != -1:
        files_to_play = files_from_wildcard(args.midi_files)
    else:
        files_to_play = [args.midi_files]
    
    if args.output_port is None:
        outport = args.output_port
    else:
        # outport = None
        midiout = rtmidi.MidiOut()
        outport = midiout.open_virtual_port("midivirtualoutput")

    for f in files_to_play:
        play_notes(midi_file=f, outport=outport)

    print('Thank you for using Midi Player!')


if __name__ == "__main__":
    main()
