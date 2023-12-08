// Increase Server's realtime memory
s.options.memSize_(65536 * 4);

// Start supercollider server
s.waitForBoot{
    // This code runs after server is booted
    "\n".postln;
    "******************".postln;
    "* Server booted! *".postln;
    "******************".postln;

    // Load ocean sample into buffer to be read
    b = Buffer.read(s, "ocean.wav");

    // Define "sine" Synth
    SynthDef("sine", { arg freq=800;
        var sig, sig2, env, osc, osc2, pitchMod, pitchModWidth, panMod, newFreq, cFreq, delay1, delay2, cMajor, randomCentAdjuster;

        // This is just a long envelope to kill the process after verb tail
        Line.kr(0, 0, 30, doneAction:2);

        newFreq = freq;

        // modulator for pitch modulation
        pitchModWidth = 5;
        pitchMod = SinOsc.kr(freq: 0.5).bipolar(pitchModWidth);
        
        // oscillator - sine wave
        osc = SinOsc.ar(newFreq + pitchMod, 0, 0.1); 

        // oscillator 2 - sin wave with random scale adjustment to pitch

        // This code makees osc2 have the frequency of a random note in Cmaj
        // cMajor = Scale.major();
        // randomCentAdjuster = cMajor.cents.choose;
        // osc2 = SinOsc.ar(freq + randomCentAdjuster, 0, 0.1); 

        // Get first frequency of c major scale
        cFreq = Scale.major.degreeToFreq(1, 60.midicps, 1);
        osc2 = SinOsc.ar(cFreq, 0, 0.1); 

        // envelope 
        env = XLine.kr(start: 1, end: 0.001, dur: 4, doneAction: 0);
        
        sig = osc * env;
        sig2 = osc2 * env * 0.1;

        sig = sig + sig2;

        sig = FreeVerb2.ar(sig, sig, 0.3, 0.99);

        // Add delays
        delay1 = DelayN.ar(sig, 1, 1);
        delay2 = DelayN.ar(sig, 2, 2);

        sig = sig.blend([delay1, delay2], 0.5);

        // Pan the signal between ears
        panMod = SinOsc.kr(freq: 1);
        sig = Pan2.ar(sig, panMod);

        Out.ar(0, sig);
    }).add; 

    // Define "saw" Synth
    SynthDef("saw", { arg freq=800;
        // 1. Setup variables: signal, envelope, oscillator
        var sig, env, osc, attack, decay, lpfFreq;

        attack = 0.1;
        decay = 5;

        lpfFreq = 2000;

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

        sig = LPF.ar(sig, lpfFreq);


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



    // ------------------
    // NOISE / FIELD RECORDINGS
    // ------------------
    SynthDef("ocean-sample", {
        var sig, amp;

        amp = 0.9;

        sig = PlayBuf.ar(
            numChannels: 2,
            bufnum: \buf.kr(0),
            rate: BufRateScale.kr(\buf.kr(0)),
            loop: 1
        );

        sig = sig * amp;

        Out.ar(\out.kr(0), sig);
    }).add;
    
    SynthDef("ocean", {
        // arg gate = 1;
        var sig, mod, env, amp;

        amp = 0.1;
        
        mod = SinOsc.kr(freq: 1/8, phase: 3pi/2, mul: 0.5, add: 0.5);

        sig = PinkNoise.ar(amp);

        sig = sig * mod;

        sig = FreeVerb2.ar(sig, sig, 1, 0.99);

        // Send the signal to the output
        Out.ar(0, sig);
    }).add;
};
