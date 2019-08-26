#!/usr/bin/python

import sys
import os
# base.py, pruebas y base para crear y probar sunciones con un robot simple
#

sys.path.append('/usr/local/lib/python2.7/site-packages/')
sys.path.append('/usr/local/lib64/python2.7/site-packages/')

import math
from playerc import *
import time

robot = playerc_client(None, 'localhost', 6665)
if robot.connect()!=0:
    raise Exception(playerc_error_str())

robot_position = playerc_position2d(robot, 0);
if robot_position.subscribe(PLAYER_OPEN_MODE):
    raise Exception(playerc_error_str())

robot_sonar = playerc_ranger(robot,0);
if robot_sonar.subscribe(PLAYER_OPEN_MODE):
    raise Exception(playerc_error_str())

robot_sonar.get_geom()
robot.read()

for i in range(0,50):
    for j in range(robot_sonar.ranges_count):
        print "%.3f, " %robot_sonar.ranges[j]
    print "\n"
    time.sleep(0.5)
    robot.read()


robot.disconnect()



exit(0)
