(
// Create a SynthDef for a monophonic sine wave synth
SynthDef(\sineSynth, {
    arg freq = 440, amp = 0.5;
    var sig;
    sig = SinOsc.ar(freq, 0, amp);
    Out.ar(0, sig);
}).add;
)

// Set up a MIDIIn object to receive key presses
m = MIDIIn.new;

// Function to respond to key presses
(
m.noteOn = { |vel, num, chan, src|
    if (num == 60, {  // Change 60 to the MIDI note number you want to trigger
        Synth.new(\sineSynth, [\freq, num.midicps, \amp, vel.linlin(0, 127, 0, 1)]);
    })
};
)

// Function to handle key release
(
m.noteOff = { |vel, num, chan, src|
    if (num == 60, {
        s.queryAll({ |node|
            if (node.isKindOf(Synth) && { node.synthDef.name == \sineSynth }, {
                node.free;
            });
        });
    })
};
)