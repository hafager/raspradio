
import sys
from subprocess import call
import time
import readchar
from queue import Queue

from Player import Player
from radioIO import RadioIO
import utils

#
# https://github.com/yeokm1/pi-radio
# https://www.nrk.no/mp3aac/
#


class Radio(object):

    def __init__(self):
        super(Radio, self).__init__()
        self.ioQueue = Queue()
        self.radioStations = utils.read_radio_stations()
        self.station_values = utils.create_station_values(self.radioStations)
        self.radioPlayer = Player(self.radioStations)
        self.radioIO = RadioIO(self.ioQueue, debug=False)
        self.radioIO.start()

        self.current_volume = self.radioIO.currentVolume
        self.radioPlayer.set_volume(self.current_volume)

        self.current_station = 0

        self.PLAYER_COMMANDS = {
            'q': "play",
            'w': "stop",
            'e': "previous",
            'r': "next"
        }
        self.IO_COMMANDS = {
            "station": self.change_station,
            "volume": self.change_volume,
            "mode": self.change_mode,
            "key": self.change_using_keys
        }

    def change_station(self, value):
        print("Station: {0}".format(value))
        #  if value not in range of current station, change to new channel
        if self.current_station == 0:
            if value > self.station_values[self.current_station]:
                self.current_station += 1
                self.radioPlayer.play_station(self.radioStations[self.current_station]["url"])
        elif self.current_station == len(self.station_values) - 1:
            if value <= self.station_values[self.current_station - 1]:
                self.current_station -= 1
                self.radioPlayer.play_station(self.radioStations[self.current_station]["url"])
        elif value > self.station_values[self.current_station]:
            self.current_station += 1
            self.radioPlayer.play_station(self.radioStations[self.current_station]["url"])
        elif value <= self.station_values[self.current_station - 1]:
            self.current_station -= 1
            self.radioPlayer.play_station(self.radioStations[self.current_station]["url"])


    def change_volume(self, new_volume):
        print("Set volume to: {}".format(new_volume))
        #  self.playerQueue.put(new_volume)

        if new_volume != self.current_volume and new_volume >= 0 and new_volume <= 100:
            self.radioPlayer.set_volume(new_volume)
            self.current_volume = new_volume

    def change_mode(self, value):
        if value == "play":
            #self.playerQueue.put("play")
            print("play")
        elif value == "stop":
            #self.playerQueue.put("stop")
            print("stop")

    def change_using_keys(self, value):
        try:
            print("Put {} into the Player Queue".format(self.PLAYER_COMMANDS[value]))
            # self.playerQueue.put(self.PLAYER_COMMANDS[value])
            print(self.PLAYER_COMMANDS[value])
        except KeyError:
            print("None")
            #self.playerQueue.put(None)
            self.radioPlayer.stop()
            sys.exit("Exiting")
        except KeyboardInterrupt:
            print("Interrupt")
            #self.playerQueue.put(None)
            self.radioPlayer.stop()
            sys.exit("KeyboardInterrupt")

    def start(self):

        while True:
            action = self.ioQueue.get()
            if action is None:
                #  self.playerQueue.put(None)
                self.radioPlayer.stop()
                sys.exit("Exiting")
                break

            # TODO: Check for invalid values
            self.IO_COMMANDS[action[0]](action[1])
            self.ioQueue.task_done()


def main():

    radio = Radio()
    radio.start()


if __name__ == '__main__':
    main()
