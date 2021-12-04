import sys
import time

import board
import busio

from micropython import const

from TCA9548A import TCA9548A
from DRV2605 import DRV2605

class Multi_DRV2605(DRV2605):

    def __init__(self, i2c, tca, multibus=0):
        self._multibus = multibus
        self._multi = tca
        self._multi.bus_select(self._multibus)
        DRV2605.__init__(self, i2c) 
             
    def _read_u8(self, address):
        self._multi.bus_select(self._multibus)
        return DRV2605._read_u8(self, address)
        
    def _write_u8(self, address, val):
        self._multi.bus_select(self._multibus)
        DRV2605._write_u8(self, address, val)
        
