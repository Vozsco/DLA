# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 17:24:52 2020

@author: User
"""

"""
This function finds the fractal dimensionality of the cluster 
"""

from dlaCluster import DLAcluster
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
#   FD FUNCTION

#   This function measures the fracttal dimensionality of a cluster.
#   Parameters are the same as the Aggregation function as it calls said
#   function within it.

# =============================================================================

def FD(SeedChoice, BiasAmount, BiasChoice, MaxWalker, Probability,Radius, GIFChoice, LineColourChoice, BackColourChoice):
    #Creates a an array of 10 to the size of the radius, with increasing steps of 5
    #This means that a radius is created for size 10, then size 10+5
    #and on and on until the user defined Radius is met.
    #User is restricted by the fact that they can only choose a radius greater
    #than a pre-defined radius. This process is commented and described in
    # runner.py
    RadiusArray=np.arange(10,Radius,5)
    
    #Initialises Mass
    mass=[]

    #This for loop will loop through all the values of the RadiusArray,
    #calling the aggregation function constantly to create a cluster    
    for r in RadiusArray:
        #massValue and lattice save the results from the Aggregation function.
        massValue, lattice = DLAcluster(SeedChoice, BiasAmount, BiasChoice, MaxWalker, Probability, r, GIFChoice, LineColourChoice, BackColourChoice)
        #Mass value is appended into the mass value
        mass.append(massValue)
    
    
    #The following will find fits for the mass and radius of the cluster
    #We are expecting a linear function, of the form
    # y = a + bx
    #In this casem a = scaling component, b = power of t
    
    #This produces natural logs of all the arrays
    logRadius=np.log(RadiusArray)
    logMass=np.log(mass)
    
    #We use the numpy library to produce a poly fit of the logs we made 
    #earlier
    fitLog=np.polyfit(logRadius, logMass,1)
    fitLogFunc=np.poly1d(fitLog)
    
    #The results are printed out in the console for the user to see
    print("Log-Log plot: slope = ",fitLog[0]," shift: ",fitLog[1])
    print("Log-Log: form is e^",fitLog[1],"* r^",fitLog[0])
    
    #We create a string that can be put onto the log plot later
    num = str(np.round(fitLog[0], 3))
    
    #This actually plots the LogMass-LogRadius plot
    
    fig=plt.subplot()
    plt.scatter(logRadius,logMass, color='blue', edgecolors='blue', s=30)
    plt.plot(logRadius, fitLogFunc(logRadius),color='indigo', lw=2)
    plt.title("Log-Log plot, Mass vs Radius",fontsize=18)
    plt.xlabel("Log Radius",fontsize=12)
    plt.ylabel("Log Mass",fontsize=12)
    fig.text(2.6,4.3,'Fractal Dimensionality:' + num) 
    plt.savefig('images/logRadiusMass.png')
    plt.show()