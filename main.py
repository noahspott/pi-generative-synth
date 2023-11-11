from gpiozero import Button, RotaryEncoder
from RPi import GPIO
import mido
import subprocess
from time import sleep
import atexit
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse
import sys
from music21 import scale, note
from Screen import Screen

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
# SYNTH STATE
#################

SCALES = [
    'major',
    'minor'
]

KEYS = ['C', 'C#', 'D', 'D#', 'E', 'F', 
        'F#', 'G', 'G#', 'A', 'A#', 'B']

OCTAVES = [range(1, 8)]

CURRENT_SCALE = SCALES[0]
CURRENT_KEY = KEYS[0]
CURRENT_POS = 20

#################
# ROTARY CODE
#################

# Pin 2 = CLK (clock)
# Pin 3 = DT  (direction)
# Pin 4 = SW  (switch)

def handle_rotate_cw():
    print("rotated clockwise")
    screen.write("rotated clockwise")

    globals()['CURRENT_POS'] += 1

    print(f"current_pos: {CURRENT_POS}")

    set_button_notes(CURRENT_KEY, CURRENT_SCALE, CURRENT_POS)

def handle_rotate_ccw():
    print("rotated counter clockwise")
    screen.write("rotated counter clockwise")

    globals()['CURRENT_POS'] -= 1

    print(f"current_pos: {CURRENT_POS}")

    set_button_notes(CURRENT_KEY, CURRENT_SCALE, CURRENT_POS)


def handle_rotary_click():
    print("Rotary Press!")
    screen.write("Rotary Press!")

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
pos = 0

c_pentatonic_frequencies = [
    523.251,  # C5
    587.330,  # D5
    659.255,  # E5
    783.991,  # G5
    880.000,  # A5
]

sample_rate = 44100

def get_button_notes(scale, pos):
    """
        From a scale and the position of a rotary knob,
        return the appropriate pitches for the buttons.

        Args:
            scale - a music21 scale object
            pos - position of a rotary knob
    """

    scale_degrees = [(pos + i) % 5 for i in range(5)]
    octaves = [(pos + i) // 5 for i in range(5)]

    print(f"scale_degress: {scale_degrees}")
    print(f"octaves: {octaves}")

    pitches = []

    # Build pitch array
    for degree, octave in zip(scale_degrees, octaves):
        # get the letter name from the scale degree of the scale
        letter = str(scale.pitchFromDegree(degree + 1))[0]

        # attach it to the octave
        pitch = letter + str(octave)

        pitches.append(pitch)

    print(f"pitches: {pitches}")

    return pitches

def get_scale(tonic, scale_name):

    if scale_name == 'major':
        return scale.MajorScale(tonic)
    
    elif scale_name == 'minor':
        return scale.NaturalMinorScale(tonic)
    
    else:
        print("Scale name not recognized.")
        return  # Exit the function if scale name is not recognized


def set_button_notes(tonic, scale_name, pos):
    """Assigns the frequencies of the first 5 notes of the specified scale to the buttons in the buttons array.

    Args:
        tonic: The tonic of the scale.
        scale_name: The name of the scale ('major_pentatonic', 'minor_pentatonic', 'major', 'minor').
        pos: The position of the first note in the scale to assign to the first button.

    """

    octave = CURRENT_POS // 5
    pitch = tonic + str(octave)

    # Get the music21 scale object
    if pos < 0:
        pos += 5

    chosen_scale = get_scale(tonic, scale_name)

    # After the scale w
    pitches = get_button_notes(chosen_scale, pos)

    for i in range(5):
        note_freq = note.Note(pitches[i]).pitch.frequency

        buttons[i].when_pressed = lambda note=note_freq: play_midi_note_on(note)
        buttons[i].when_released = lambda note=note_freq: play_midi_note_off(note)



# def map_buttons_to_midi():
#     for button, note in zip(buttons, c_pentatonic_frequencies):
#         button.when_pressed = lambda note=note: play_midi_note_on(note)
#         button.when_released = lambda note=note: play_midi_note_off(note)
        

node_id = 1000
# Function to play a MIDI note on
def play_midi_note_on(note, velocity=64):
    # print(f'NOTE ON \nnote: {note}, velocity: {velocity}')
    screen.write('NOTE ON')

    global node_id

    # Create a bundle builder to contain the message
    bundle_builder = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)

    # Create a message with osc_message_builder
    msg_builder = osc_message_builder.OscMessageBuilder("/s_new")
    msg_builder.add_arg("saw")
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

    globals()['node_id'] += 1
    

# Function to play a MIDI note off
def play_midi_note_off(note, velocity=0):
    # print(f'NOTE OFF \nnote: {note}, velocity: {velocity}')
    screen.write("NOTE OFF")

    # global node_id

    # msg = osc_message_builder.OscMessageBuilder(address = '/n_free')
    # msg.add_arg(node_id)
    # msg = msg.build()
    # client.send(msg)

    # globals()['node_id'] += 1

#################
# STARTUP / SHUTDOWN
#################

process = None

server_ip = "127.0.0.1"
server_port = 57110
server_address = f"/{server_ip}:{server_port}"

client_ip = "127.0.0.2"
client_port = 5000

def startup():
    # Start SuperCollider server in a subprocess
    subprocess.Popen(['sclang', 'startup.scd'])

    # Screen initialization
    global screen
    screen = Screen(GPIO.BCM, 16, 2, pin_lcd_rw, pin_lcd_rs, pin_lcd_e, lcd_pins[4:])
    screen.write('GENERATIVE')
    screen.write('AMBIENT MACHINE', False)

    # screen.lcd.cursor_mode = 'blink'
    # print(f"Cursor Position: {screen.lcd.cursor_pos}")

    # Wait for server to boot
    sleep(5)

    global client
    client = udp_client.SimpleUDPClient(server_ip, server_port)

    # TODO: Write code to wait for server to be ready.
    # use the /status command of the server

def handle_shutdown():
    print("Shutting down program...")

    # Send /quit message to server
    msg = osc_message_builder.OscMessageBuilder(address = '/quit')
    msg.add_arg(1)
    msg = msg.build()
    client.send(msg)

    exit()

#################
# MAIN
#################

def main():
    startup()
    set_button_notes(CURRENT_KEY, CURRENT_SCALE, CURRENT_POS)

    while True:
        sleep(0.1)  # Add a small delay

        # Poll tonicboard for shutdown trigger
        char = sys.stdin.read(1)
        if char == "q":
            handle_shutdown()
        
if __name__ == '__main__':
    main()