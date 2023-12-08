from gpiozero import Button, RotaryEncoder
from RPi import GPIO
import subprocess
from time import sleep
from osc4py3.as_eventloop import *
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
    'lydian',
    'minor'
]

SYNTH_NAME = 'sine'

TONICS = ['C', 'C#', 'D', 'D#', 'E', 'F', 
        'F#', 'G', 'G#', 'A', 'A#', 'B']

CURRENT_SCALE = SCALES[0]
CURRENT_TONIC = TONICS[0]
CURRENT_POS = 20
CURRENT_PITCHES = ['C', 'D', 'E', 'F', 'G']

IS_EDIT_MODE = True
IS_PARAM_2 = True

#################
# ROTARY CODE
#################

def handle_rotate_cw():

    # Parameter selection mode
    if not IS_EDIT_MODE:
        globals()['IS_PARAM_2'] = not IS_PARAM_2
        screen.set_cursor(int(IS_PARAM_2))
        return

    # Edit parameter mode
    if IS_EDIT_MODE:

        # Scale note selection mode
        if IS_PARAM_2:

            # if the rotary knob is at the lower limit, do nothing
            if CURRENT_POS > 34:
                return

            # update the current position of the rotary knob
            globals()['CURRENT_POS'] += 1

        # Scale selection mode
        else:
            current_scale_index = SCALES.index(CURRENT_SCALE)
            new_scale_index = (current_scale_index + 1) % len(SCALES)
            globals()['CURRENT_SCALE'] = SCALES[new_scale_index]

        # Update the buttons either way
        set_button_notes(CURRENT_TONIC, CURRENT_SCALE, CURRENT_POS)

def handle_rotate_ccw():

    # Parameter selection mode
    if not IS_EDIT_MODE:
        globals()['IS_PARAM_2'] = not IS_PARAM_2
        screen.set_cursor(int(IS_PARAM_2))
        return

    # Edit parameter mode
    if IS_EDIT_MODE:
    
        # Scale note selection mode
        if IS_PARAM_2:

            # if the rotary knob is at the lower limit, do nothing
            if CURRENT_POS < 1:
                return

            # update the current position of the rotary knob
            globals()['CURRENT_POS'] -= 1
        
        # Scale selection mode
        else:
            current_scale_index = SCALES.index(CURRENT_SCALE)
            new_scale_index = (current_scale_index - 1) % len(SCALES)
            globals()['CURRENT_SCALE'] = SCALES[new_scale_index]

        # Update the buttons either way
        set_button_notes(CURRENT_TONIC, CURRENT_SCALE, CURRENT_POS)

def handle_rotary_click():
    # Toggle IS_EDIT_MODE
    globals()['IS_EDIT_MODE'] = not IS_EDIT_MODE

    screen.set_cursor(int(IS_PARAM_2))
    screen.hide_cursor() if IS_EDIT_MODE else screen.show_cursor()

# Rotary Encoder setup code
rotary_encoder = RotaryEncoder(2, 3)
rotary_encoder.when_rotated_clockwise = handle_rotate_cw
rotary_encoder.when_rotated_counter_clockwise = handle_rotate_ccw

# Rotary button setup code
rotary_button = Button(4)
rotary_button.when_pressed = handle_rotary_click


#################
# BUTTON CODE
#################
buttons = [Button(pin) for pin in button_pins]

def set_button_notes(tonic, scale_name, pos):
    """Assigns the frequencies of the first 5 notes of the specified scale to the buttons in the buttons array.

    Args:
        tonic: The tonic of the scale.
        scale_name: The name of the scale ('major_pentatonic', 'minor_pentatonic', 'major', 'minor').
        pos: The position of the first note in the scale to assign to the first button.

    """
    # Get the music21 scale object
    music21_scale = get_scale(tonic, scale_name)

    # Get the buttons notes and set them to the global CURRENT_PITCHES
    pitches = get_button_notes(music21_scale, pos)
    globals()['CURRENT_PITCHES'] = pitches
    
    # Add the pitches to the button functions
    for i in range(5):
        # get the frequency from the pitch
        note_freq = note.Note(pitches[i]).pitch.frequency

        # apply the click function to each button with the note hardcoded
        buttons[i].when_pressed = lambda note=note_freq: play_note(note)

    # Display scale and pitches on LCD screen
    pitches_string = ' '.join(pitches)
    screen.write(scale_name, pitches_string)

def get_button_notes(scale, pos):
    """
        From a scale and the position of a rotary knob,
        return the appropriate pitches for the buttons.

        Args:
            scale - a music21 scale object
            pos - position of a rotary knob
    """

    # Get scale degrees and octaves based on rotary knob position
    scale_degrees = [(pos + i) % 5 for i in range(5)]
    octaves = [(pos + i) // 5 for i in range(5)]

    pitches = []

    # Build pitch array
    for degree, octave in zip(scale_degrees, octaves):
        # get the letter name from the scale degree of the scale
        letter = str(scale.pitchFromDegree(degree + 1))[0:-1]

        # attach it to the octave
        pitch = letter + str(octave)

        pitches.append(pitch)

    return pitches

def get_scale(tonic, scale_name):

    if scale_name == 'major':
        return scale.MajorScale(tonic)
    
    elif scale_name == 'minor':
        return scale.MinorScale(tonic)
    
    elif scale_name == 'lydian':
        return scale.LydianScale(tonic)
    
    else:
        print("Scale name not recognized.")
        return  # Exit the function if scale name is not recognized     

node_id = 1000
# Function to play a MIDI note on
def play_note(note):
    global node_id

    # Create a bundle builder to contain the message
    bundle_builder = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)

    # Create a message with osc_message_builder
    msg_builder = osc_message_builder.OscMessageBuilder("/s_new")
    msg_builder.add_arg(SYNTH_NAME)
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

def start_ocean():
    global node_id

    # Create a bundle builder to contain the message
    bundle_builder = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)

    # Create a message with osc_message_builder
    msg_builder = osc_message_builder.OscMessageBuilder("/s_new")
    msg_builder.add_arg('ocean')
    msg_builder.add_arg(node_id)  # Assuming s.nextNodeID holds the value for x

    # Build the message
    msg = msg_builder.build()

    # Add the message to the bundle
    bundle_builder.add_content(msg)

    # Send the bundle
    bundle = bundle_builder.build()
    client.send(bundle)

    globals()['node_id'] += 1

def start_ocean_sample():
    global node_id

    # Create a bundle builder to contain the message
    bundle_builder = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)

    # Create a message with osc_message_builder
    msg_builder = osc_message_builder.OscMessageBuilder("/s_new")
    msg_builder.add_arg('ocean-sample')
    msg_builder.add_arg(node_id)  # Assuming s.nextNodeID holds the value for x

    # Build the message
    msg = msg_builder.build()

    # Add the message to the bundle
    bundle_builder.add_content(msg)

    # Send the bundle
    bundle = bundle_builder.build()
    client.send(bundle)

    globals()['node_id'] += 1



# Function to play a MIDI note off
def play_midi_note_off(note):
    pass

#################
# STARTUP / SHUTDOWN
#################
SERVER_IP = "127.0.0.1"
SERVER_PORT = 57110

def startup():
    # Screen initialization
    global screen
    screen = Screen(GPIO.BCM, 16, 2, pin_lcd_rw, pin_lcd_rs, pin_lcd_e, lcd_pins[4:])
    screen.clear()
    screen.write('RASPBERRY PI', 'AMBIENT SYNTH')
    screen.set_cursor(int(IS_PARAM_2))

    # Start SuperCollider server in a subprocess
    subprocess.Popen(['sclang', 'startup.scd'])
    sleep(5) # Wait for server to boot
    print("Type 'q' to shutdown")

    # Start UDP Client to communicate with SuperCollider server
    global client
    client = udp_client.SimpleUDPClient(SERVER_IP, SERVER_PORT)

def shutdown():
    print("Shutting down program...")
    screen.clear()

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
    set_button_notes(CURRENT_TONIC, CURRENT_SCALE, CURRENT_POS)
    # start_ocean()
    start_ocean_sample()

    while True:
        sleep(0.1)  # Add a small delay

        # Let user type 'q' to shutdown
        char = sys.stdin.read(1)
        if char == "q":
            shutdown()
        
if __name__ == '__main__':
    main()