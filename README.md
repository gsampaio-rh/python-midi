# python-midi

python-midi is a set of python scripts that let you send/consume MIDI messages to/from a Kafka cluster. 

There is a producer script that sends MIDI notes to a topic and there is a consumer script that reads those notes and plays them to your speakers.

# Dependencies

To run the scripts, you're going to need:

- Python `3.10.6` _(To install, follow these instructions: https://realpython.com/installing-python/)_
- pip `22.2.2` _(To install, follow these instructions: https://pip.pypa.io/en/stable/installation/)_
## Installation requirements

```
# install python scripts requirements
pip install -r requirements.txt
```
## Producer

Sends/produces MIDI notes from a MIDI file into a Kafka topic

```
# run kafka midi producer python script
python3 midi-producer-kafka.py -m $MIDI_FILE_PATH
```
### Producer options

```
usage: midi-producer-kafka.py [-h] -m MIDI_FILES 
                              [-b BOOTSTRAP_SERVERS]
                              [-t NOTES_TOPIC]
                              [--record-size RECORD_SIZE]

optional arguments:
  -h, --help            show this help message and exit
  -m MIDI_FILES, --midi-files MIDI_FILES
                        Folder with MIDI files to play
  -b BOOTSTRAP_SERVERS, --bootstrap-servers BOOTSTRAP_SERVERS
                        Bootstrap servers (defaults to 'localhost:9092')
  -t NOTES_TOPIC, --notes-topic NOTES_TOPIC
                        Topic to produce (play) notes to (defaults =
                        'midi')
  --record-size RECORD_SIZE
                        Additional payload to add to each MIDI note message to
                        match the cluster/application average message size
```
## Consumer

Receives/consumess MIDI notes from a Kafka topic

```
# run kafka midi producer python script
python3 midi-producer-kafka.py -m $MIDI_FILE_PATH
```
### Consumer options

```
usage: midi-consumer-kafka.py [-h] -m MIDI_FILES 
                              [-b BOOTSTRAP_SERVERS]
                              [-t NOTES_TOPIC]
                              [-o MIDI_OUTPUT_PORT]
                              [-v]
                              
optional arguments:
  -h, --help            show this help message and exit
  -b BOOTSTRAP_SERVERS, --bootstrap-servers BOOTSTRAP_SERVERS
                        Bootstrap servers (defaults to 'localhost:9092')
  -t NOTES_TOPIC, --notes-topic NOTES_TOPIC
                        Topic to produce (play) notes to (defaults to 'midi')
  -o MIDI_OUTPUT_PORT, --output-port MIDI_OUTPUT_PORT
                        MIDI output port
  -v, --virtual-midi-port Enables a virtual MIDI output port (midivirtualoutput)
  
```

Notes: 
> **ℹ️ NOTE:** You should adjust the number of partitions and replication factor to match your typical cluster setup.
> **ℹ️ NOTE:** Why use `--record-size`? This is optional but MIDI messages are very small and are written/read very quickly. When these messages are delayed, it's typically by milliseconds and the change in melody may not be noticeable. When this option is used, the player adds a random payload to make the messages bigger.   
