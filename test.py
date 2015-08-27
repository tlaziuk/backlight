#! /usr/bin/env python3

import unittest
from backlight import Brightness, BrightnessDevice, BrightnessDevicePercentage

class TestBrightness(unittest.TestCase):
    brightness = Brightness()
    delta = 10
    def setUp(self):
        self.v = self.brightness.get()
    def tearDown(self):
        self.brightness.set(self.v)
    def test_set(self):
        """ test Brightness.set() method """
        self.brightness.set(self.delta*2)
        self.assertAlmostEqual(self.brightness.get(), self.delta*2, delta=1)
    def test_inc(self):
        """ test Brightness.inc() method """
        current = self.brightness.get()
        self.brightness.inc(self.delta)
        self.assertAlmostEqual(self.brightness.get(), current+self.delta, delta=1)
    def test_dev(self):
        """ test Brightness.dec() method """
        current = self.brightness.get()
        self.brightness.dec(self.delta)
        self.assertAlmostEqual(self.brightness.get(), current-self.delta, delta=1)

if __name__ == "__main__":
    unittest.main()

