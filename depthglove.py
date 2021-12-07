import sys
import time

import math

from glove import Glove
import cv2

import numpy as np

horizontalfov = 70
vertcalfov = 60
histogram_size = 100
warning_frac = 0.1

x_first = False

class DepthGlove:
        
        def __init__(self, maxdist=1000, mindist=500, horizontalfrac=1.0, verticalfrac=1.0, hand='left'):
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
                
                
                #print("lower left: {}".format(image[-1][0]))
                
                #imax = np.amax(image)
                #print("min: " + str(np.amin(image)))
                #print("max: " + str(np.amax(image)))
                #cv2.imshow("depth", image / imax)
                image[image == 0.0] = self._maxdist
                
                
                #image = np.where(image == 0.0, self._maxdist, image)
                #print("min: " + str(np.amin(image)))
                #print("max: " + str(np.amax(image)))
                
                minarray = np.full(image.shape, self._mindist)
                maxarray = np.full(image.shape, self._maxdist)
                image = np.clip(image, minarray, maxarray)
                
                
                
                #cv2.imshow("depth", image / self._maxdist)
                
                #print("min: " + str(np.amin(image)))
                #print("max: " + str(np.amax(image)))
                
                #print("{} {} {} {} {} {} {}".format(
                #horizontalstart, horizontalend, zonewidth, verticalstart, verticalend, zoneheight, total_samples))
                
                fingers = [0]*5
                dist = []
                
                showimg = np.copy(image)
                #showimg[50:150, 250:350] = 0
                font = cv2.FONT_HERSHEY_SIMPLEX
                
                #print("shape {}".format(image.shape))
                
                for zone in range(5):
                        #self._histogram_setup()
                        
                        #for x in range(horizontalstart+zone*zonewidth, horizontalstart+(zone+1)*zonewidth):
                        #        for y in range(verticalstart, verticalend):
                        #                frac = self._get_frac(image[y][x])
                        #                self._histogram_place(frac)
                        
                        zoneleft = horizontalstart+zone*zonewidth
                        zoneright = horizontalstart+(zone+1)*zonewidth
                        histogram, binedges = np.histogram(image[verticalstart:verticalend, horizontalstart+zone*zonewidth:horizontalstart+(zone+1)*zonewidth],
                                bins=histogram_size)
                                
                        #print(histogram)
                        
                        integral = 0
                        target_integral = total_samples * warning_frac
                        for bucket in range(histogram_size):
                                integral = integral + histogram[bucket]
                                #print("{}: {}/{}".format(bucket, integral, target_integral))
                                if integral >= target_integral:
                                        finger = zone if self._hand == 'left' else 4-zone
                                        dist.append(binedges[bucket])
                                        #print(binedges)
                                        fingers[finger] = 1 - self._get_frac(binedges[bucket])
                                        break
                        cv2.line(showimg,(zoneleft,0),(zoneleft,image.shape[0]),(255,255,255),1)
                        cv2.putText(showimg,str("{:.2f}".format(dist[-1])),(zoneleft,50), font, 0.4,(255,255,255),1,cv2.LINE_AA)
                                        
                #print("fingers {}".format(fingers))
                #print("fingerdist {}".format(dist))
                cv2.imshow("depth", showimg / self._maxdist)
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
                
                
                
                
        
