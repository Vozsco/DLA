# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 17:24:56 2020

@author: User
"""

"""
Function that generates the random pos, at the specified Radius
INPUT = Radius, Xseed, Yseed
OUTPUT = [x,y] pos
"""

import random
import numpy as np
def randomAtRadius(Radius, Xseed, Yseed):
    theta = 2*np.pi*random.random() #generate random theta
    x=int(Radius*np.cos(theta))+Xseed #use trig to transfer into X
    y=int(Radius*np.sin(theta))+Yseed #find Y coordinate
    pos=[x, y] #save locaction
    return pos