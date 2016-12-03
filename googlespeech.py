import httplib
import sys
import re
import os


class SpeechRecog(object):

    @staticmethod
    def get_answer_from_google():

        f = open("/home/random/Python-exp/VoiceCommander/sentence.flac", "r")
        data = f.read()
        f.close()
        google_speech = httplib.HTTPConnection('www.google.com')

        google_speech.request('POST',
                              '/speech-api/v2/recognize?output=json&lang=fr&key=AIzaSyC1xLBh8Wsh_DYUU3K3NI9Q2PKX2E4MqLw',
                              data, {'Content-type': 'audio/x-flac; rate=16000'})

        answer = google_speech.getresponse().read()
        google_speech.close()
        f = open("text", "w").write(answer)


if __name__ == '__main__':

    SpeechRecog.get_answer_from_google()
