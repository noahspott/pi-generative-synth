// Start supercollider server
s.waitForBoot{
    // This code runs after server is booted
    // { [SinOsc.ar(440, 0, 0.2), SinOsc.ar(442, 0, 0.2)] }.play;

    "\n".postln;
    "******************".postln;
    "* Server booted! *".postln;
    "******************".postln;

    s.options.maxLogins = 5;

    // // Define Synth
    // SynthDef("sine", { arg freq=800;
    //     var osc;
    //     osc = SinOsc.ar(freq, 0, 0.1); // 800 Hz sine oscillator
    //     Out.ar(0, osc); // send output to audio bus zero.
    // }).writeDefFile; // write the def to disk in the default directory synthdefs/
    
    // Define Synth
    SynthDef("sine", { arg freq=800;
        var osc;
        osc = SinOsc.ar(freq, 0, 0.1); // 800 Hz sine oscillator
        Out.ar(0, osc); // send output to audio bus zero.
    }); 

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
