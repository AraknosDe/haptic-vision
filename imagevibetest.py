# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the DRV2605 haptic feedback motor driver.
# Will play all 123 effects in order for about a half second each.
import time

import board
import busio

from depthglove import DepthGlove
import numpy as np



if __name__ == '__main__':
    depthglove = DepthGlove()
    
    image = np.array( [[ 300,  3000],
                       [ 2500,  2500],
                       [ 2500,  2500],
                       [ 2500,  2500],
                       [ 2500, 2500]])
    
    try:                   
        while True:
            depthglove.update_glove(image)
            #time.sleep(1.0)
            image = np.roll(image, 1, axis=0)
            #print(image)
    except:
        depthglove.stop_fingers()
        
    try:                   
        start = time.time()
        for i in range (1000):
            depthglove.update_glove(image)
            image = np.roll(image, 1, axis=0)
        end = time.time()
        print(1000/(end - start))
    except:
        depthglove.stop_fingers()

    depthglove.stop_fingers()
    
        
        
