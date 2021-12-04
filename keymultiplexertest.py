# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the DRV2605 haptic feedback motor driver.
# Will play all 123 effects in order for about a half second each.
import time

import board
import busio

from glove import Glove

from pynput.keyboard import Key, KeyCode, Listener

glove = Glove()
fingers = [0]*5

def update_fingers():
    glove.set_fingers(fingers)

def on_press(key):
    #print(str(key) + " pressed")
    if key == KeyCode.from_char('a'):
        print('in a if')
        fingers[0] = 1.0
    if key == KeyCode.from_char('s'):
        fingers[1] = 1.0
    if key == KeyCode.from_char('d'):
        fingers[2] = 1.0
    if key == KeyCode.from_char('f'):
        fingers[3] = 1.0
    if key == KeyCode.from_char('g'):
        fingers[4] = 1.0
    update_fingers()

def on_release(key):
    #print(str(key) + " released")
    if key == Key.esc:
        glove.stop_fingers()
        # Stop listener
        return False
    if key == KeyCode.from_char('a'):
        fingers[0] = 0.0
    if key == KeyCode.from_char('s'):
        fingers[1] = 0.0
    if key == KeyCode.from_char('d'):
        fingers[2] = 0.0
    if key == KeyCode.from_char('f'):
        fingers[3] = 0.0
    if key == KeyCode.from_char('g'):
        fingers[4] = 0.0
    update_fingers()


if __name__ == '__main__':

    # Collect events until released
    with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()
    
        
        
