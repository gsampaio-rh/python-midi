import mido
import time
from collections import deque

output_list = mido.get_output_names()
input_list = mido.get_input_names()

print("OUTPUT LIST")
print(output_list)# To list the output ports

print("INPUT LIST")
print(input_list) # To list the input ports

inport = mido.open_input('XONE:K2')
outport = mido.open_output('XONE:K2')

# for msg in inport:
#     print(msg)

print("Send Message 36")
outport.send(mido.Message('note_on', note=36))

print("Send Message 37")
outport.send(mido.Message('note_on', note=37))

print("Send Message 38")
outport.send(mido.Message('note_on', note=38))

print("Send Message 39")
outport.send(mido.Message('note_on', note=39))

# msglog = deque()
# echo_delay = 2

# while True:
#     while inport.pending():
#         msg = inport.receive()
#         if msg.type != "clock":
#             print (msg)
#             msglog.append({"msg": msg, "due": time.time() + echo_delay})
#     while len(msglog) > 0 and msglog[0]["due"] <= time.time():
#         outport.send(msglog.popleft()["msg"])