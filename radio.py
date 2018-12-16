
import sys
from subprocess import call
import time
import readchar
from queue import Queue

from Player import Player
from radioIO import RadioIO

#
# https://github.com/yeokm1/pi-radio
# https://www.nrk.no/mp3aac/
#



class Radio(object):

    def __init__(self):
        super(Radio, self).__init__()
        self.playerQueue = Queue()
        self.ioQueue = Queue()
        self.radioStations = readRadioStations()
        self.radioPlayer = Player(self.playerQueue, self.radioStations)
        self.radioPlayer.start()
        self.radioIO = RadioIO(self.ioQueue, debug=False)
        self.radioIO.start()

        self.radioPlayer.set_volume(0)
        self.current_volume = 0

        self.current_station = self.radioStations[0]

        self.PLAYER_COMMANDS = {
            'q': "play",
            'w': "stop",
            'e': "previous",
            'r': "next"
        }
        self.IO_COMMANDS = {
            "station": self.changeStation,
            "volume": self.changeVolume,
            "mode": self.changeMode,
            "key": self.changeUsingKeys
        }

    def changeStation(self, value):
        print("Station: {0}".format(value))

    def changeVolume(self, new_volume):
        print("Volume")

        print("Set volume to: {}".format(new_volume))
        #self.playerQueue.put(new_volume)

        if new_volume != self.current_volume:
            self.radioPlayer.set_volume(new_volume)
            self.current_volume = new_volume


    def changeMode(self, value):
        if value == "play":
            self.playerQueue.put("play")
        elif value == "stop":
            self.playerQueue.put("stop")

    def changeUsingKeys(self, value):
        try:
            print("Put {} into the Player Queue".format(self.PLAYER_COMMANDS[value]))
            self.playerQueue.put(self.PLAYER_COMMANDS[value])
        except KeyError:
            self.playerQueue.put(None)
            self.radioPlayer.stop()
            sys.exit("Exiting")
        except KeyboardInterrupt:
            self.playerQueue.put(None)
            self.radioPlayer.stop()
            sys.exit("KeyboardInterrupt")

    def start(self):

        while True:
            action = self.ioQueue.get()
            if action is None:
                self.playerQueue.put(None)
                self.radioPlayer.stop()
                sys.exit("Exiting")
                break

            # TODO: Check for invalid values
            self.IO_COMMANDS[action[0]](action[1])
            self.ioQueue.task_done()



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


def main():

    radio = Radio()
    radio.start()



if __name__ == '__main__':
    main()
