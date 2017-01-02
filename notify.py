# Very simple function using notify-send with Popen class
from subprocess import Popen


def notify(string, icon):
    Popen(["notify-send","-i", icon, string])
