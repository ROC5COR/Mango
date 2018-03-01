#!/usr/bin/env python
"""
moonphase.py - Calculate Lunar Phase
Author: Sean B. Palmer, inamidst.com
Cf. http://en.wikipedia.org/wiki/Lunar_phase#Lunar_phase_calculation
Modified by Romain LE DONGE
"""

import math, decimal, datetime
dec = decimal.Decimal


def instance():
    return Moon()

class Moon():

    def go(self, args):
        pos = self.position()
        phase_name = self.phase(pos)

        #roundedpos = round(float(pos), 3)
        print("[MOON] This evening there will be the %s" % phase_name.lower())

    @staticmethod
    def position(now=datetime.datetime.now()):
       diff = now - datetime.datetime(2001, 1, 1)
       days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
       lunations = dec("0.20439731") + (days * dec("0.03386319269"))

       return lunations % dec(1)

    @staticmethod
    def phase(pos):
       index = (pos * dec(8)) + dec("0.5")
       index = math.floor(index)
       return {
          0: "New Moon",
          1: "Waxing Crescent",
          2: "First Quarter",
          3: "Waxing Gibbous",
          4: "Full Moon",
          5: "Waning Gibbous",
          6: "Last Quarter",
          7: "Waning Crescent"
       }[int(index) & 7]
