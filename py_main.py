from os import system, path, walk, popen, getpid
from notify import notify
from subprocess import call, Popen
from recorder import Record
from gtts import gTTS
from googlespeech import SpeechRecog
import re
import time
import numpy as np


class Recognizer(object):

    #--------------------------------------------------------------#

    def __init__(self):
        
        
        self.icon = "/home/random/.config/awesome/themes/powerarrow-darker/icons/micon_on.png"
        self.end = False
        self.prog = {
            "chromium": ["chrome", "chromium"],
            "firefox": ["firefox", "firefoxe", "light"],
            "gvim": ["vim", "vime", "gvim", "j'ai vim", "j'ai vime", "programmer"],
            "mpv": ["lecteur", "mpv"]
        }
        self.directory = "/run/media/random/DATA/Animes/"
   #--------------------------------------------------------------#
    
    def record_and_read(self):

        r = Record()
        r.launch()
        speech = SpeechRecog.get_answer_from_google()        
        
        return speech
   #--------------------------------------------------------------#

    def play_answer(self, a, i, *text):
    
        if not path.isfile("answers/{}_{}.mp3".format(a, i)):
            tts = gTTS(
                        text="Très bien, je {} {}...".format(a, i), lang="fr")
            tts.save("answers/{}_{}.mp3".format(a,i))
        notify("Très bien, je {} {} ... ".format(a, i), self.icon)
        Popen(["mpv", "answers/{}_{}.mp3".format(a, i)])
        self.end = True

   #--------------------------------------------------------------#
 
    def parser(self, speech):

        for i, j in self.prog.items():
            for k in j:
                if k in speech:
                    self.play_answer('lance', i)
                    Popen(["{}".format(i), ""])
                    break
        
        self.launch_other_stuff(speech)

    #--------------------------------------------------------------#

    def launch_other_stuff(self, speech):
        
        if "musique" in speech:

            Popen(
                ["mpv", "/run/media/random/DATA2/SoulseekDownloads/complete/Musique_djam"])
            self.end = True

        if "merci" in speech:
            if not path.isfile("answers/merci.mp3"):
                tts = gTTS(
                    text="Mais de rien mon seigneur, je voue mon existence à votre service", lang="fr")
                tts.save("answers/merci.mp3")
            notify("Mais de rien mon seigneur, je voue mon existence à votre service", self.icon)
            Popen(["mpv", "answers/merci.mp3"])
            self.end = True

        if "religion" in speech:
            if not path.isfile("answers/stallman.mp3"):
                tts = gTTS(
                    text="Richard Stallmanne est mon seul et unique dieu", lang="fr")
                tts.save("answers/stallman.mp3")
            notify("Richard Stallmanne est mon seul et unique dieu", self.icon)
            Popen(["mpv", "answers/stallman.mp3"])
            self.end = True

  
        if "suivant" in speech:
            f_list = open("play", "r").read().split("|")
            if int(f_list[1]) < 9:
                file = f_list[0].replace(f_list[1], str(int(f_list[1])+1))
            else:
                file = f_list[0].replace(f_list[1], str(int(f_list[1])+1))
            open("play", "w").write(file+"|"+str(int(f_list[1])+1))
            self.end = True  
            Popen(["python", "mpv.py", file])
        
        if "précédent" in speech:
            f_list = open("play", "r").read().split("|")
            if int(f_list[1]) <= 10:
                file = f_list[0].replace(f_list[1], str(int(f_list[1])-1))
            else:
                file = f_list[0].replace(f_list[1], str(int(f_list[1])-1))
            open("play", "w").write(file+"|"+str(int(f_list[1])-1))
            self.end = True
            Popen(["python", "mpv.py", file])

    #--------------- search through directory ---------------------------------------------------#

        try:

            names = re.search("lance \w+ \w+",
                                  speech)
            if not names:
                names = re.search("lancer \w+ \w+",
                                      speech)
                if not names:
                    names = str(re.search('":"\w+ \w+',
                        speech).group()).replace('":"', '').split(" ")
                    names.insert(0, "Test")
                else:
                    names = str(names.group()).split()

            else:
                names = str(names.group()).split()
            
            id = re.search("épisode ([0-9]+)", speech).group(1)
            
            print(type(names))
            print(names)
            
            try:
                season = re.search("saison ([0-9]+)", speech).group(1)
            except:
                print("No season!")
                season = None 

            if len(names[1]) <= 3:
                name = names[2][0:5].replace(
                    "é", "e").replace("É", "E")
            else:
                name = names[1][0:5].replace(
                    "é", "e").replace("É", "E")

            for root, directories, files in walk(self.directory):
                for directory in directories:
                    if name.lower() in str(directory).lower():
                        dirs = self.directory + str(directory) + '/'
                        for root, directories, files in walk(dirs):
                            if ' ' in directory or '!' in directory:
                                self.directory += '"{}"/'.format(
                                    str(directory))
                            else:
                                self.directory += str(directory) + '/'
                            if directories:
                                for directory in directories:
                                    if season:
                                        if season in str(directory):
                                            dirs += str(directory) + '/'
                                            if ' ' in directory or '!' in directory:
                                                self.directory += '"{}"/'.format(
                                                    str(directory))
                                            else:
                                                self.directory += str(
                                                            directory) + '/'
                                            break

                            
                            for root, dirs, files in walk(dirs):
                                for file in files:
                                    if id in str(file) and '.srt' not in str(file):
                                        if ' ' in str(file):
                                            f = self.directory + \
                                                '"{}"'.format(file)
                                        
                                        else: 
                                            f = self.directory + file
                                        
                                        open("play", "w").write(f+"|"+id)
                                        Popen(
                                            ["python", "mpv.py", f])
                                        self.end = True
                                            
                                        break

        except:
            pass
    
  #--------------------------------------------------------------#

    def killer(self, speech):

        for i, j in self.prog.items():
            for k in j:
                if k in speech:
                    self.play_answer('ferme', i) 
                    Popen(["killall", "{}".format(i)])
                    break

  #--------------------------------------------------------------#


def write_pid_file():

    pid = "\n" + str(getpid())
    f = open('/home/random/Python-exp/VoiceCommander/my_pid', 'a')
    f.write(pid)
    f.close()

  #--------------------------------------------------------------#


def main():

    Master = Recognizer()
    write_pid_file()
    system("mpv answers/salut.mp3")
    notify("Oui maître ? ", Master.icon)
    
    while True:
        speech = Master.record_and_read()
        print(speech)
        
        if "ferme" in speech:
            Master.killer(speech)
        else:
            Master.parser(speech)

        if Master.end:
            #[Popen(["kill", i]) for i in open("my_pid", "r").readlines()]
            quit()

        else:

            if not path.isfile("answers/sorry.mp3"):
                tts = gTTS(
                    text="Excusez-moi je n'ai pas compris, pouvez-vous répéter ?", lang="fr")
                tts.save("answer/sorry.mp3")

            system("mpv answers/sorry.mp3")


if __name__ == '__main__':

    main()
