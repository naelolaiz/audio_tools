#!/usr/bin/python3
import soundfile as sf
import sys
from scipy.signal import fftconvolve

def main() : 
    if(len(sys.argv) < 3) :
        print("Usage: %s file1 file2 [max_offset]" % sys.argv[0])
        sys.exit(-1)
    
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    max_offset = int(sys.argv[3]) if len(sys.argv) == 4 else 0
    audiofile1 = sf.SoundFile(filename1)
    audiofile2 = sf.SoundFile(filename2)

    if audiofile1.channels != audiofile2.channels : 
        print("Channel count must match")
        sys.exit(-2)
    channel_count = audiofile1.channels

    to_read_from_audio_1 = min(audiofile1.frames, max_offset*2) if max_offset != 0 else audiofile1.frames
    to_read_from_audio_2 = min(audiofile2.frames, max_offset*2) if max_offset != 0 else audiofile2.frames

    print("Reading %i frames from %s..." % (to_read_from_audio_1, filename1))
    signal1 = audiofile1.read(to_read_from_audio_1)

    print("Reading %i frames from %s..." % (to_read_from_audio_2, filename2))
    signal2_reverse = audiofile2.read(to_read_from_audio_2)[::-1]


    for channel in range(channel_count) :
        channel_signal_1 = signal1.transpose()[channel] if channel_count>1 else signal1
        channel_signal_2_reverse = signal2_reverse.transpose()[channel] if channel_count>1 else signal2_reverse
        conv = abs(fftconvolve(channel_signal_1,  channel_signal_2_reverse,  mode="full"))
#        #open("conv_out.txt","w").write("\n".join(["%i: %f" % (i,f) for (i,f) in enumerate(conv)]))
        offset_found = to_read_from_audio_2 - conv.argmax()
        print("Max value index for channel %i: %i (%s has a delay of %i samples with regard to %s)" % (channel, offset_found, filename2, offset_found, filename1))

if __name__ == "__main__" : main()

