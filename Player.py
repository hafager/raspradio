# Methods for controlling the radiosoftware. Should be triggered by events in radioIO.

from subprocess import call
from subprocess import Popen
from subprocess import DEVNULL
import time
from threading import Thread


"""
    TODO:
    [X] Make it possible to change channel when not playing without starting the stream.
    [ ] Change commands to use Popen instead of call.
    
    play(self, station)
    stop(self)
    set_volume(self, new_volume)
    mute(self)
    
    Testing:
    mplayer -cache-min 2 http://lyd.nrk.no/nrk_radio_p2_mp3_h
"""

play_command = "mplayer -cache-min 2 {} </dev/null >/dev/null 2>&1 &"
play_command_new = ['mplayer', '-quiet', '-cache-min', '2']
stdout_command_new = ['</dev/null', '>/dev/null', '2>&1', '&']
stop_command = "killall mplayer"
stdout_command = " </dev/null >/dev/null 2>&1 &"
volume_command = "amixer -q sset PCM {}%"

MAX_VOLUME = 100

class Player():
    """
        docstring for Player.
    """
    def __init__(self, radioStations):
        super(Player, self).__init__()
        self.status = "stopped"
        self.radioStations = radioStations
        self.currentStation = 0

    def play_station(self, station):
        call(stop_command, shell=True)
        print(play_command_new + [station])
        # Do I need to use stdout_command here?
        p = Popen(play_command_new + [station], stdout=DEVNULL)

        # A method that can be changed to the station given as an argument. TODO
        #print(play_command % station["url"])
        #print(play_command.format(self.radioStations[0]["url"]))

        #call([play_command, station.url])
        #call(play_command.format(self.radioStations[0]["url"]), shell=True)

    def play_deprecated(self):
        print("Playing current station id {} called {} from URL: {}".format(
                    self.currentStation,
                    self.radioStations[self.currentStation]["name"],
                    self.radioStations[self.currentStation]["url"]))
        call(play_command.format(self.radioStations[self.currentStation]["url"]), shell=True)
        self.status = "playing"

    def stop(self):
        call(stop_command, shell=True)
        print("stop")
        self.status = "stopped"

    def update(self):
        """
            Stops and starts the player.
            Should be called when the channel is switched
        """
        call(stop_command, shell=True)
        self.play_station(self.currentStation)

    def nextStation(self):
        """
            Changes to next station.
            Nothing happens if you are at the last station
        """
        print("Next Station")
        if self.currentStation < len(self.radioStations) - 1:
            self.currentStation += 1
            if self.status == "playing":
                self.update()

    def previousStation(self):
        """
            Changes to previous station
            Nothing happens if you are at the first station
        """
        print("Previous Station")
        if self.currentStation != 0:
            self.currentStation -= 1
            if self.status == "playing":
                self.update()

    def volumeUp(self):
        print("Volume up")
        call(volume_command.format("1+"), shell=True)

    def volumeDown(self):
        print("Volume down")
        call(volume_command.format("1-"), shell=True)

    def set_volume(self, new_volume):
        if new_volume < 0 or new_volume > 100:
            print("Error: Inappropriate volume.")
        else:
            print("Setting volume to {}".format(new_volume))
            call(volume_command.format(new_volume), shell=True)


def get_volume():
    # Expects the volume to show as percent in the 5th line between brackets.
    p = Popen(get_volume_command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output = str(p.stdout.readlines()[4])
    vol = output[output.index('[') + 1:output.index(']') - 1]
    return vol
