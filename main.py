from snowboy import snowboydecoder
import os

def write_pid_file():
    
    pid = "\n"+str(os.getpid())
    f = open('/home/random/Python-exp/VoiceCommander/my_pid', 'a')
    f.write(pid)
    f.close()

def detected_callback():
    
    write_pid_file()
    global launch
    launch += 1
    if launch >= 2:
        print "Jarvis > Oui maitre ?"
        os.system("python py_main.py")
    
    detector = snowboydecoder.HotwordDetector("jarviss.pmdl", sensitivity=0.37, audio_gain=1)
    detector.start(detected_callback)

launch = 0
write_pid_file()
detected_callback()
