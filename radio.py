

from subprocess import call
import time

#
# https://github.com/yeokm1/pi-radio
#

play_command = "mplayer -cache-min 2 %s </dev/null >/dev/null 2>&1 &"
stop_command = "killall mplayer"
stdout_command = " </dev/null >/dev/null 2>&1 &"
volume_up_command = ""
volume_down_command = ""



def read_radiostations():
    station_file = open("/Users/hafager/Projects/radioproject/raspradio/radiostations.txt", "r")
    stations = station_file.read().splitlines()
    station_file.close()
    radio_stations = []
    for station in stations:
        name, url = station.split("|")
        radio_stations.append({"name": name, "url": url})

    print radio_stations[0]["url"]
    return radio_stations

def play_station(station):
    print(play_command % station["url"])

    #call([play_command, station.url])
    call(play_command % station["url"], shell=True)

radio_stations = read_radiostations()

def stop_radio():
    call(stop_command, shell=True)
    print("stop")

def volume_up():
    print("Volume up")

def volume_down():
    print("Volume down")

play_station(radio_stations[0])

time.sleep(3)

stop_radio()
