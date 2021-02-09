# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 13:14:42 2020

@author: User
"""

##Square Aggregrate
import random
import numpy
import os
import matplotlib.pyplot as plt
from matplotlib import colors



############ Custom functions
from checkAround import checkAround
from randomAtRadius import randomAtRadius
#from indexM import indexM
############


def SquareCluster(radius, needGif, LineColour, BackColour):

    
    #check if folder "images" exists, and if not - create it
    if not os.path.isdir("images"):
        os.mkdir("images")
    
    if needGif:

        import imageio

    
    #initialize variables that are dependent upon the radius
    # note - we add 2 to the parameters to get a thick border between the edges of the disk and square
    # x coordinate of a seed particle
    seedX = radius
    # y coordinate of a seed
    seedY = radius
    # size of the grid to account for field of wandering around
    squareSize = radius*2

    matrix=numpy.zeros((squareSize, squareSize))

    for row in range (0,squareSize):
        for col in range (0,squareSize):
            #put a seed particle
            if row==seedY and col==seedX: 
                matrix[row][col]=1
                for count in range (-radius, seedX):
                    for count in range (-radius, seedY):
                       matrix[row][col-radius+count] = 1
                       matrix[row-radius+count][col] = 1
                    
            #define field outside of circle
            elif numpy.sqrt((seedX-col)**2+(seedY-row)**2)>radius:
                matrix[row][col]=2
    cmap = colors.ListedColormap([BackColour,LineColour, BackColour])

    # Initialize the random walker counter
    randomWalkersCount = 0

    # Set the cluster to NOT be complete
    Complete = False

    # Start running random walkers
    addedCount=0 #keep track of number added

    # initialize array for the used interval for graphing
    usedInterval=[]

    while not Complete:
        # Release a walker
        randomWalkersCount += 1
        random.seed()

        # Generate a (Xstart, Ystart) for walker, need within radius
        location=randomAtRadius(radius, seedX, seedY)

        # Initialize variables, like Friend tag and near edge identifier
        foundFriend = False #not near other particle
        nearEdge = False #not near the edge of the field


        # Set an individual walker out, stop if found a 'friend', give up if it reached the edge of the board
        while not foundFriend and not nearEdge:
            # Run the checking/walking function
            locationNew,foundFriend, nearEdge, exitCircle = checkAround(location,squareSize,matrix)

            # Add to the cluster if near a friend
            if foundFriend:
                # current location, replace with 1 and stop
                matrix[location[1]][location[0]] = 1
                addedCount+=1

            # Otherwise, save the location
            else:
                location = locationNew
        
        intervalSavePic=range(2,400000,500)
        if randomWalkersCount in intervalSavePic:
            print("Added ", randomWalkersCount, " random walkers.", " Cluster: ", addedCount)
        if needGif:
            if randomWalkersCount in intervalSavePic:
                usedInterval.append(randomWalkersCount) #append to the used count
                label=str(randomWalkersCount)
                plt.title("DLA Cluster", fontsize=20)
                plt.matshow(matrix, interpolation='nearest',cmap=cmap)#plt.cm.Blues) #ocean, Paired
                plt.xlabel("$x$", fontsize=15)
                plt.ylabel("$y$", fontsize=15)
                plt.savefig("images/cluster{}.png".format(label), dpi=200)
                plt.close()
       
        if randomWalkersCount==400000:
            print("ERROR TOO MANY ITERATIONS")
            Complete = True

        # Once it finds a friend and leaves the previous loop, we must check if it
        # is also touching a circular wall. If so, we have a complete cluster
        if foundFriend and exitCircle:
            print("Random walkers in the cluster: ",addedCount)
            Complete = True
    
    plt.title("DLA Cluster", fontsize=20)
    plt.matshow(matrix, interpolation='nearest',cmap=cmap)#plt.cm.Blues) #ocean, Paired
    plt.xlabel("$x$", fontsize=15)
    plt.ylabel("$y$", fontsize=15)
    plt.savefig("images/cluster.png", dpi=200)
    plt.close()

    print(usedInterval)

    if needGif:
        with imageio.get_writer('images/movie.gif', mode='I') as writer:
            for i in usedInterval:
                filename="images/cluster"+str(i)+".png"
                image = imageio.imread(filename)
                writer.append_data(image)
                os.remove(filename)
            image = imageio.imread("images/cluster.png")
            writer.append_data(image)

    return addedCount, matrix


