// Start supercollider server
s.waitForBoot{
    // This code runs after server is booted
    // { [SinOsc.ar(440, 0, 0.2), SinOsc.ar(442, 0, 0.2)] }.play;

    "\n".postln;
    "******************".postln;
    "* Server booted! *".postln;
    "******************".postln;
    
    // To stop the ocean, we want to set the gate to 0
    // x.set(\gate, 0)
    SynthDef("ocean", {
        // arg gate = 1;
        var sig, mod, env, amp;

        amp = 0.05;
        
        mod = SinOsc.kr(freq: 1/8, phase: 3pi/2, mul: 0.5, add: 0.5);

        // env = EnvGen.kr(
        //     envelope: Env(
        //         levels: [0, 1, 0],
        //         times: [4, 4],
        //         curve: [-1, -1],
        //         releaseNode: 1
        //     ),
        //     gate: gate,
        //     doneAction: 2
        // );

        sig = PinkNoise.ar(amp);

        sig = sig * mod;

        // Send the signal to the output
        Out.ar([0, 1], sig);
    }).add;

    // Define "sine" Synth
    SynthDef("sine", { arg freq=800;
        // 1. Setup variables: signal, envelope, oscillator
        var sig, env, osc, mod, modWidth;

        modWidth = 20;

        mod = SinOsc.kr(freq: 4).bipolar(modWidth);

        // 2. Define the envelope: 
        env = XLine.kr(start: 1, end: 0.001, dur: 4, doneAction: 2);

        // 3. Define the oscillator
        osc = SinOsc.ar(freq + mod, 0, 0.1); 

        // Combine the oscillator with the envelope
        sig = osc * env;

        // Send the signal to the output
        Out.ar([0, 1], sig);
    }).add; 

    // Define "saw" Synth
    SynthDef("saw", { arg freq=800;
        // 1. Setup variables: signal, envelope, oscillator
        var sig, env, osc, attack, decay;

        attack = 0.1;
        decay = 5;

        // 2. Define the envelope: 
        env = EnvGen.kr(
            envelope: Env(
                levels: [0, 1, 0],
                times: [attack, decay],
                curve: [5, -10]
            ),
            doneAction: 2
        );

        osc = Saw.ar(freq: freq, mul: 0.1, add: 0); 

        sig = osc * env;

        Out.ar([0, 1], sig); // send output to audio bus zero.
    }).add; 

    // Define "triangle" Synth
    SynthDef("triangle", { arg freq=800;
        // 1. Setup variables: signal, envelope, oscillator
        var sig, env, osc;

        // 2. Define the envelope: 
        env = Line.kr(1, 0, 1);

        osc = LFTri.ar(freq: freq, iphase: Rand(0, 2), mul: 0.1, add: 0); 

        sig = osc * env;

        Out.ar([0, 1], sig); // send output to audio bus zero.
    }).add; 

    // Define "pulse" Synth
    SynthDef("pulse", { arg freq=800;
        // 1. Setup variables: signal, envelope, oscillator
        var sig, env, osc;

        freq = freq.lag(2);

        // 2. Define the envelope: 
        env = Line.kr(1, 0, 1);

        osc = LFPulse.ar(freq: freq, width: Rand(), mul: 0.1, add: 0); 

        sig = osc * env;

        Out.ar([0, 1], sig); // send output to audio bus zero.
    }).add; 

    // Define "pulse" Synth
    SynthDef("noise", { arg freq=800;

        // var sig = LFPulse.ar(freq: freq, width: Rand(), mul: 0.1, add: 0);
        
        var sig = Decay.ar(
            in: LFPulse.ar(freq: freq, width: Rand(), add: 0), 
            decayTime: 1, 
            mul: 0.1, 
            add: 0
        );

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
