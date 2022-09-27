import argparse
import json
from signal import signal, SIGINT
from sys import exit

import time
import mido
import rtmidi

def handle_arguments():
    parser = argparse.ArgumentParser(description='Creates a virtual MIDI port')

    parser.add_argument("-n", "--name",
                        help="Virtual Midi Port name (defaults to 'virtualmidioutport')",
                        default="virtualmidioutport")

    return parser.parse_args()

def main():
    def ctrl_c_handler(signal_received, frame):
        # Handle any cleanup here
        print('Thank you for using Python Midi Player!')
        del midiout
        exit(0)
    
    signal(SIGINT, ctrl_c_handler)
    args = handle_arguments()

    print("Starting Virtual MIDI Port")
    print()
    midiout = rtmidi.MidiOut()
    midiin = rtmidi.MidiIn()

    print('Input Ports:', mido.get_input_names())
    print('Output Ports:', mido.get_output_names())
    print()

    print("Outport name -> ",args.name)
    print()
    midiout.open_virtual_port(args.name)
    midiin.open_virtual_port(args.name)

    print('Input Ports:', mido.get_input_names())
    print('Output Ports:', mido.get_output_names())
    print()

    try:
      with mido.open_input(args.name) as port:
        print('Using {}'.format(port))
        print('Waiting for messages...')
        for message in port:
          print('Received {}'.format(message))
          sys.stdout.flush()
    except KeyboardInterrupt:
      pass

if __name__ == "__main__":
    main()
