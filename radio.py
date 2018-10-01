
import sys
from subprocess import call
import time

from Player import Player

#
# https://github.com/yeokm1/pi-radio
# https://www.nrk.no/mp3aac/
#



class Radio(object):

    def __init__(self):
        super(Radio, self).__init__()
        self.radioPlayer = Player()
        self.COMMANDS = {
            'q': self.radioPlayer.play,
            'w': self.radioPlayer.stop,
            'e': self.radioPlayer.previousStation,
            'r': self.radioPlayer.nextStation
        }

    def startRadio(self):

        while True:
            try:
                command = input("Command: ")
                self.COMMANDS[command]()
            except KeyError:
                print("Wrong key.")
            except KeyboardInterrupt:
                self.radioPlayer.stop()
                sys.exit("KeyboardInterrupt")



def main():
    # radioPlayer = Player()
    #
    #
    #
    # while True:
    #     try:
    #         command = input("Command: ")
    #         COMMANDS[command]()
    #     except KeyError:
    #         print("Wrong key.")
    #     except KeyboardInterrupt:
    #         radioPlayer.stop()
    #         sys.exit("KeyboardInterrupt")
    #
    # radioPlayer.stop()
    radio = Radio()
    radio.startRadio()



if __name__ == '__main__':
    main()
