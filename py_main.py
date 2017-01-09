from os import system, path, walk, popen, getpid
from notify import notify
from subprocess import call, Popen
from recorder import Record
from gtts import gTTS
from googlespeech import SpeechRecog
import re
from time import sleep


class Recognizer(object):

    #--------------------------------------------------------------#

    def __init__(self):
        
        if "blue" in open("/home/random/.config/awesome/rc.lua", "r").read():
            self.icon = "/home/random/.config/awesome/themes/powerarrow-darker/icons/micon_blue.png"
        else:
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

    def normalize(self, speech):

        speech = speech.lower().replace(
            "é", "e").replace("è", "e")
        
        return speech 
    
    def print_what_you_said(self, speech):

        # match = re.match(r"^.*\:\"(.*)\"\,.*$", speech).group(1)

        match = speech.split(':"')
        match = match[1].split('",')
        match = match[0]
        notify("You: {}".format(match), self.icon)

   #--------------------------------------------------------------#
    def play_answer(self, action, software=None, text=None):
        if software:
            if not path.isfile("answers/{}_{}.mp3".format(action, software)):
                tts = gTTS(
                    text="Très bien, je {} {}...".format(action, software), lang="fr")
                tts.save("answers/{}_{}.mp3".format(action, software))
        
            notify("Alexa: Très bien, je {} {} ... ".format(
                                        action, software), self.icon)
            Popen(["mpv", "answers/{}_{}.mp3".format(action, software)])
        else:
            if not path.isfile("answers/{}.mp3".format(action)):
                tts = gTTS(
                    text=text, lang="fr")
                tts.save("answers/{}.mp3".format(action))
            notify("Alexa: {}".format(text), self.icon)
            Popen(["mpv", "answers/{}.mp3".format(action)])
            sleep(1)
   #--------------------------------------------------------------#
    def parser(self, speech):
        if "ferme" not in speech and "coupe" not in speech:
            for i, j in self.prog.items():
                for k in j:
                    if k in speech:
                        self.play_answer('lance', software=i)
                        Popen(["{}".format(i), ""])
                        self.end = True
                        break
    #--------------------------------------------------------------#

    def launch_other_stuff(self, speech):

        if "musique" in speech:
            Popen(
                ["mpv", "/run/media/random/DATA2/SoulseekDownloads/complete/Musique_djam"])
            self.end = True

        if "merci" in speech:
            self.play_answer("merci.mp3", 
                    text="Mais de rien mon seigneur, je voue mon existence à votre service.") 
            self.end = True

        if "religion" in speech:
            self.play_answer("stallman.mp3", 
                    text="Richard Stallmanne est mon seul et unique dieu !")
            self.end = True

        if "suivant" in speech:
            f_list = open("play", "r").read().split("|")
            if int(f_list[2]) < 9:
                id = "0" + str(int(f_list[2]) + 1)
              
            else:
                id = str(int(f_list[2]) + 1)
            
            dir = f_list[0]
            self.directory = f_list[1]
            
            for root, dirs, files in walk(dir):
                for file in files:
                    if id in str(file) and '.srt' not in str(file):
                        if ' ' in str(file):
                            f = self.directory + \
                                '"{}"'.format(file)
                        else:
                            f = self.directory + file

                        open("play", "w").write(
                            dir + "|"+ self.directory + "|" + id)
                        Popen(
                            ["python", "mpv.py", f])
                        self.end = True
                        break
                if self.end:
                    break

            
        if "precedent" in speech:
            f_list = open("play", "r").read().split("|")
            if int(f_list[2]) <= 10:
                id = "0" + str(int(f_list[2]) - 1)

            else:
                id = str(int(f_list[2]) - 1)
            
            dir = f_list[0]
            self.directory = f_list[1]
            
            for root, dirs, files in walk(dir):
                for file in files:
                    if id in str(file) and '.srt' not in str(file):
                        if ' ' in str(file):
                            f = self.directory + \
                                '"{}"'.format(file)
                        else:
                            f = self.directory + file

                        open("play", "w").write(
                            dir + "|"+ self.directory + "|" + id)
                        Popen(
                            ["python", "mpv.py", f])
                        self.end = True
                        break
                if self.end:
                    break
 

        if "bonjour" in speech:
            self.play_answer("bonjour.mp3", 
                    text="Bonjour, comment ça va ?") 
            self.end = True

    #--------------- search through directory ---------------------------------------------------#

    def play_video(self, speech):

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

            id = re.search("episode ([0-9]+)", speech).group(1)
            
            if int(id) < 10:
                id = "0"+str(int(id))
            
            print(type(names))
            print(names)

            try:
                season = re.search("saison ([0-9]+)", speech).group(1)
            except:
                print("No season!")
                season = None

            if len(names[1]) <= 3:
                name = names[2][0:5]

            else:
                name = names[1][0:5]

            for root, directories, files in walk(self.directory):
                for directory in directories:
                    if name in str(directory).lower():
                        dir = self.directory + str(directory) + '/'
                        for root, directories, files in walk(dir):
                            if ' ' in directory or '!' in directory:
                                self.directory += '"{}"/'.format(
                                    str(directory))
                            else:
                                self.directory += str(directory) + '/'
                            if directories:
                                for directory in directories:
                                    if season:
                                        if season in str(directory):
                                            dir += str(directory) + '/'
                                            if ' ' in directory or '!' in directory:
                                                self.directory += '"{}"/'.format(
                                                    str(directory))
                                            else:
                                                self.directory += str(
                                                    directory) + '/'
                                            break
                            
                            for root, dirs, files in walk(dir):
                                for file in files:
                                    if id in str(file) and '.srt' not in str(file):
                                        if ' ' in str(file):
                                            f = self.directory + \
                                                '"{}"'.format(file)
                                        else:
                                            f = self.directory + file
                                        
                                        open("play", "w").write(
                                            dir + "|" + self.directory + "|"+ id)
                                        Popen(
                                            ["python", "mpv.py", f])
                                        self.end = True
                                        break
                                if self.end:
                                    break
                            if self.end:
                                break

        except Exception as e:
            print(e)
  
  #--------------------------------------------------------------#

    def killer(self, speech):

        if "ferme" in speech or "coupe" in speech:
            for i, j in self.prog.items():
                for k in j:
                    if k in speech:
                        self.play_answer('ferme', software=i)
                        Popen(["killall", "{}".format(i)])
                        self.end = True
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
   
    Master.play_answer("salut.mp3", text="Oui maître ?")

    while True:

        speech = Master.normalize(Master.record_and_read())
        print(speech)
        Master.print_what_you_said(speech)
        Master.killer(speech)
        Master.parser(speech)
        Master.launch_other_stuff(speech)
        Master.play_video(speech)

        if Master.end:
            [Popen(["kill", i]) for i in open("my_pid", "r").readlines()]
            quit()

        else:
            Master.play_answer("sorry.mp3", 
                    text="Excusez-moi je n'ai pas compris, pouvez-vous répéter ?")
            

if __name__ == '__main__':

    main()
