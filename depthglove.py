import sys
import time

import math

from glove import Glove

import numpy as np

horizontalfov = 70
vertcalfov = 60
histogram_size = 100
warning_frac = 0.1

x_first = True

class DepthGlove:
        
        def __init__(self, maxdist=3000, mindist=300, horizontalfrac=1.0, verticalfrac=1.0, hand='left'):
                self._glove = Glove()
                self._maxdist = maxdist
                self._mindist = mindist
                self._distrange = maxdist - mindist
                self._horizontalfrac=horizontalfrac
                self._verticalfrac=verticalfrac
                self._histogram = []
                self._hand = hand
             
        def update_glove(self, image):
                width = image.shape[0]
                height = image.shape[1]
                if not x_first:
                        width, height = height, width
                        
                horizontalstart = math.floor((1-self._horizontalfrac)/2*width)
                horizontalend = width - 1 - horizontalstart
                zonewidth = math.floor((horizontalend - horizontalstart + 1)/5)
                
                verticalstart = math.floor((1-self._verticalfrac)/2*height)
                verticalend = height - 1 - verticalstart
                zoneheight = verticalend - verticalstart + 1
                
                total_samples = zonewidth * zoneheight
                
                #print("{} {} {} {} {} {} {}".format(
                #horizontalstart, horizontalend, zonewidth, verticalstart, verticalend, zoneheight, total_samples))
                
                fingers = [0]*5
                
                for zone in range(5):
                        self._histogram_setup()
                        for x in range(horizontalstart+zone*zonewidth, horizontalstart+(zone+1)*zonewidth):
                                for y in range(verticalstart, verticalend):
                                        frac = self._get_frac(image[x][y])
                                        self._histogram_place(frac)
                        integral = 0
                        target_integral = total_samples * warning_frac
                        for bucket in range(histogram_size):
                                integral = integral + self._histogram[bucket]
                                if integral >= target_integral:
                                        finger = 4-zone if self._hand == 'left' else zone
                                        fingers[finger] = 1 - bucket/(histogram_size - 1)
                                        break
                                        
                #print("fingers {}".format(fingers))
                self._glove.set_fingers(fingers)
                
        def stop_fingers(self):
                self._glove.stop_fingers()
                        
        def _get_frac(self, val):
                val = max(min(self._maxdist, val), self._mindist)
                return (val - self._mindist)/self._distrange
        
        def _histogram_setup(self):
                self._histogram = [0]*histogram_size
                
        def _histogram_place(self, val):
                bucket = min(math.floor(histogram_size * val), histogram_size-1)
                self._histogram[bucket] = self._histogram[bucket] + 1
                
                
                
                
        
