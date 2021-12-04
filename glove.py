import sys
import time

import board
import busio

from TCA9548A import TCA9548A
from multiplexed_drv2605 import Multi_DRV2605

class Glove:
        
        def __init__(self):
                self._i2c = busio.I2C(board.SCL, board.SDA)

                self._tca = TCA9548A(self._i2c)
                self._drvlist = []
                for i in range(5):
                        try:
                            self._drvlist.append(Multi_DRV2605(self._i2c, self._tca, multibus=i))
                        except ValueError:
                            print("no controller on bus " + str(i))
                            
                for drv in self._drvlist:
                        drv.RTP_write(0)
                        drv.RTP_on()
             
        def set_fingers(self, fingerlist):
                for drv, val in zip(self._drvlist, fingerlist):
                        drv.RTP_write(val)
                        
        def stop_fingers(self):
                for drv in self._drvlist:
                        drv.RTP_write(0)
        
