from gpiozero import Button, RotaryEncoder
from RPLCD.gpio import CharLCD
from RPi import GPIO
from mido import Message, MidiFile, MidiTrack
import subprocess
from time import sleep
import atexit
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse
import sys

from pythonosc import udp_client, osc_message_builder, osc_bundle_builder

"""

Pin Map Legend:

    2  - rotary: CLK                
    3  - rotary: DT
    4  - rotary: SW             14 - 
                                15 - 
    17 - lcd: rw                18 - 
    27 - lcd: rs                     
    22 - lcd: e                 23 - 
                                24 - 
    10 -
    9  -                        25 - 
    11 -                        8  -
                                7  -
    
    5  - Button 5 (leftmost)
    6  - Button 4               12 -
    13 - Button 3               
    19 - Button 2               16 -
    26 - Button 1 (rightmost)   20 -
                                21 -

"""    

#################
# PINS
#################

pin_rotary_clk = 2
pin_rotary_dt = 3
pin_rotary_sw = 4

pin_lcd_rw = 17
pin_lcd_rs = 27
pin_lcd_e = 22

pin_lcd_d0 = None
pin_lcd_d1 = None
pin_lcd_d2 = None
pin_lcd_d3 = None

pin_lcd_d4 = 23
pin_lcd_d5 = 18
pin_lcd_d6 = 15
pin_lcd_d7 = 14

lcd_pins = [pin_lcd_d0, pin_lcd_d1, pin_lcd_d2, pin_lcd_d3, 
            pin_lcd_d4, pin_lcd_d5, pin_lcd_d6, pin_lcd_d7]

# Keys are numbered left to right 1-5
button_pins = [26, 19, 13, 6, 5]

#################
# LCD Screen
#################

lcd = CharLCD(numbering_mode=GPIO.BCM, 
              cols=16, rows=2, 
              pin_rw=pin_lcd_rw, pin_rs=pin_lcd_rs, pin_e=pin_lcd_e, pins_data=lcd_pins[4:])
lcd.write_string('GENERATIVE\n\rAMBIENT MACHINE')
lcd.cursor_mode = 'blink'

print(lcd.cursor_pos)

def write(message):
    lcd.clear()
    lcd.write_string(message)


#################
# ROTARY CODE
#################

# Pin 2 = CLK (clock)
# Pin 3 = DT  (direction)
# Pin 4 = SW  (switch)

def handle_rotate_cw():
    print("rotated clockwise")
    write("rotated clockwise")


def handle_rotate_ccw():
    print("rotated counter clockwise")
    write("rotated counter clockwise")

def handle_rotary_click():
    print("Rotary Press!")
    write("Rotary Press!")

rotary_encoder = RotaryEncoder(2, 3)
rotary_encoder.when_rotated_clockwise = handle_rotate_cw
rotary_encoder.when_rotated_counter_clockwise = handle_rotate_ccw

rotary_button = Button(4)
rotary_button.when_pressed = handle_rotary_click


#################
# BUTTON MIDI CODE
#################

buttons = [Button(pin) for pin in button_pins]
midi_notes = [500, 700, 900, 1100, 1300]
sample_rate = 44100

def map_buttons_to_midi():
    for button, note in zip(buttons, midi_notes):
        button.when_pressed = lambda note=note: play_midi_note_on(note)
        button.when_released = lambda note=note: play_midi_note_off(note)
        

node_id = 1000
# Function to play a MIDI note on
def play_midi_note_on(note, velocity=64):
    print(f'NOTE ON \nnote: {note}, velocity: {velocity}')
    write(f'NOTE ON note: {note}, velocity: {velocity}')

    global node_id

    # Create a bundle builder to contain the message
    bundle_builder = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)

    # Create a message with osc_message_builder
    msg_builder = osc_message_builder.OscMessageBuilder("/s_new")
    msg_builder.add_arg("sine")
    msg_builder.add_arg(node_id)  # Assuming s.nextNodeID holds the value for x
    msg_builder.add_arg(1)
    msg_builder.add_arg(1)
    msg_builder.add_arg("freq")
    msg_builder.add_arg(note)

    # Build the message
    msg = msg_builder.build()

    # Add the message to the bundle
    bundle_builder.add_content(msg)

    # Send the bundle
    bundle = bundle_builder.build()
    client.send(bundle)
    

# Function to play a MIDI note off
def play_midi_note_off(note, velocity=0):
    print(f'NOTE OFF \nnote: {note}, velocity: {velocity}')
    write(f'NOTE OFF note: {note}, velocity: {velocity}')

    global node_id

    msg = osc_message_builder.OscMessageBuilder(address = '/n_free')
    msg.add_arg(node_id)
    msg = msg.build()
    client.send(msg)

    globals()['node_id'] += 1

#################
# STARTUP
#################

process = None

server_ip = "127.0.0.1"
server_port = 57110
server_address = f"/{server_ip}:{server_port}"

client_ip = "127.0.0.2"
client_port = 5000

def startup():
    # Start SuperCollider server in a subprocess
    # subprocess.Popen(['sclang', 'startup.scd'])
    # Wait for server to boot
    # sleep(5)

    global client
    client = udp_client.SimpleUDPClient(server_ip, server_port)

    # TODO: Write code to wait for server to be ready.
    # use the /status command of the server

    # Create a new synth??
    # msg = osc_message_builder.OscMessageBuilder(address = '/s_new')
    # msg.add_arg("sine", arg_type='s')
    # msg = msg.build()
    # client.send(msg)

    # Register to receive notifications from server with /notify
    msg = osc_message_builder.OscMessageBuilder(address = '/notify')
    msg.add_arg(1)
    msg = msg.build()
    client.send(msg)


#################
# MAIN
#################

def handle_shutdown():
    print("Shutting down program...")

    # Send /quit message to server
    msg = osc_message_builder.OscMessageBuilder(address = '/quit')
    msg.add_arg(1)
    msg = msg.build()
    client.send(msg)

    exit()

def main():
    startup()
    map_buttons_to_midi()

    while True:
        sleep(0.1)  # Add a small delay

        # Poll keyboard for shutdown trigger
        char = sys.stdin.read(1)
        if char == "q":
            handle_shutdown()
        
if __name__ == '__main__':
    main()