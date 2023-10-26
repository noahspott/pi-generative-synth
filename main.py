from gpiozero import Button, RotaryEncoder
from mido import Message, MidiFile, MidiTrack
from time import sleep
import fluidsynth
from RPLCD.gpio import CharLCD
from RPi import GPIO

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
# FLUID SYNTH CODE
#################
# fs = fluidsynth.Synth(sample_rate=sample_rate)
# # fs.start(driver="alsa")
# sf2_file = ""
# # fs.load_soundfont(sf2_file)

#################
# LCD Screen
#################

lcd = CharLCD(numbering_mode=GPIO.BCM, cols=16, rows=2, pin_rw=pin_lcd_rw, pin_rs=pin_lcd_rs, pin_e=pin_lcd_e, pins_data=lcd_pins[4:])
lcd.write_string('Hello World')

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
midi_notes = [60, 62, 64, 65, 67]
sample_rate = 44100

def map_buttons_to_midi():
    for button, note in zip(buttons, midi_notes):
        button.when_pressed = lambda note=note: play_midi_note_on(note)
        button.when_released = lambda note=note: play_midi_note_off(note)

    while True:
        sleep(0.1)  # Add a small delay

# Function to play a MIDI note on
def play_midi_note_on(note, velocity=64):
    print(f'NOTE ON \nnote: {note}, velocity: {velocity}')
    write(f'NOTE ON note: {note}, velocity: {velocity}')
    # fs.noteon(0, note, velocity)

# Function to play a MIDI note off
def play_midi_note_off(note, velocity=0):
    print(f'NOTE OFF \nnote: {note}, velocity: {velocity}')
    write(f'NOTE OFF note: {note}, velocity: {velocity}')
    # fs.noteoff(velocity, note)

#################
# MAIN
#################
if __name__ == '__main__':
    try:
        map_buttons_to_midi()
    except KeyboardInterrupt:
        pass