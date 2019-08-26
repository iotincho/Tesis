import sys
import os
# base.py, pruebas y base para crear y probar sunciones con un robot simple
#

sys.path.append('/usr/local/lib/python2.7/site-packages/')
sys.path.append('/usr/local/lib64/python2.7/site-packages/')

from playerc import *
import yaml
from numpy import deg2rad, sqrt, arctan2
class Robot():
    """ fields:
            - connection :connnection with server
            - name : instance's name
            - start_pos : <tuple> initial position (x,y,yaw)
            - target : <tuple> target (x,y)
            - simulation : proxy to simulation driver
            - sonars : list of proxies to sonar rangers
            - lasers : list of proxies to laser rangers
    """
    def __init__(self, configFile):
        """ @param configFile yaml config file """
        #parse config file
        robot_cfg       = yaml.load(open(configFile,'r'))['robot']
        # connect to server
        self.connection = self.connect(robot_cfg['host'],robot_cfg['port'])
        # store parameters
        self.name           = robot_cfg['name']
        self.start_pos      = self.Coordinate2d()
        self.start_pos.x,\
        self.start_pos.y,\
        self.start_pos.yaw  = robot_cfg['start_pos']
        self.target         = self.Coordinate2d()
        self.target.x,\
        self.target.y       = robot_cfg['target']
        ### connections to drivers
        # connect to simulation
        self.simulation     = self.simulation_connect(index=0)
        #connect to position2d
        self.position       = self.position2d_connect(index=0)
        # connect to sonars
        if len(robot_cfg['sonars']) > 0:
            self.sonars=[]
            for i in range(0,len(robot_cfg['sonars'])):
                self.sonars.append(self.ranger_connect(robot_cfg['sonars'][i]))
                self.sonars[i].get_geom()

        # connect to lasers
        if len(robot_cfg['lasers']) > 0:
            self.lasers=[]
            for i in range(0,len(robot_cfg['lasers'])):
                self.lasers.append(self.ranger_connect(robot_cfg['lasers'][i]))
                self.laser[i].get_geom()


        self.move_to_start_pos()

    def read(self):
        """update proxies"""
        return self.connection.read()

    def move_to_start_pos(self):
        """move robot to start position"""
        self.simulation.set_pose2d(self.name,
                                    self.start_pos.x,
                                    self.start_pos.y,
                                    deg2rad(self.start_pos.yaw))

    def connect(self,host,port=6665):
        """connect to player server"""
        port  = int(port)
        robot = playerc_client(None, host, port)
        if robot.connect()!=0:
            raise Exception(playerc_error_str())
        return robot

    def position2d_connect(self,index):
        """connect to position2d driver"""
        position = playerc_position2d(self.connection, index);
        if position.subscribe(PLAYER_OPEN_MODE):
            raise Exception(playerc_error_str())
        return position

    def ranger_connect(self,index):
        """connect to ranger driver"""
        sonar = playerc_ranger(self.connection,index);
        if sonar.subscribe(PLAYER_OPEN_MODE):
            raise Exception(playerc_error_str())
        return sonar

    def simulation_connect(self,index):
        """connect to simulation driver (stage driver)"""
        simulation = playerc_simulation(self.connection,index)
        if simulation.subscribe(PLAYERC_OPEN_MODE) !=0:
            raise Exception(playerc_error_str())
        return simulation

    def get_abs_vel(self):
        """ return the absolute actual velocity"""
        return sqrt(self.position.vx**2 + self.position.vy**2)

    def move_to_goal(self):
        dyaw = self.get_goal_direction()
        self.set_vel(self.default_speed,dyaw)

    def get_goal_direction(self):
        """@return angle in radians of the direction
                   to goal from the robot nose
        """
        dx   = self.target.x-self.position.px
        dy   = self.target.y-self.position.py
        dyaw = arctan2(dy, dx)-self.position.pa
        return dyaw

    class Coordinate2d():
        x   = None
        y   = None
        yaw = None
