from gpiozero import Button
from mido import Message, MidiFile, MidiTrack
from time import sleep
import fluidsynth

# Keys are numbered left to right 1-5
button_pins = [26, 19, 13, 6, 5]
buttons = [Button(pin) for pin in button_pins]

midi_notes = [60, 62, 64, 65, 67]

# sample_rate = 44100

# fs = fluidsynth.Synth(sample_rate=sample_rate)
# # fs.start(driver="alsa")

# sf2_file = ""
# # fs.load_soundfont(sf2_file)

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

if __name__ == '__main__':
    try:
        map_buttons_to_midi()
    except KeyboardInterrupt:
        pass