
from subprocess import Popen
from subprocess import PIPE
from subprocess import DEVNULL

get_volume_command = ['amixer', 'sget', 'PCM']

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
    print(station_values)
    return station_values

def get_volume():
    # Expects the volume to show as percent in the 5th line between brackets.
    p = Popen(get_volume_command, stdin=DEVNULL, stdout=PIPE, stderr=DEVNULL)
    output = str(p.stdout.readlines()[4])
    vol = output[output.index('[') + 1:output.index(']') - 1]
    return vol