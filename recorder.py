from subprocess import call 
import time
import numpy as np
from sys import byteorder
from array import array
from struct import pack
import os
import pyaudio
import wave


class Record(object):

    def __init__(self):
        self.THRESHOLD =  1200
        self.CHUNK_SIZE = 1024
        self.FORMAT = pyaudio.paInt16
        self.RATE = 44100

    def write_pid_file(self):
        pid = "\n" + str(os.getpid())
        f = open('my_pid', 'a')
        f.write(pid)
        f.close()

    def is_silent(self, snd_data):
        "Returns 'True' if below the 'silent' threshold"
        return max(snd_data) < self.THRESHOLD

    def normalize(self, snd_data):
        "Average the volume out"
        MAXIMUM = 16384
        times = float(MAXIMUM) / max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i * times))
        return r

    def trim(self, snd_data):
        "Trim the blank spots at the start and end"
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i) > self.THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

        # Trim to the left
        snd_data = _trim(snd_data)

        # Trim to the right
        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data

    def add_silence(self, snd_data, seconds):
        "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
        r = array('h', [0 for i in range(int(seconds * self.RATE))])
        r.extend(snd_data)
        r.extend([0 for i in range(int(seconds * self.RATE))])
        return r

    def record(self):
        """
        Record a word or words from the microphone and 
        return the data as an array of signed shorts.

        Normalizes the audio, trims silence from the 
        start and end, and pads with 0.5 seconds of 
        blank sound to make sure VLC et al can play 
        it without getting chopped off.
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=1, rate=self.RATE,
                        input=True, output=True,
                        frames_per_buffer=self.CHUNK_SIZE)
        num_silent = 0
        snd_started = False
        nb = 0
        
        r = array('h')

        while True:
            nb += 1
            data_array = np.zeros((300))
            # little endian, signed short
            snd_data = array('h', stream.read(self.CHUNK_SIZE))

            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)
            
            silent = self.is_silent(snd_data)
            
            if nb == 1:
                self.THRESHOLD = max(snd_data) + max(snd_data)/2
                t = time.time() 
            print(self.THRESHOLD, max(snd_data), num_silent) 
            print("|" * int(max(snd_data) / 33))
            np.append(snd_data, data_array)
            
            if time.time() - t >= 4.5:
                break 
            
            if not silent:
                num_silent = 0

            if silent and snd_started:
                num_silent += 1
            

            elif not silent and not snd_started:
                snd_started = True
            
            if snd_started and num_silent > 70:

                break

        print("-----------------------------------------------------")
        sample_width = p.get_sample_size(self.FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()

        os.system("clear")
        r = self.normalize(r)
        r = self.trim(r)
        r = self.add_silence(r, 0.5)

        return sample_width, r

    def record_to_file(self, path):
        "Records from the microphone and outputs the resulting data to 'path'"
        sample_width, data = self.record()
        data = pack('<' + ('h' * len(data)), *data)

        wf = wave.open(path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(self.RATE)
        wf.writeframes(data)
        wf.close()

    def launch(self):
        self.write_pid_file()
        self.record_to_file('sentences/sentence.wav')
        call(["sox", "sentences/sentence.wav", "-r", "16000","sentences/sentence.flac"])
        print("         ----------------------------------------------------- ")
                                                                      
        print("         [+] DONE - result written to sentence.flac [+]     ")
                                                                        
        print("         ----------------------------------------------------- ")     
