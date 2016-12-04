from os import system, path, walk, popen, getpid
from notify import notify
from googlespeech import SpeechRecog
from subprocess import call, Popen
from recorder import Record
from gtts import gTTS
from multiprocessing import Pool
import re
import time
import numpy as np


class Recognizer(object):

    #--------------------------------------------------------------#

    def __init__(self):

        self.end = False
        self.prog = {
            "chromium": ["chrome", "chromium"],
            "light": ["firefox", "firefoxe", "light"],
            "gvim": ["vim", "vime", "gvim", "j'ai vim", "j'ai vime", "programmer"],
            "mpv": ["lecteur", "mpv"]
        }
        self.directory = "/run/media/random/DATA/Animes/"
        self.icon = "/home/random/.config/awesome/themes/powerarrow-darker/icons/micon_on.png"
   #--------------------------------------------------------------#
    
    def record_and_read(self):

        r = Record()
        r.launch()
        speech = SpeechRecog.get_answer_from_google() 
       
        return speech
   #--------------------------------------------------------------#

    def parser(self, speech):

        for i, j in self.prog.items():
            for k in j:
                if k in speech:

                    if not path.isfile("answers/lance_{}.mp3".format(i)):
                        tts = gTTS(
                            text="Très bien, je lance {}".format(i), lang="fr")
                        tts.save("answers/lance_{}.mp3".format(i))
                    notify("Très bien, je lance {}".format(i), self.icon)
                    Popen(["mpv", "answers/lance_{}.mp3".format(i)])
                    Popen(["{}".format(i), ""])
                    self.end = True
                    break

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

        if "éteins" and "ordinateur" in speech or "éteins" and "pc" in speech:
            system("shutdown -h now")


    #--------------- search through directory ---------------------------------------------------#

        try:

            names = str(re.search("lance \w+ \w+",
                                  speech).group()).split(" ")
            if not names:
                names = str(re.search("lancer \w+ \w+",
                                      speech).group()).split(" ")

            id = re.search("épisode ([0-9]+)", speech).group(1)
            try:
                season = re.search("saison ([0-9]+)", speech).group(1)
            except:
                print("No season!")
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
                                    try:
                                        if season in str(directory):
                                            dirs += str(directory) + '/'
                                            if ' ' in directory or '!' in directory:
                                                self.directory += '"{}"/'.format(
                                                    str(directory))
                                            else:
                                                self.directory += str(
                                                    directory) + '/'
                                    except:
                                        print("no season...")

                            for root, dirs, files in walk(dirs):
                                for file in files:
                                    if id in str(file) and '.srt' not in str(file):
                                        if ' ' in str(file):
                                            f = self.directory + \
                                                '"{}"'.format(file)
                                            Popen(
                                                ["python", "mpv.py", f])
                                            self.end = True
                                            break

                                        else:
                                            Popen(
                                                ["mpv", "--fs", self.directory + file])
                                            self.end = True
                                            break
        except:
            pass

  #--------------------------------------------------------------#

    def killer(self, speech):

        for i, j in self.prog.items():
            for k in j:
                if k in speech:

                    if not path.isfile("answers/ferme_{}.mp3".format(i)):
                        tts = gTTS(
                            text="Très bien, je ferme {}".format(i), lang="fr")
                        tts.save("answers/ferme_{}.mp3".format(i))
                    
                    notify("Très bien, je ferme {}".format(i), self.icon)
                    Popen(["mpv", "answers/ferme_{}.mp3".format(i)])
                    Popen(["killall", "{}".format(i)])
                    self.end = True
                    break


def write_pid_file():

    pid = "\n" + str(getpid())
    f = open('/home/random/Python-exp/VoiceCommander/my_pid', 'a')
    f.write(pid)
    f.close()

  #--------------------------------------------------------------#


def main():

    write_pid_file()
    
    rd = np.random.choice([0, 1])
    if rd == 1:
        Popen(["mpv", "answers/Salut.mp3"])
    else:
        Popen(["mpv", "answers/Salut2.mp3"])

    while True:
        Master = Recognizer()
        speech = Master.record_and_read()

        print(speech)

        if "ferme" in speech:
            Master.killer(speech)
        else:
            Master.parser(speech)

        if Master.end is True:
            quit()

        else:

            if not path.isfile("answers/sorry.mp3"):
                tts = gTTS(
                    text="Excusez-moi je n'ai pas compris, pouvez-vous répéter ?", lang="fr")
                tts.save("answer/sorry.mp3")

            system("mpv answers/sorry.mp3")


if __name__ == '__main__':

    main()
