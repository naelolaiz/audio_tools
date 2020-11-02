#!/usr/bin/python3
import sys
from scipy.signal import fftconvolve
import soundfile as sf
import numpy as np

def convolve_arrays(signal_input, signal_IR) : 
    input_channel_count = 1 if len(signal_input.shape)==1 else signal_input.shape[1]
    IR_channel_count = 1 if len(signal_IR.shape)==1 else signal_IR.shape[1]
    output_sample_count = signal_input.shape[0] + signal_IR.shape[0] - 1

    conv_signals = np.ndarray((input_channel_count, output_sample_count))

    #print(conv_signals.shape)
    for channel in range(input_channel_count) :
        channel_signal_input = signal_input.transpose()[channel]  if input_channel_count !=1 else signal_input
        channel_signal_IR = signal_IR.transpose()[channel] if IR_channel_count != 1 else signal_IR
        conv_signals[channel] = fftconvolve(channel_signal_input,  channel_signal_IR,  mode="full")
        #open("conv_out.txt","w").write("\n".join(["%i: %f" % (i,f) for (i,f) in enumerate(conv)]))

    return conv_signals

def convolve_files (filename_input, filename_IR, filename_output) :
    audiofile_input = sf.SoundFile(filename_input)
    audiofile_IR = sf.SoundFile(filename_IR)

    if audiofile_input.channels != audiofile_IR.channels and audiofile_IR.channels != 1:
        print("IR channel count must be either 1 or the same as the input file")
        sys.exit(-2)

    to_read_from_audio_input = audiofile_input.frames
    to_read_from_audio_IR = audiofile_IR.frames
    print("Reading %i frames in %i channel(s) from %s..." % (to_read_from_audio_input, audiofile_input.channels, filename_input))
    signal_input = audiofile_input.read(to_read_from_audio_input)
    print("Reading %i frames in %i channel(s) from %s..." % (to_read_from_audio_IR, audiofile_IR.channels, filename_IR))
    signal_IR = audiofile_IR.read(to_read_from_audio_IR)

    #print ("==",signal_input.shape)
    #print ("==",signal_IR.shape)

    conv_signals = convolve_arrays(signal_input, signal_IR)
    
    # todo: check that matches conv_signals.shape
    output_channel_count = audiofile_input.channels # should be the same as the input
    output_sample_count  = audiofile_input.frames + audiofile_IR.frames - 1

    outputfile = sf.SoundFile(filename_output, "w", audiofile_input.samplerate, output_channel_count)
    print("Writting %i channels of %i frames to %s..." % (output_channel_count, output_sample_count, filename_output))
    outputfile.write(np.array(conv_signals).transpose())

def main() : 
    if(len(sys.argv) < 4) :
        print("Usage: %s file_input IR_input file_out " % sys.argv[0])
        sys.exit(-1)
    
    filename_input = sys.argv[1]
    filename_IR = sys.argv[2]
    filename_output = sys.argv[3]
    convolve_files(filename_input, filename_IR, filename_output)

if __name__ == "__main__" : main()

