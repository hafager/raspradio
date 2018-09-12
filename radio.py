

from subprocess import call
import time

from radioPlayer import Player

#
# https://github.com/yeokm1/pi-radio
#

radioPlayer = Player()
radioPlayer.play()

#radioActions.play_station(radio_stations[0])

time.sleep(5)

radioPlayer.nextStation()

time.sleep(5)
radioPlayer.nextStation()

time.sleep(5)
radioPlayer.previousStation()
time.sleep(5)

radioPlayer.stop()
