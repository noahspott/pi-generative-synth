from gpiozero import LED
from gpiozero import Button
# import foxdot
import time
import sys
import signal

print(sys.path)

# Keys are numbered left to right 1-5
key1 = Button(26)
key2 = Button(19)
key3 = Button(13)
key4 = Button(6)
key5 = Button(5)
keys = [key1, key2, key3, key4, key5]

# synth = foxdot.Synth()

def print_current_time():
    current_time = time.strftime("%H:%M:%S")
    print("Current time:", current_time)        

key1.when_pressed = print_current_time
key2.when_pressed = print_current_time
key3.when_pressed = print_current_time
key4.when_pressed = print_current_time
key5.when_pressed = print_current_time

try:
    while True:
        pass
except KeyboardInterrupt:

    print("Program Terminated")