# This class will contain methods for reading input from the physical radio.
"""
    Info GPIO and I2C: https://www.raspberrypi.org/documentation/usage/gpio/
    Info potentiometer; https://www.sparkfun.com/products/9939
    Enable I2C: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
    Data sheet AD/DA Converter PCF8591: https://www.nxp.com/docs/en/data-sheet/PCF8591.pdf
    Example PCF8591: https://www.waveshare.com/wiki/Raspberry_Pi_Tutorial_Series:_PCF8591_AD/DA
"""



from threading import Thread
import sys
import readchar
if sys.platform != "darwin":
    import smbus
import time

ADDRESS = 0x48
A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43

KEYS = set(['q', 'w', 'e', 'r'])

"""
    Messages for radioIO to radio:
    ["station", 53.2]
    ["volume", 10.0]
    ["mode", "play"]
    ["key", "q"]
"""

class RadioIO(Thread):
    """
        docstring for RadioIO.
    """
    def __init__(self, queue, debug=False):
        super(RadioIO, self).__init__()
        self.debug = debug
        self.queue = queue
        if not self.debug:
            self.bus = smbus.SMBus(1)
            self.currentVolume = self.readVolume()
            self.currentStation = self.readStation()
        self.currentVolume = 0
        self.currentStation = 0


    def readMode(self):
        return "radio"

    def readVolume(self):
        return "5"

    def readStation(self):
        bus.write_byte(address,A0)
        value = bus.read_byte(ADDRESS)
        print("AOUT:%1.3f  " %(value*3.3/255)) # Current voltage
        print("AOUT:{0:5.1}%".format((value/255)*100)) # Percent of max
        return round((value/255)*100, 1) # Return a number between 0 - 100 with 1 decimal.

    def readTone(self):
        return "high"

    def readKey(self):
        try:
            key = readchar.readchar()
            if key in KEYS:
                print("Put {} into the IO Queue".format(key))
                self.queue.put(["key", key])
            else:
                raise ValueError
        except ValueError or KeyboardInterrupt:
            self.queue.put(None)
            sys.exit("Exiting")
        # return key

    def run(self):
        if not self.debug:
            while True:
                stationValue = self.readStation()
                diff = self.currentStation - stationValue
                if diff > (diff/abs(diff)) * 0.5: # Check if it at least changes by a certain amount. To avoid unstable values.
                    self.currentStation = stationValue
                    self.queue.put(["station", self.currentStation])

                time.sleep(0.1)

        if self.debug:
            while True:
                self.readKey()


def main():
    print("Cannot run this class on its own")

if __name__ == '__main__':
    main()
