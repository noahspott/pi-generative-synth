// Start supercollider server
s.waitForBoot{
    // This code runs after server is booted
    // { [SinOsc.ar(440, 0, 0.2), SinOsc.ar(442, 0, 0.2)] }.play;

    "\n".postln;
    "******************".postln;
    "* Server booted! *".postln;
    "******************".postln;
    // s.options.maxLogins = 5;

    // // Define Synth
    // SynthDef("sine", { arg freq=800;
    //     var osc;
    //     osc = SinOsc.ar(freq, 0, 0.1); // 800 Hz sine oscillator
    //     Out.ar(0, osc); // send output to audio bus zero.
    // }).writeDefFile; // write the def to disk in the default directory synthdefs/
    
    // Define "sine" Synth
    SynthDef("sine", { arg freq=800;
        // 1. Setup variables: signal, envelope, oscillator
        var sig, env, osc;

        // 2. Define the envelope: 
        env = Line.kr(1, 0, 1);

        osc = SinOsc.ar(freq, 0, 0.1); 

        sig = osc * env;

        Out.ar([0, 1], sig); // send output to audio bus zero.
    }).add; 

    // Define "saw" Synth
    SynthDef("saw", { arg freq=800;
        // 1. Setup variables: signal, envelope, oscillator
        var sig, env, osc;

        // 2. Define the envelope: 
        env = Line.kr(1, 0, 1);

        osc = LFSaw.ar(freq, 0, 0.1); 

        sig = osc * env;

        Out.ar([0, 1], sig); // send output to audio bus zero.
    }).add; 

    // SynthDef("adsr_sine_no_sustain", {
    //     arg freq=800, gate=1, amp=0.5, attack=0.01, decay=0.1, release=0.1;
        
    //     var env, osc, sig;
        
    //     // Envelope with zero sustain
    //     env = EnvGen.kr(EnvGen.ad(attack, decay, release), gate, doneAction: 2);
        
    //     // Oscillator
    //     osc = SinOsc.ar(freq, 0, 0.1); // Change frequency and other parameters as needed
        
    //     // Apply envelope to the oscillator
    //     sig = osc * env * amp;
        
    //     // Output in stereo
    //     Out.ar([0, 1], sig);
    // }).add;

    // SynthDef("envsaw",{ arg out=100, pan=0, sustain=0.5, freq=500, amp=1, cutoff=10000, rezz=1;
    // var env;
    // env = EnvGen.kr(Env.perc(0.01, sustain, 0.2), doneAction: Done.none, gate:amp);
    // Out.ar(out,Pan2.ar(RLPF.ar(Saw.ar(Lag.kr(freq,0.1),env),cutoff,rezz)*amp,
    //     pan));
    // });

    // s.sendSynthDef("sine");

    

    // n = NetAddr.new("127.0.0.1", NetAddr.langPort); // local machine

    // o = OSCFunc(
    //     { "arg msg, time, addr, recvPort; [msg, time, addr, recvPort]".postln; }, 
    //     '/note_on',
    //     nil
    // );

    // "o.enabled ".postln;
    // o.enabled.postln;

    // o = OSCFunc.new(
    //     { [SinOsc.ar(440, 0, 0.2), SinOsc.ar(442, 0, 0.2)] }.play;,
    //     "/note_on"
    // );
}
