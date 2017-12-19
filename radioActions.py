# Methods for controlling the radiosoftware. Should be triggered by events in radioIO.

from subprocess import call
import time


play_command = "mplayer -cache-min 2 %s </dev/null >/dev/null 2>&1 &"
stop_command = "killall mplayer"
stdout_command = " </dev/null >/dev/null 2>&1 &"
volume_up_command = ""
volume_down_command = ""


def play_station(station):
    print(play_command % station["url"])

    #call([play_command, station.url])
    call(play_command % station["url"], shell=True)

def stop_radio():
    call(stop_command, shell=True)
    print("stop")

def play_next():
    print("next")

def volume_up():
    print("Volume up")

def volume_down():
    print("Volume down")
