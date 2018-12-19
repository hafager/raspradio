import utils
from Player import Player
import time

radio_stations = utils.read_radio_stations()

p = Player(radio_stations)

p.play_station(radio_stations[0]["url"])

time.sleep(10)

p.play_station(radio_stations[1]["url"])

time.sleep(10)

p.stop()