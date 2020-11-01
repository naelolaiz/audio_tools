#!/usr/bin/python3
import sndfile
import sys
#import scipy.signal
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
    if audiofile1.channels != 1 or audiofile2.channels !=1 : 
        print("Only mono files allowed at the moment")
        sys.exit(-2)

    toReadFromAudio1 = min(audiofile1.frames, max_offset*2) if max_offset != 0 else audiofile1.frames
    toReadFromAudio2 = min(audiofile2.frames, max_offset*2) if max_offset != 0 else audiofile2.frames

    print("Reading %i frames from %s..." % (toReadFromAudio1, filename1))
    signal1 = audiofile1.read_frames("f", toReadFromAudio1)
    print("Reading %i frames from %s..." % (toReadFromAudio2, filename2))
    signal2 = audiofile2.read_frames("f", toReadFromAudio2)
    signal2_reverse = signal2[::-1]

    conv = abs(fftconvolve(signal1, signal2_reverse,  mode="full"))

    #open("conv_out.txt","w").write("\n".join(["%i: %f" % (i,f) for (i,f) in enumerate(conv)]))

    print("Max value index : " + str(toReadFromAudio2 - conv.argmax()))


if __name__ == "__main__" : main()



