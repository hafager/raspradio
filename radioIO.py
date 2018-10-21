# This class will contain methods for reading input from the physical radio.
"""
    Info GPIO and I2C: https://www.raspberrypi.org/documentation/usage/gpio/
    Info potentiometer; https://www.sparkfun.com/products/9939
    Enable I2C: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
    Data sheet AD/DA Converter PCF8591: https://www.nxp.com/docs/en/data-sheet/PCF8591.pdf
    Example PCF8591: https://www.waveshare.com/wiki/Raspberry_Pi_Tutorial_Series:_PCF8591_AD/DA
"""




import readchar
import smbus
import time

ADDRESS = 0x48
A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43

class RadioIO(Thread):
    """
        docstring for RadioIO.
    """
    def __init__(self, queue):
        super(RadioIO, self).__init__()
        self.queue = queue
        self.bus = smbus.SMBus(1)

    def readMode(self):
        return "radio"

    def readVolume(self):
        return "5"

    def readStation(self):
        bus.write_byte(address,A0)
        value = bus.read_byte(ADDRESS)
        print("AOUT:%1.3f  " %(value*3.3/255))
        print("AOUT:{} \%".format((value/255)*100))
        return value

    def readTone(self):
        return "high"

    def readKey(self):
        readchar.readchar()

    def run(self):
        while True:
            station_value = self.readStation()
            print("AOUT:%1.3f  " %(station_value*3.3/255))
            time.sleep(0.1)

def main():
    print("test")
    key = readchar.readchar()
    print(key)

if __name__ == '__main__':
    main()
