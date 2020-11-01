#!/usr/bin/python3
import sndfile
import sys
from scipy.signal import fftconvolve
import soundfile # TODO: use either sndfile or soundfile, but not both. preferibly the last, to use only numpy arrays
import numpy as np

def main() : 
    if(len(sys.argv) < 4) :
        print("Usage: %s file_input IR_input file_out " % sys.argv[0])
        sys.exit(-1)
    
    filename_input = sys.argv[1]
    filename_IR = sys.argv[2]
    filename_out = sys.argv[3]
    audiofile_input = sndfile.open(filename_input)
    audiofile_IR = sndfile.open(filename_IR)

    if audiofile_input.channels != audiofile_IR.channels and audiofile_IR.channels != 1:
        print("IR channel count must be either 1 or the same as the input file")
        sys.exit(-2)

    to_read_from_audio_input = audiofile_input.frames
    to_read_from_audio_IR = audiofile_IR.frames
    print("Reading %i frames from %s..." % (to_read_from_audio_input, filename_input))
    signal_input = audiofile_input.read_frames("f", to_read_from_audio_input)
    print("Reading %i frames from %s..." % (to_read_from_audio_IR, filename_IR))
    signal_IR = audiofile_IR.read_frames("f", to_read_from_audio_IR)

    conv_signals = []
    channelCount = audiofile_input.channels
    for channel in range(channelCount) :
        channel_signal_input = [f for (i,f) in enumerate(signal_input) if i % channelCount == channel]
        channel_signal_IR = [f for (i,f) in enumerate(signal_IR) if i % channelCount == channel] if audiofile_IR.channels != 1 else signal_IR
        conv_signals += [fftconvolve(channel_signal_input,  channel_signal_IR,  mode="full")]
        #open("conv_out.txt","w").write("\n".join(["%i: %f" % (i,f) for (i,f) in enumerate(conv)]))


    outputfile = soundfile.SoundFile(filename_out, "w", audiofile_input.samplerate, audiofile_input.channels)
    print("Writting %i frames to %s..." % (len(conv_signals[0]), filename_out))
    outputfile.write(np.array(conv_signals).transpose())

if __name__ == "__main__" : main()



