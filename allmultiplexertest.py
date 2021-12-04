# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the DRV2605 haptic feedback motor driver.
# Will play all 123 effects in order for about a half second each.
import time

import board
import busio

from TCA9548A import TCA9548A
from multiplexed_drv2605 import Multi_DRV2605
from DRV2605 import Effect





if __name__ == '__main__':
    # See table 11.2 in the datasheet for a list of all the effect names and IDs.
    #   http://www.ti.com/lit/ds/symlink/drv2605.pdf

    # Initialize I2C bus and DRV2605 module.
    i2c = busio.I2C(board.SCL, board.SDA)

    tca = TCA9548A(i2c)
    drvlist = []
    for i in range(5):
        try:
            drvlist.append(Multi_DRV2605(i2c, tca, multibus=i))
        except ValueError:
            print("no controller on bus " + str(i))
    
    for drv in drvlist:
        drv.RTP_write(0)
        drv.RTP_on()
    
    for drv in drvlist:
        for i in range(5):
            print("motor " + str(drv._multibus) + " " + str(25*i) + "%")
            drv.RTP_write(0.25*i)
            time.sleep(0.5)
        drv.RTP_write(0)
    
        
        
