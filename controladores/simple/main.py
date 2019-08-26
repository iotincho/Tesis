#!/usr/bin/python

import time
import yaml
from .functions import SimpleRobot
import numpy as np
if __name__=='__main__':
    robot = SimpleRobot('simple/conf.yaml')

    #update proxies
    robot.read()
    robot.drive()
    #for i in range(0,50):
    #    for j in range(robot.sonars[0].ranges_count):
    #        print "%.3f, " %robot.sonars[0].ranges[j]
    #        print "%.3f, " %np.rad2deg(robot.position.pa)
    #    print "\n"
    #    time.sleep(0.5)
    #    robot.read()



    exit(0)
