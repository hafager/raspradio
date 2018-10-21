
import sys
from subprocess import call
import time
import readchar
from queue import Queue

from Player import Player

#
# https://github.com/yeokm1/pi-radio
# https://www.nrk.no/mp3aac/
#



class Radio(object):

    def __init__(self):
        super(Radio, self).__init__()
        self.queue = Queue()
        self.radioStations = readRadioStations()
        self.radioPlayer = Player(self.queue)
        self.radioPlayer.start()
        # self.COMMANDS = {
        #     'q': self.radioPlayer.play,
        #     'w': self.radioPlayer.stop,
        #     'e': self.radioPlayer.previousStation,
        #     'r': self.radioPlayer.nextStation
        # }
        self.COMMANDS = {
            'q': "play",
            'w': "stop",
            'e': "next",
            'r': "previous"
        }

    def start(self):

        while True:
            try:
                command = readchar.readchar()
                # command = input("Command: ")
                #self.COMMANDS[command]()
                self.queue.put(self.COMMANDS[command])
            except KeyError:
                self.queue.put(None)
                self.radioPlayer.stop()
                sys.exit("Exiting")
            except KeyboardInterrupt:
                self.queue.put(None)
                self.radioPlayer.stop()
                sys.exit("KeyboardInterrupt")


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
