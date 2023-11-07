# pi-generative-synth

## Install
<b>Follow these instructions to install supercollider on RPI: </b><br/>
https://github.com/supercollider/supercollider/blob/develop/README_RASPBERRY_PI.md

## Setup Audio I/O
<b>Create your Jack configuration file:</b><br/>
```echo /usr/bin/jackd -P75 -dalsa -dhw:3 -r44100 -p512 -n3 > ~/.jackdrc```<br/>
"dhw:3" is your desired audio I/O device. To see your available devices run ```aplay -l```.

## Startup
### SuperCollider Server
Open a new terminal on your RPI and run:
- ```sclang```
- ```s.boot```
