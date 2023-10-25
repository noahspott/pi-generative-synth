from gpiozero import Button, RotaryEncoder
from mido import Message, MidiFile, MidiTrack
from time import sleep
import fluidsynth

"""
Pin Map Legend:
    2  - rotary: CLK
    3  - rotary: DT
    4  - rotary: SW

    5  - Button 5 (leftmost)
    6  - Button 4
    13 - Button 3
    19 - Button 2
    26 - Button 1 (rightmost)
"""

# Keys are numbered left to right 1-5
button_pins = [26, 19, 13, 6, 5]
buttons = [Button(pin) for pin in button_pins]

midi_notes = [60, 62, 64, 65, 67]

sample_rate = 44100

#################
# FLUID SYNTH CODE
#################
# fs = fluidsynth.Synth(sample_rate=sample_rate)
# # fs.start(driver="alsa")
# sf2_file = ""
# # fs.load_soundfont(sf2_file)


#################
# ROTARY CODE
#################

# Pin 2 = CLK (clock)
# Pin 3 = DT  (direction)
# Pin 4 = SW  (switch)

def handle_rotate_cw():
    print("rotated clockwise")

def handle_rotate_ccw():
    print("rotated counter clockwise")

def handle_rotary_click():
    print("Rotary Press!")

rotary_encoder = RotaryEncoder(2, 3)
rotary_encoder.when_rotated_clockwise = handle_rotate_cw
rotary_encoder.when_rotated_counter_clockwise = handle_rotate_ccw

rotary_button = Button(4)
rotary_button.when_pressed = handle_rotary_click


#################
# BUTTON MIDI CODE
#################

def map_buttons_to_midi():
    for button, note in zip(buttons, midi_notes):
        button.when_pressed = lambda note=note: play_midi_note_on(note)
        button.when_released = lambda note=note: play_midi_note_off(note)

    while True:
        sleep(0.1)  # Add a small delay

# Function to play a MIDI note on
def play_midi_note_on(note, velocity=64):
    print(f'NOTE ON \nnote: {note}, velocity: {velocity}')
    # fs.noteon(0, note, velocity)

# Function to play a MIDI note off
def play_midi_note_off(note, velocity=0):
    print(f'NOTE OFF \nnote: {note}, velocity: {velocity}')
    # fs.noteoff(velocity, note)


#################
# MAIN
#################
if __name__ == '__main__':
    try:
        map_buttons_to_midi()
    except KeyboardInterrupt:
        pass