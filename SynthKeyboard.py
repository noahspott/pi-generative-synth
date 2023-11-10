import SynthKey
import music21

class SynthKeyboard:
    def __init__(self, pins):
        self.keys = [SynthKey(pin) for pin in pins]
        self.set_notes(["C4", "D4", "E4", "F4", "G4"])  # Set initial notes

    def set_notes(self, notes):
        if len(notes) == len(self.keys):
            for i, note in enumerate(notes):
                self.keys[i].note = note
        else:
            print("Error: Number of notes does not match the number of keys")

    def play(self):
        while True:
            pass  # Perform other operations or keep the program running