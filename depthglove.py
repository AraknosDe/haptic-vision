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

run_fingers = True

x_first = False

class DepthGlove:
        
        def __init__(self, maxdist=2500, mindist=500, horizontalfrac=1.0, verticalfrac=0.5, hand='left'):
                self._glove = Glove()
                self._maxdist = maxdist
                self._mindist = mindist
                self._distrange = maxdist - mindist
                self._horizontalfrac=horizontalfrac
                self._verticalfrac=verticalfrac
                self._histogram = []
                self._hand = hand
             
        def update_glove(self, image):
                image = np.flip(image, axis=1)
                
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
                
                #total_samples = zonewidth * zoneheight
                
                
                #print("lower left: {}".format(image[-1][0]))
                
                #imax = np.amax(image)
                #print("min: " + str(np.amin(image)))
                #print("max: " + str(np.amax(image)))
                #cv2.imshow("depth", image / imax)
                #image[image == 0.0] = -1.0#self._mindist
                
                
                #image = np.where(image == 0.0, self._maxdist, image)
                #print("min: " + str(np.amin(image)))
                #print("max: " + str(np.amax(image)))
                
                zeroimg = np.zeros(image.shape)
                minarray = np.full(image.shape, self._mindist)
                maxarray = np.full(image.shape, self._maxdist)
                image = np.clip(image, zeroimg, maxarray)
                
                
                
                #cv2.imshow("depth", image / self._maxdist)
                
                #print("min: " + str(np.amin(image)))
                #print("max: " + str(np.amax(image)))
                
                #print("{} {} {} {} {} {} {}".format(
                #horizontalstart, horizontalend, zonewidth, verticalstart, verticalend, zoneheight, total_samples))
                
                fingers = [0]*5
                dist = []
                
                
                bottomadd = zonewidth
                showimg = np.zeros((image.shape[0]+bottomadd, image.shape[1]))
                showimg[0:image.shape[0], :] = np.clip(image, minarray, maxarray) 
                showimg[0:image.shape[0], :] = 1 - (showimg[0:image.shape[0], :] - self._mindist)/self._distrange
                #showimg[50:150, 250:350] = 0
                font = cv2.FONT_HERSHEY_SIMPLEX
                
                #print("shape {}".format(image.shape))
                
                for zone in range(5):
                        finger = 4-zone if self._hand == 'left' else zone
                        #self._histogram_setup()
                        
                        #for x in range(horizontalstart+zone*zonewidth, horizontalstart+(zone+1)*zonewidth):
                        #        for y in range(verticalstart, verticalend):
                        #                frac = self._get_frac(image[y][x])
                        #                self._histogram_place(frac)
                        
                        zoneleft = horizontalstart+zone*zonewidth
                        zoneright = horizontalstart+(zone+1)*zonewidth
                        histogram, binedges = np.histogram(image[verticalstart:verticalend, horizontalstart+zone*zonewidth:horizontalstart+(zone+1)*zonewidth],
                                bins=histogram_size, range=(self._mindist, self._maxdist))
                        
                        total_samples = np.sum(histogram)
                        #print(histogram)
                        
                        integral = 0
                        target_integral = total_samples * warning_frac
                        if total_samples == 0:
                                dist.append(self._maxdist)
                                fingers[finger] = 1 - self._get_frac(self._maxdist)
                        else:
                                for bucket in range(histogram_size):
                                        integral = integral + histogram[bucket]
                                        #print("{}: {}/{}".format(bucket, integral, target_integral))
                                        if integral >= target_integral:
                                                dist.append(binedges[bucket])
                                                #print(binedges)
                                                fingers[finger] = 1 - self._get_frac(binedges[bucket])
                                                break
                        cv2.line(showimg,(zoneleft,0),(zoneleft,image.shape[0]),(0,0,0),1)
                        #cv2.putText(showimg,str("{:.0f}".format(dist[-1])),(zoneleft+5,30), font, 0.6,(1,0,0),5,cv2.LINE_AA)
                        #cv2.putText(showimg,str("{:.0f}".format(dist[-1])),(zoneleft+5,30), font, 0.6,(0,0,0),3,cv2.LINE_AA)
                        cv2.circle(showimg,
                                (int(zoneleft+bottomadd/2), int(bottomadd/2+image.shape[0])),
                                int(bottomadd/2), fingers[finger], -1)
                        textcolor = 1 if fingers[finger] < 0.5 else 0
                        cv2.putText(showimg,str("{:.0f}".format(dist[-1])),(zoneleft+5,int(bottomadd/2+image.shape[0]+5)), font, 0.6,(textcolor,0,0),2,cv2.LINE_AA)
                        
                cv2.line(showimg,(horizontalend,0),(horizontalend,image.shape[0]),(0,0,0),1)
                cv2.line(showimg,(0,verticalstart),(image.shape[1],verticalstart),(0,0,0),1)
                cv2.line(showimg,(0,verticalend),(image.shape[1],verticalend),(0,0,0),1)
                #print("fingers {}".format(fingers))
                #print("fingerdist {}".format(dist))
                cv2.imshow("depth", showimg)
                if run_fingers:
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
                
                
                
                
        
