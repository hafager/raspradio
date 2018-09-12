# Methods for controlling the radiosoftware. Should be triggered by events in radioIO.

from subprocess import call
import time


play_command = "mplayer -cache-min 2 {} </dev/null >/dev/null 2>&1 &"
stop_command = "killall mplayer"
stdout_command = " </dev/null >/dev/null 2>&1 &"
volume_up_command = ""
volume_down_command = ""

class Player(object):
    """
        docstring for Player.
    """
    def __init__(self):
        super(Player, self).__init__()
        self.status = "stopped"
        self.radioStations = readRadioStations()
        self.currentStation = 0

    def play(self):
        print("Playing current station {} URL: {}".format(self.currentStation, self.radioStations[self.currentStation]["url"]))
        call(play_command.format(self.radioStations[self.currentStation]["url"]), shell=True)
        self.status = "playing"

    def stop(self):
        call(stop_command, shell=True)
        print("stop")
        self.status = "stopped"


    def playStation(self, station):
        #print(play_command % station["url"])
        print(play_command.format(self.radiostations[0]["url"]))

        #call([play_command, station.url])
        call(play_command.format(self.radiostations[0]["url"]), shell=True)


    def nextStation(self):
        """
            Changes to next station.
            Nothing happens if you are at the last station
        """
        print("Next Station")
        self.currentStation += 1
        self.stop()
        self.play()

    def previousStation(self):
        """
            Changes to previous station
            Nothing happens if you are at the first station
        """
        print("Previous Station")
        self.currentStation -= 1
        self.stop()
        self.play()

    def volumeUp(self):
        print("Volume up")

    def volumeDown(self):
        print("Volume down")


def readRadioStations():
    stationFile = open("radiostations.txt", "r")
    stations = stationFile.read().splitlines()
    stationFile.close()
    radioStations = []
    for station in stations:
        name, url = station.split("|")
        radioStations.append({"name": name, "url": url})

    print(radioStations)
    return radioStations
