# pi-generative-synth

## Install
<b>Follow these instructions to install supercollider on RPI: </b><br/>
https://github.com/supercollider/supercollider/blob/develop/README_RASPBERRY_PI.md

## Setup Audio I/O
<b>Create your Jack configuration file:</b><br/>
"dhw:3" is your desired audio I/O device. For me, that is my audio interface.<br/>
<pre>
echo /usr/bin/jackd -P75 -dalsa -dhw:3 -r44100 -p512 -n3 > ~/.jackdrc
</pre>
You might want to change your audio I/O device. To see your available devices:
<pre>
aplay -l
</pre>

## Startup
### Setup Environment
Make sure your terminal is in the appropriate environment. For my system, I created an environment called synthenv with the associated dependencies.
<pre>
. ~/synthenv/bin/activate
</pre>

### Setup Audio Interface
Make sure your audio interface is connected and turned on!

### 
Run main
<pre>
python3 main.py
</pre>
