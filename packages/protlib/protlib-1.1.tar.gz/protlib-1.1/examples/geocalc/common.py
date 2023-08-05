import sys
sys.path.append("../..")

import logging
logging.basicConfig(level = logging.INFO)

from protlib import *

SERVER_ADDR = ("127.0.0.1", 12321)

class Point(CStruct):
    code = CShort(always = 1)
    x    = CFloat()
    y    = CFloat()

class Vector(CStruct):
    code = CShort(always = 2)
    p1   = Point.get_type()
    p2   = Point.get_type()

class PointGroup(CStruct):
    code = CShort(always = 3)
    count = CInt()

class Rectangle(CStruct):
    code = CShort(always = 4)
    points = CArray(4, Point)
