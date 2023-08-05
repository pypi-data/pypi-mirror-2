# $Id: colortest.py 3880 2004-10-26 15:43:54Z sean $
#
# Project:  MapServer
# Purpose:  xUnit style Python mapscript tests of colorObj
# Author:   Sean Gillies, sgillies@frii.com
#
# ===========================================================================
# Copyright (c) 2004, Sean Gillies
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
# ===========================================================================
#
# Execute this module as a script from mapserver/mapscript/python
#
#     python tests/cases/colortest.py -v
#
# ===========================================================================

import os, sys
import unittest

# the testing module helps us import the pre-installed mapscript
from testing import mapscript
from testing import MapPrimitivesTestCase

# ===========================================================================
# Test begins now

class ColorObjTestCase(unittest.TestCase):
    
    def testColorObjConstructorNoArgs(self):
        """a color can be initialized with no arguments"""
        c = mapscript.colorObj()
        assert (c.red, c.green, c.blue, c.pen) == (0, 0, 0, -4)
    
    def testColorObjConstructorArgs(self):
        """a color can be initialized with arguments"""
        c = mapscript.colorObj(1, 2, 3)
        assert (c.red, c.green, c.blue, c.pen) == (1, 2, 3, -4)
    
    def testColorObjToHex(self):
        """a color can be outputted as hex"""
        c = mapscript.colorObj(255, 255, 255)
        assert c.toHex() == '#ffffff'
   
    def testColorObjToHexBadly(self):
        """raise an error in the case of an undefined color"""
        c = mapscript.colorObj(-1,-1,-1)
        self.assertRaises(mapscript.MapServerError, c.toHex)

    def testColorObjSetRGB(self):
        """a color can be set using setRGB method"""
        c = mapscript.colorObj()
        c.setRGB(255, 255, 255)
        assert (c.red, c.green, c.blue, c.pen) == (255, 255, 255, -4)
    
    def testColorObjSetHexLower(self):
        """a color can be set using lower case hex"""
        c = mapscript.colorObj()
        c.setHex('#ffffff')
        assert (c.red, c.green, c.blue, c.pen) == (255, 255, 255, -4)
    
    def testColorObjSetHexUpper(self):
        """a color can be set using upper case hex"""
        c = mapscript.colorObj()
        c.setHex('#FFFFFF')
        assert (c.red, c.green, c.blue) == (255, 255, 255)

    def testColorObjSetHexBadly(self):
        """invalid hex color string raises proper error"""
        c = mapscript.colorObj()
        self.assertRaises(mapscript.MapServerError, c.setHex, '#fffffg')

# ===========================================================================
# Run the tests outside of the main suite

if __name__ == '__main__':
    unittest.main()
    
