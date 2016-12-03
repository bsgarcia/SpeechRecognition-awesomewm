from snowboy import snowboydecoder
from os import system

def detected_callback():
    
    launch += 1
    
    if launch >= 2:
        print "Jarvis > Oui maitre ?"
        system("python py_main.py")
    
    detector = snowboydecoder.HotwordDetector("jarviss.pmdl", sensitivity=0.37, audio_gain=1)
    detector.start(detected_callback)

global launch
launch = 0 
detected_callback()
