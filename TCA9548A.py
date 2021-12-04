from micropython import const

from adafruit_bus_device.i2c_device import I2CDevice

# Internal constants:
_TCA9548A_ADDR = const(0x70)

class TCA9548A:

    # Class-level buffer for reading and writing data with the sensor.
    # This reduces memory allocations but means the code is not re-entrant or
    # thread safe!
    

    def __init__(self, i2c, address=_TCA9548A_ADDR):
        self._BUFFER = bytearray(1)
        self._device = I2CDevice(i2c, address)
        self._lastbus = -1
        self.bus_select(0)

    def _write_u8(self, val):
        # Write an 8-bit unsigned value to the specified 8-bit address.
        with self._device as i2c:
            self._BUFFER[0] = val & 0xFF
            i2c.write(self._BUFFER, end=1)

    def bus_select(self, bus):
        if bus <= 7 and bus >=0:
            if bus != self._lastbus:
                self._write_u8(1 << bus)
                self._lastbus = bus
