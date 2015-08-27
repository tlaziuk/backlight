#! /usr/bin/env python3
DEV_DIR = "/sys/class/backlight/"
import os
class BrightnessDevice:
    _min = int()
    _max = int()
    _current = int()
    def __init__(self, device, name=None):
        self.device = device
        if name == None:
            self.name = os.path.basename(device)
        else:
            self.name = name
        self._max_brightness = open(os.path.join(self.device, "max_brightness"), "r")
        self._brightness = open(os.path.join(self.device, "brightness"), "r+")
        self._read_brightness()
    def __del__(self):
        self._max_brightness.close()
        self._brightness.close()
    def __str__(self):
        return self.name
    def __iadd__(self, amount):
        return self.add(amount)
    def __isub__(self, amount):
        return self.sub(amount)
    def _read_brightness(self):
        self._min = int(0)
        self._max = int(self._max_brightness.readline()[:-1])
        self._current = int(self._brightness.readline()[:-1])
        return self
    def set(self, value):
        if value < self._min:
            value = self._min
        if value > self._max:
            value = self._max
        self._brightness.seek(0)
        self._brightness.write(str(value))
        self._current = value
        self._brightness.truncate()
        return self
    def get(self):
        return self._current
    def add(self, value):
        return self.set(self._current + value)
    inc = add
    def sub(self, value):
        return self.set(self._current - value)
    dec = sub

class BrightnessDevicePercentage(BrightnessDevice):
    def _read_brightness(self):
        self._min = int(0)
        self._max = int(self._max_brightness.readline()[:-1])
        current = int(self._brightness.readline()[:-1])
        self._current = int(current / self._max * 100)
        return self
    def set(self, val):
        value = int(val / 100 * self._max)
        if value < self._min:
            value = self._min
            val = 0
        if value > self._max:
            value = self._max
            val = 100
        self._brightness.seek(0)
        self._brightness.write(str(value))
        self._current = val
        self._brightness.truncate()
        return self

class Brightness:
    _device = list()
    def __init__(self, directory=DEV_DIR):
        self.__directory = directory
        if not os.path.exists(directory):
            raise FileNotFoundError("device directory "+directory+" does not exists")
        for i in os.listdir(directory):
            self._device.append(BrightnessDevicePercentage(os.path.join(directory, i), i))
    def __str__(self):
        return self.__directory
    def dec(self, val):
        for d in self._device:
            d.dec(val)
        return self
    def inc(self, val):
        for d in self._device:
            d.inc(val)
        return self
    def set(self, val):
        for d in self._device:
            d.set(val)
        return self

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Change the brightness of your displays.", prog="backlight")
    parser.add_argument("-D", "--directory", metavar="DIR", help="change directory of display devices", default=DEV_DIR)
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument("-d", "--dec", help="decrease value by given percentage value", action="store_true")
    group1.add_argument("-i", "--inc", help="increase value by given percentage value", action="store_true")
    parser.add_argument("percentage", metavar="N%", help="change brightness to given percentage value", type=int)
    args = parser.parse_args()
    backlight = Brightness(args.directory)
    if args.dec:
        backlight.dec(args.percentage)
    elif args.inc:
        backlight.inc(args.percentage)
    else:
        backlight.set(args.percentage)
    exit(0)
