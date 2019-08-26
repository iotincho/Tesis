from utils.robot import Robot
import yaml
import math
from time import sleep
from numpy import arctan2, deg2rad, rad2deg, sqrt

class SimpleRobot(Robot):
    """
        fields:
            - delta_t : time between samples
            - bubble : bubbles, defines the bubble shape (Ki)
            - default_speed : default travel speed in m/s
    """
    def __init__(self,configFile):
        """ @param configFile yaml config file """
        #parse config file
        Robot.__init__(self,configFile)
        simple_cfg         = yaml.load(open(configFile,'r'))['simple_algorithm']
        self.delta_t       = simple_cfg['delta_t']
        self.bubble        = simple_cfg['bubble_boundary']
        self.default_speed = simple_cfg['default_speed']
        self.sensor_count  = simple_cfg['sensor_count']
        #assert sonar count in player, and yaml
        if  self.sensor_count != len(self.bubble) or \
             self.sensor_count != self.sonars[0].element_count:
             raise Exception("sensor_count(" + str(self.sensor_count)+\
                            "),buble length(" + str(len(self.bubble))+\
                            ") and sonar[0](" + str(self.sonars[0].element_count)+\
                            ") length do not match")
        self.simulation.set_pose2d("target",
                                    self.target.x,
                                    self.target.y,
                                    0)

    def drive(self):
        while not self.target_reached():
            self.read()
            if self.obstacle_in_bubble():
                self.avoid_obstacle()
            self.move_to_goal()
            sleep(self.delta_t)


    def avoid_obstacle(self):
        while not self.goal_visible():
            deg_alpha = self.get_rebound_angle()
            self.set_vel(self.default_speed*0.6,deg2rad(deg_alpha))
            self.read()

    def get_rebound_angle(self):
        alpha = 180/len(self.sensor_count)
        numerator = sum(list(map(lambda i:alpha*i*self.sonars[0].ranges[i],
                                    range(-a//2+1,a//2+1))))
        denominator = 0
        for i in range(0,self.sensor_count):
            denominator = denominator + self.sonars[0].ranges[i]
        return numerator/denominator



    def set_vel(self,speed,yaw):
        """change direction and speed
            @param speed: speed in m/s
            @param yaw: turn angle in radians"""
        self.position.set_cmd_vel(speed,0,yaw,1)

    def goal_visible(self):
        yaw    = self.get_goal_direction()
        sector = int(yaw / (180/self.sensor_count)) # TODO: revisar para formular mejor xq tiene error
        sector = sector + (self.sensor_count//2) #convierto el rango de  [4,-4] a [0,8] para indexar una lista
        return True if self.sonars[0].ranges[sector] >= \
                        self.sonars[0].max_range else False

    def target_reached(self):
        return False

    def obstacle_in_bubble(self, sonars_index=0):
        V = self.get_abs_vel()
        bubble_boundary = list(map(lambda Ki: Ki*V*self.delta_t, self.bubble))
        sonar_readings  = self.sonars[sonars_index].ranges
        for i in range(0,len(bubble_boundary)):
            if sonar_readings[i] <= bubble_boundary[i]:
                return True
        return False
