# pi-generative-synth

## Install
- Follow these instructions to install supercollider on RPI: https://github.com/supercollider/supercollider/blob/develop/README_RASPBERRY_PI.md

## Setup Audio I/O
Creat your Jack configuration file:<br/>
```echo /usr/bin/jackd -P75 -dalsa -dhw:3 -r44100 -p512 -n3 > ~/.jackdrc```
- "dhw:3" is going to be your desired audio I/O device. To see your available devices run ```aplay -l``` in the terminal.

## Startup
### SuperCollider Server
- Open a new terminal and run ```sclang```
