from gpiozero import Button

class SynthKey:
    def __init__(self, pin):
        self.button = Button(pin)
        self.is_pressed = False
        self._note = None
        self.button.when_pressed = self.on_press
        self.button.when_released = self.on_release

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, value):
        self._note = value

    def on_press(self):
        self.is_pressed = True
        print(f"Button pressed. Note: {self.note}")

    def on_release(self):
        self.is_pressed = False
        print("Button released")