#!/usr/bin/env python3

'''
log2pgm.py : BreezySLAM Python demo.  Reads logfile with odometry and scan data
             from Paris Mines Tech and produces a .PGM image file showing robot 
             trajectory and final map.
             
For details see

    @inproceedings{coreslam-2010,
      author    = {Bruno Steux and Oussama El Hamzaoui},
      title     = {CoreSLAM: a SLAM Algorithm in less than 200 lines of C code},
      booktitle = {11th International Conference on Control, Automation, 
                   Vehicleics and Vision, ICARCV 2010, Singapore, 7-10 
                   December 2010, Proceedings},
      pages     = {1975-1979},
      publisher = {IEEE},
      year      = {2010}
    }
                 
Copyright (C) 2014 Simon D. Levy

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http://www.gnu.org/licenses/>.

Change log:

20-APR-2014 - Simon D. Levy - Get params from command line
05-JUN-2014 - SDL - get random seed from command line
'''

# Map size, scale10
MAP_SIZE_PIXELS          = 360
MAP_SIZE_METERS          = 10

from breezyslam.algorithms import Deterministic_SLAM, RMHC_SLAM
import numpy as np
from mines import MinesLaser, Rover, load_data
from data_utils import *

from sys import argv, exit, stdout
from time import time

def RunBreezySlam(dataset,use_odometry,seed):    
	# Load the data from the file, ignoring timestamps
    _, lidars, odometries = load_data('.', dataset)
    # print(odometries)
    # Build a robot model if we want odometry
    robot = Rover() if use_odometry else None
    # Create a CoreSLAM object with laser params and optional robot object
    slam = RMHC_SLAM(MinesLaser(), MAP_SIZE_PIXELS, MAP_SIZE_METERS, random_seed=seed) \
           if seed \
           else Deterministic_SLAM(MinesLaser(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)
    nscans = len(lidars)
    # Start with an empty trajectory of positions
    trajectory = []
    # Loop over scans    
    cnt = 0
    for scanno in range(nscans):
        if use_odometry:
            if cnt == 0:
                init_pose_x = odometries[0][1]
                init_pose_y = odometries[0][2]
                init_pose_theta = odometries[0][3]
            # Convert odometry to pose change (dxy_mm, dtheta_degrees, dt_seconds)
            velocities = robot.computePoseChange(odometries[scanno]) 
            # print(velocities)
            # velocities = (odometries[cnt][1]/1000,odometries[cnt][2]/1000,1)
            # print(velocities)
            # velocities = odometries[cnt][0],odometries[cnt][1],1
            # print((odometries[-1]))
            # Update SLAM with lidar and velocities
            slam.update(lidars[scanno], velocities)
            mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)
            slam.getmap(mapbytes)

        else:
            # Update SLAM with lidar alone
            slam.update(lidars[scanno])
        cnt = cnt + 1

        # Get new position
        x_mm, y_mm, theta_degrees = slam.getpos()    
        # Add new position to trajectory
        trajectory.append((x_mm, y_mm))                          
    # Create a byte array to receive the computed maps
    mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)
    # Get final map    
    slam.getmap(mapbytes)

    trajectory_data = []        
                                                               
    output_data = save_data("no_trajectory",mapbytes, (MAP_SIZE_PIXELS, MAP_SIZE_PIXELS))
   
    if use_odometry:
        test = fix_data(mapbytes, (MAP_SIZE_PIXELS, MAP_SIZE_PIXELS), init_pose_theta, init_pose_x-float(trajectory[0][0]), init_pose_y-float(trajectory[0][1]))
        plt.imshow(test)
        plt.savefig('test.png')
        output_data = test
    # Put trajectory into map as black pixels

    for coords in trajectory:
        x_mm, y_mm = coords  
        x_pix = mm2pix(x_mm)
        y_pix = mm2pix(y_mm)
        trajectory_data.append((x_mm/1000-7.379,y_mm/1000-5))
        # mapbytes[y_pix * MAP_SIZE_PIXELS + x_pix] = 0;
    # save_data("with_trajectory",mapbytes, (MAP_SIZE_PIXELS, MAP_SIZE_PIXELS))

    #test to see the 1st and last position
    # print("first",trajectory_data[0])
    # print("last",trajectory_data[-1])
    return output_data
            
# Helpers ---------------------------------------------------------        

def mm2pix(mm):
    return int(mm / (MAP_SIZE_METERS * 1000. / MAP_SIZE_PIXELS))  
