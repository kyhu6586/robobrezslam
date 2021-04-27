'''
BreezySLAM: Simple, efficient SLAM in Python

vehicles.py: odometry models for different kinds of vehicles
(currently just wheeled vehicles)

Copyright (C) 2014 Suraj Bajracharya and Simon D. Levy

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http:#www.gnu.org/licenses/>.
'''

import math

class WheeledVehicle(object):
    '''
    An abstract class supporting ododmetry for wheeled robots.  Your implementing
    class should provide the method:
    
      extractOdometry(self, timestamp, leftWheel, rightWheel) --> 
        (timestampSeconds, leftWheelDegrees, rightWheelDegrees)      
    '''
    
    def __init__(self, wheelRadiusMillimeters, halfAxleLengthMillimeters):
        '''
        wheelRadiusMillimeters    radius of each odometry wheel   
        halfAxleLengthMillimeters half the length of the axle between the odometry wheels  
        '''
        self.wheelRadiusMillimeters = wheelRadiusMillimeters  
        self.halfAxleLengthMillimeters = halfAxleLengthMillimeters
        
        self.timestampSecondsPrev = None        
        self.x_posePrev = None
        self.y_posePrev = None
        self.theta_posePrev = None
                
    def __str__(self):
        
        return '<Wheel radius=%f mm Half axle Length=%f mm>' % \
        (self.wheelRadiusMillimeters, self.halfAxleLengthMillimeters)
        
    def __repr__(self):
        
        return self.__str__()
        
    def computePoseChange(self, timestamp, x_pose, y_pose, theta_pose):
        '''
        Computes pose change based on odometry.
        
        Parameters:
        
          timestamp          time stamp, in whatever units your robot uses       
          x_pose  odometry for left wheel, in whatever form your robot uses       
          y_pose odometry for right wheel, in whatever form your robot uses
        
        Returns a tuple (dxyMillimeters, dthetaDegrees, dtSeconds)
        
          dxyMillimeters     forward distance traveled, in millimeters
          dthetaDegrees change in angular position, in degrees
          dtSeconds     elapsed time since previous odometry, in seconds
        '''                      
        dxyMillimeters = 0
        dthetaDegrees = 0
        dtSeconds = 0
                       
        timestampSecondsCurr, x_poseCurr, y_poseCurr , theta_poseCurr= \
            self.extractOdometry(timestamp, x_pose, y_pose,theta_pose)
            
        if self.timestampSecondsPrev != None:  
            
            dx = (x_poseCurr - self.x_posePrev)*1000
            dy = (y_poseCurr - self.y_posePrev)*1000
            
            dxyMillimeters =  math.sqrt(dx**2+dy**2)     
            dthetaDegrees = math.degrees(theta_poseCurr - self.theta_posePrev)
            dtSeconds = (timestampSecondsCurr - self.timestampSecondsPrev)*10**-6
                
        # Store current odometry for next time
        self.timestampSecondsPrev = timestampSecondsCurr        
        self.x_posePrev = x_poseCurr
        self.y_posePrev = y_poseCurr
        self.theta_posePrev = theta_poseCurr

        # Return linear velocity, angular velocity, time difference
        return dxyMillimeters, dthetaDegrees, dtSeconds
