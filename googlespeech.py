import http.client
import sys
import re
import os


class SpeechRecog(object):
    
    @staticmethod
    def get_answer_from_google():
        data = open("sentence.flac", "rb").read()
        google_speech = http.client.HTTPConnection('www.google.com')

        google_speech.request('POST',
                              '/speech-api/v2/recognize?output=json&lang=fr&key'
                              '=AIzaSyC1xLBh8Wsh_DYUU3K3NI9Q2PKX2E4MqLw',
                              data, {'Content-type': 'audio/x-flac; rate=16000'})

        stt = google_speech.getresponse().read()
        google_speech.close()
        
        return str(stt, "utf8")

if __name__ == '__main__':
    SpeechRecog.get_answer_from_google()
    quit()
