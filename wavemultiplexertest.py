# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the DRV2605 haptic feedback motor driver.
# Will play all 123 effects in order for about a half second each.
import time

import board
import busio

from glove import Glove





if __name__ == '__main__':
    # See table 11.2 in the datasheet for a list of all the effect names and IDs.
    #   http://www.ti.com/lit/ds/symlink/drv2605.pdf

    # Initialize I2C bus and DRV2605 module.
    glove = Glove()
    
    rate = 5
    
    delay = 1/rate
    finger = 0
    direction = 1
    
    while True:
        try:
            fingers = [1 if i == finger else 0.0 for i in range(5)]
            glove.set_fingers(fingers)
            if finger == 4:
                direction = -1
            if finger == 0:
                direction = 1
            finger = finger + direction
            time.sleep(delay)
        except:
            glove.stop_fingers()
            break
    
    
        
        
