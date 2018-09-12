

from subprocess import call
import time

from radioPlayer import Player

#
# https://github.com/yeokm1/pi-radio
#



class Radio(object):

    def __init__(self):
        super(Player, self).__init__()

def main():
    radioPlayer = Player()

    COMMANDS = {
        'q': radioPlayer.play,
        'w': radioPlayer.stop,
        'e': radioPlayer.previousStation,
        'r': radioPlayer.nextStation,
    }

    while True:
        command = input("Command: ")
        COMMANDS[command]()

    # radioPlayer.play()
    #
    # time.sleep(5)
    # radioPlayer.nextStation()
    # time.sleep(5)
    # radioPlayer.nextStation()
    # time.sleep(5)
    # radioPlayer.nextStation()
    # time.sleep(5)
    # radioPlayer.previousStation()
    # time.sleep(5)
    #
    radioPlayer.stop()



if __name__ == '__main__':
    main()
