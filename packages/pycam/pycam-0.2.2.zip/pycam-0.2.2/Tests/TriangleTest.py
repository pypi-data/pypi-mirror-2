#!/usr/bin/python
import sys
sys.path.insert(0,'.')

import math

from pycam.Geometry import *
from pycam.Gui.Visualization import Visualization


p1 = Point(1,0,0)
p2 = Point(0,1,0)
p3 = Point(0,0,1)
t = Triangle(p1,p2,p3)
t.id=1
t.calc_circumcircle()

def DrawScene():
    t.to_OpenGL()

if __name__ == "__main__":

    print "p1=" + str(p1);
    print "p2=" + str(p2);
    print "p3=" + str(p3);

    print "p2-p1=" + str(p2.sub(p1))
    print "p3-p2=" + str(p3.sub(p2))
    print "p1-p3=" + str(p1.sub(p3))

    print "p2.p1=" + str(p2.dot(p1))
    print "p3.p2=" + str(p3.dot(p2))
    print "p1.p3=" + str(p1.dot(p3))

    print "p1xp2=" + str(p1.cross(p2))
    print "p2xp3=" + str(p2.cross(p3))
    print "p3xp1=" + str(p3.cross(p1))

    print t

    print "circ(t) = %s@%s" % (t.radius(),t.center())


    Visualization("VisualizationTest", DrawScene)
