import sys
import time

import math

from glove import Glove

horizontalfov = 70
vertcalfov = 60
histogram_size = 100
warning_frac = 0.1

class DepthGlove:
        
        def __init__(self, maxdist=10, mindist=1, horizontalfrac=1.0, verticalfrac=1.0, hand='left'):
                self._glove = Glove()
                self._maxdist = maxdist
                self._mindist = mindist
                self._distrange = maxdist - mindist
                self._horizontalfrac=horizontalfrac
                self._verticalfrac=verticalfrac
                self._histogram = []
             
        def update_glove(self, image, width, height):
                horizontalstart = (1-self._horizontalfrac)/2*width
                horizontalend = width - horizontalstart
                zonewidth = (horizontalend - horizontalstart)/5
                
                verticalstart = (1-self._verticalfrac)/2*height
                verticalend = height - verticalstart
                zoneheight = verticalend - verticalstart
                
                total_samples = zonewidth * zoneheight
                
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
                                        finger = 4-zone if hand == 'left' else zone
                                        fingers[finger] = 1 - bucket/(histogram_size - 1)
                                        break
                                        
                glove.set_fingers(fingers)
                        
        def _get_frac(self, val):
                val = max(min(self._maxdist, val), self._mindist)
                return (val - self._mindist)/self._distrange
        
        def _histogram_setup(self, val):
                self._histogram = [0]*histogram_size
                
        def _histogram_place(self, val):
                bucket = min(math.floor(histogram_size * val), histogram_size-1)
                self._histogram[bucket] = self._histogram[bucket] + 1
                
                
                
                
        
