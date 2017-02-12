from snowboy import snowboydecoder  
import os

class Snowboy(object):
    
    run = 0
    
    @staticmethod 
    def write_pid_file():
        pid = "\n"+str(os.getpid())
        f = open('/home/random/Python/VoiceCommander/my_pid', 'a')
        f.write(pid)
        f.close()
    
    @classmethod
    def detected_callback(cls):
        cls.write_pid_file()
        cls.run += 1 
        
        if cls.run >= 2:
            print "Alexa > Oui maitre ?"
            os.system("python run.py")
        
        detector = snowboydecoder.HotwordDetector(
                "models/Alexa.pmdl", sensitivity=0.48, audio_gain=1)
        detector.start(cls.detected_callback)

if __name__ == '__main__':
    Snowboy.write_pid_file()
    Snowboy.detected_callback()
