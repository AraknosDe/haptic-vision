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


# Initialize I2C bus and DRV2605 module.
i2c = busio.I2C(board.SCL, board.SDA)
tca = TCA9548A(i2c)
drv0 = Multi_DRV2605(i2c, tca, multibus=0)
drv2 = Multi_DRV2605(i2c, tca, multibus=2)

if __name__ == '__main__':
    # See table 11.2 in the datasheet for a list of all the effect names and IDs.
    #   http://www.ti.com/lit/ds/symlink/drv2605.pdf
    
    drv0.RTP_write(0)
    drv2.RTP_write(0)
    
    drv0.RTP_on()
    drv2.RTP_on()
    
    drv0.RTP_write(0)
    drv2.RTP_write(1)
    time.sleep(1.0)
    
    drv0.RTP_write(0.25)
    drv2.RTP_write(0.75)
    time.sleep(1.0)
    
    drv0.RTP_write(0.5)
    drv2.RTP_write(0.5)
    time.sleep(1.0)
    
    drv0.RTP_write(0.75)
    drv2.RTP_write(0.25)
    time.sleep(1.0)
    
    drv0.RTP_write(1)
    drv2.RTP_write(0)
    time.sleep(1.0)
    
    drv0.RTP_write(0)
    drv2.RTP_write(0)
    
        
        
