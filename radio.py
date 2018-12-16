
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
        self.radioStations = read_radio_stations()
        self.station_values = create_station_values(self.radioStations)
        self.radioPlayer = Player(self.playerQueue, self.radioStations)
        self.radioPlayer.start()
        self.radioIO = RadioIO(self.ioQueue, debug=False)
        self.radioIO.start()

        self.radioPlayer.set_volume(0)
        self.current_volume = 0

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

        if new_volume != self.current_volume:
            self.radioPlayer.set_volume(new_volume)
            self.current_volume = new_volume

    def change_mode(self, value):
        if value == "play":
            self.playerQueue.put("play")
        elif value == "stop":
            self.playerQueue.put("stop")

    def change_using_keys(self, value):
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


def read_radio_stations():
    station_file = open("radiostations.txt", "r")
    stations = station_file.read().splitlines()
    station_file.close()
    radio_stations = []
    for station in stations:
        name, url = station.split("|")
        radio_stations.append({"name": name, "url": url})
    print(radio_stations)
    """
    Example:
        [
            {"name": "P3", "url": "https://p3.no"}
        [
    """
    return radio_stations


def create_station_values(radio_stations):
    number_of_stations = len(radio_stations)
    station_values = []
    for i in range(1, number_of_stations + 1):
        station_values.append(i * (100//(number_of_stations + 1)))
    """
    Example:
        [ 20, 40, 60, 80 ]
    """
    return station_values


def main():

    radio = Radio()
    radio.start()


if __name__ == '__main__':
    main()
