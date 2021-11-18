#!/usr/bin/env python

'''
    Basic Kalman Filter Implementation
    Predicts velocity in 2D space
'''

import numpy as np

#* Random data set
#* Actual/Observed Velocity
actual_vel = np.random.random([10,2,1])*10
#print(actual_vel[0])
#* Measured sensor data
sensor_data = np.random.random([10,2,50])
#print(sensor_data[0])
#* Time step
dt = 0.1 #? seconds

sc = np.ones([4,1])*10
#* System State Variable
x_0 = np.random.random([4,1])*sc
print(x_0)

#* State Transition matrix
F = np.array(([1, dt, 0, 0],[0 , 0, 1, dt]))
print(F)
print(F.dot(x_0))

#* Process Noise matrix
sig_q = 0.15 #? m/s^2
Q = np.array(([1, dt, 0, 0],[0, 0, 1, dt]))