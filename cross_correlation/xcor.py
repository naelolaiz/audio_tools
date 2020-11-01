#!/usr/bin/python3
import sndfile
import sys
from scipy.signal import fftconvolve

def main() : 
    if(len(sys.argv) < 3) :
        print("Usage: %s file1 file2 [max_offset]" % sys.argv[0])
        sys.exit(-1)
    
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    max_offset = int(sys.argv[3]) if len(sys.argv) == 4 else 0
    audiofile1 = sndfile.open(filename1)
    audiofile2 = sndfile.open(filename2)
    if audiofile1.channels != audiofile2.channels : 
        print("Channel count must match")
        sys.exit(-2)
    channelCount = audiofile1.channels

    toReadFromAudio1 = min(audiofile1.frames, max_offset*2) if max_offset != 0 else audiofile1.frames
    toReadFromAudio2 = min(audiofile2.frames, max_offset*2) if max_offset != 0 else audiofile2.frames

    print("Reading %i frames from %s..." % (toReadFromAudio1, filename1))
    signal1 = audiofile1.read_frames("f", toReadFromAudio1)
    print("Reading %i frames from %s..." % (toReadFromAudio2, filename2))
    signal2_reverse = audiofile2.read_frames("f", toReadFromAudio2)[::-1]

    for channel in range(channelCount) :
        channelSignal1 = [f for (i,f) in enumerate(signal1) if i % channelCount == channel]
        channelSignal2Reverse = [f for (i,f) in enumerate(signal2_reverse) if i % channelCount == channel]

        conv = abs(fftconvolve(channelSignal1,  channelSignal2Reverse,  mode="full"))
        #open("conv_out.txt","w").write("\n".join(["%i: %f" % (i,f) for (i,f) in enumerate(conv)]))

        print("Max value index for channel %i: %i" % (channel, (toReadFromAudio2 - conv.argmax())))

if __name__ == "__main__" : main()



