# This class will contain methods for reading input from the physical radio.

import readchar

class RadioIO(object):
    """
        docstring for RadioIO.
    """
    def __init__(self):
        super(RadioIO, self).__init__()
        self.test = "test"

    def readMode(self):
        return "radio"

    def readVolume(self):
        return "5"

    def readStation(self):
        return "p3"

    def readTone(self):
        return "high"

    def readKey(self):
        readchar.readchar()

def main():
    print("test")
    key = readchar.readchar()
    print(key)

if __name__ == '__main__':
    main()