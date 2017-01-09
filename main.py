from snowboy import snowboydecoder
import os

class Snowboy(object):
    
    run = 0
    
    @staticmethod 
    def write_pid_file():
        pid = "\n"+str(os.getpid())
        f = open('/home/random/Python-exp/VoiceCommander/my_pid', 'a')
        f.write(pid)
        f.close()
    
    @classmethod
    def detected_callback(cls):
        cls.write_pid_file()
        cls.run += 1 
        if cls.run >= 2:
            print "Alexa > Oui maitre ?"
            os.system("python py_main.py")
        
        detector = snowboydecoder.HotwordDetector(
                "Alexa.pmdl", sensitivity=0.48, audio_gain=1)
        detector.start(cls.detected_callback)

Snowboy.write_pid_file()
Snowboy.detected_callback()
