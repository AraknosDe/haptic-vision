import sys
import time

import board
import busio

from micropython import const

from TCA9548A import TCA9548A

i2c = busio.I2C(board.SCL, board.SDA)
multi = TCA9548A(i2c)

if __name__ == '__main__':
    bus = int(sys.argv[1])
    time.sleep(1)
    multi.bus_select(bus)
