"""
This is the main funciton for the DLA cluster model. 
INPUT: Radius (Integer), needGif (Boolean)
OUTPUT: # of particles in the cluster (int), resulting lattice (populated by 0, 1, 2)
SAVED OUTPUT: in the folder images saves the resulting cluster image and .gif file
    -note: if folder images does not exist, it is created first
"""


import random
import numpy as np
import os
import matplotlib.pyplot as plt
import ctypes
from matplotlib import colors

# =============================================================================
#   RandomPos FUNCTION

#   Function that generates the random pos, using the specified Radius
#   Parameter of the function is user defined Radius. 
#   Radius also creates the other parameters: Xseed and YSeed 
#   This function outputs the injection position of a walker.

# =============================================================================

def RandomPos(Radius, Xseed, Yseed):
    #Produces a random angle
    #By trigonometry, using the radius as one of the lines of a triangle,
    #and the angle, a position is found for the x-coordinate, and 
    #the y-coordinate.
    #The new position is saved as an array of the x and y coordinates.
    #Function returns this value
    
    theta = 2*np.pi*random.random()
    x=int(Radius*np.cos(theta))+Xseed
    y=int(Radius*np.sin(theta))+Yseed
    pos=[x, y]
    
    return pos

# =============================================================================
#   NeighbourCheck FUNCTION

#   Function checks the injection position, making sure it is not at the edge
#   of the lattice
#   Parameters of the BiasAmount, the BiasChoice (direction of bias)
#   the position of the particle, the LatticeSize (the space the walker 
#   can be in), and the lattice itself (the position of other particles).
#   This function outputs whether or not the particle is bordering a particle
#   and determines the path it will take

# =============================================================================
def NeighbourCheck(BiasAmount, BiasChoice, pos, LatticeSize, lattice):
    #Initialises Boolean variables
    FriendFound = False 
    ExitBoundary = False
    EdgeFound=False 
    
    #This if statemate will set EdgeFound = True when the current position of
    #the particle plus one unit in any direction is outside the Lattice size
    #It does this by numerical analysis, it asks if you add/subtract 1 unit in
    #any direction to the current position, is it greater/smaller than the the
    #LatticeSize
    
    if (pos[1] + 1) > LatticeSize - 1 or (pos[1] - 1) < 1 or (pos[0] + 1) > LatticeSize - 1 or (pos[0] - 1) < 1:
        #If the above condition is met, then the EdgeFound is declared true,
        #all other pieces of code in this function are not ran as 
        #a consequence of this
        EdgeFound = True

    if not EdgeFound:
        
        #This declared variable is the status of the lattice unit one unit 
        #down from the current position
        DownNeighbour = lattice[pos[1]+1,pos[0]]
        
        if DownNeighbour == 1:
            #If there is a particle beneath it, then it has found a cluster to
            #stick on.
            FriendFound = True

        if DownNeighbour == 2:
            #If there is not a particle beneath it, then it will carry on and
            #will exit the current position
            ExitBoundary = True
            
        #This declared variable is the status of the lattice unit one unit 
        #up from the current position
        UpNeighbour=lattice[pos[1]-1,pos[0]]
        
        if UpNeighbour==1:           
            FriendFound=True            
            #If there is a particle above it, then it has found a cluster to
            #stick on.           
        if UpNeighbour==2:
            #If there is not a particle above it, then it will carry on and
            #will exit the current position
            ExitBoundary=True
            
        #This declared variable is the status of the lattice unit one unit 
        #right from the current position
        neighborRight=lattice[pos[1],pos[0]+1]
        
        if neighborRight==1:
            #If there is a particle to the right, then it has found a cluster
            #to stick on.  
            FriendFound=True
            
        if neighborRight==2:
            #If there is not a particle to the right, then it will carry on
            #and will exit the current position
            ExitBoundary=True
            
        #This declared variable is the status of the lattice unit one unit 
        #left from the current position
        neighborLeft=lattice[pos[1],pos[0]-1]
        
        if neighborLeft==1:
            #If there is a particle to the left, then it has found a cluster
            #to stick on.  
            FriendFound=True
            
        if neighborLeft==2:
            #If there is not a particle to the left, then it will carry on
            #and will exit the current position
            ExitBoundary=True

    #This if statement is only activated the particle has to take a path to
    #find a cluster to stick on
    if not FriendFound and not EdgeFound:
        #A random number between 0 and 1 is generated
        Chance = random.random()
        
        #If the user chose to have no bias then the following occurs
        if BiasChoice == 'None':

            if Chance < 0.25:
                #If the RNG produces a number below 0.25 then the particle moves
                #left
                pos = [pos[0]+1, pos[1]]
                
            elif Chance < 0.50:
                #If the RNG produces a number below 0.50 then the particle moves
                #right
                pos = [pos[0]-1, pos[1]]
           
            elif Chance < 0.75:
                #If the RNG produces a number below 0.75 then the particle moves
                #Down
                pos = [pos[0],pos[1] - 1]
                
            elif Chance < 1:
                #If the RNG produces a number below 1 then the particle moves
                #Up
                pos = [pos[0],pos[1] + 1]
                
        #If the user chooses to have a bias in the x-axis, this code runs
        if BiasChoice == 'x-Axis':      
            if Chance > 0.5-BiasAmount :
                #By convention, the right of the particle is the positive
                #The user chose a bias that could be between -0.5 and positive
                #0.5. Going to the extreme, every 0.01 step is a 2% chance
                #increase of a particle walk's going in that direction.
                #-0.5 is actually a 100% chance that a particle will go left
                #due to this.
                pos = [pos[0]-1, pos[1]]         
                
            elif Chance < 0.50-BiasAmount:
                #left
                pos = [pos[0]+1, pos[1]]
                
            if Chance < 0.5:
                #The y-direction is unchanged regardless of bias chosen
                #As such it is a simple random number inequality comparison.
                pos = [pos[0],pos[1] - 1]
                
            elif Chance > 0.5:
                #Up
                pos = [pos[0],pos[1] + 1]

    return (pos, FriendFound, EdgeFound, ExitBoundary)

# =============================================================================
#   Aggregation FUNCTION

#   Function is called by the toggle function 
# =============================================================================

def DLAcluster(SeedChoice, BiasAmount, BiasChoice, MaxWalker, Probability, Radius, GIFChoice, LineColour, BackColour):
    
    # This checks to see that if in the file where the project is located, is
    # there an image folder
    if not os.path.isdir("images"):
        #If there isn't, then is creates one at that directory
        os.mkdir("images")
        
    if GIFChoice:
        #Imports a library called imageio that is used in gif creation
        import imageio
        
    #If the user chose for the seed shape to be a singular dot
    if SeedChoice == 'Dot':
        #Initialize variables dependant on the Radius
        #Adding 2 to the Xseed and YSeed  gives a thick border between the 
        #lattice and the injection circle
        
        #Sets the x-coordinate of the Seed
        Xseed = Radius+2 
        #Sets the y-coordinate of the seed
        Yseed = Radius+2 
        #The size of the Lattice, basically where a walker can move around.
        #The +3 allows for particles to exit a cluster but 
        #still be recongnised as being
        #in the latice
        LatticeSize = Radius*2+3

        #Produces the actual lattice based on the size of the lattice
        #Lattice is actually just an empty array
        lattice=np.zeros((LatticeSize, LatticeSize))
        
        #Initalises every intersection of a column and a row to be populated
        #by nothing if it does not match the seed particle.
        for row in range (0,LatticeSize):
            for col in range (0,LatticeSize):
                
                #Places the Seed Particle into the lattice, with the Rows as
                #the y-coordinate and the columns are the x-coordinates
                if row==Yseed and col==Xseed: 
                    lattice[row][col]=1
                    
                #Next piece creates a field outside of the injection circle
                #the kill zone for the particles 
                elif np.sqrt((Xseed-col)**2+(Yseed-row)**2)>Radius:
                    
                    lattice[row][col]=2
    
    #If the user chose to have a line seed instead then this code runs
    elif SeedChoice =='Line':
        #Initialize variables dependant on the Radius
        #Sets the x-coordinate of the Seed
        Xseed = Radius
        #Sets the y-coordinate of the seed
        Yseed = Radius
        #The size of the Lattice
        LatticeSize = Radius*2
        
        #Produces the actual lattice based on the size of the lattice
        #Lattice is actually just an empty array
        lattice=np.zeros((LatticeSize, LatticeSize))


        for row in range (0,LatticeSize):
            for col in range (0,LatticeSize):
                
                #Places the Seed Particle into the lattice, with the Rows as
                #the y-coordinate and the columns are the x-coordinates
                if row==Yseed and col==Xseed: 
                    lattice[row][col]=1
                    for count in range (-Radius, Xseed):
                        lattice[row][col-Radius+count] = 1
                    #Counts all the way from the -Radius to the x seed,
                    #Fills the row with populated units, meaning a line seed
                    #is produced.
                  
                #Creates a field outside of the injection circle
                #the kill zone for the particles
                elif np.sqrt((Xseed-col)**2+(Yseed-row)**2)>Radius:
                    lattice[row][col]=2                   
                    
    elif SeedChoice == 'Quadrants':
       
        #Initialize variables dependant on the Radius
        #Sets the x-coordinate of the Seed
        Xseed = Radius
        #Sets the y-coordinate of the seed
        Yseed = Radius
        #The size of the Lattice
        LatticeSize = Radius*2 

        #Creates the lattice as an empty array.   
        lattice=np.zeros((LatticeSize, LatticeSize))
        
        for row in range (0,LatticeSize):
            for col in range (0,LatticeSize):                

                if row==Yseed and col==Xseed: 
                    lattice[row][col]=1
                    
                    for count in range (-Radius, Xseed):
                        for count in range (-Radius, Yseed):
                           lattice[row-Radius+count][col] = 1
                           lattice[row][col-Radius+count] = 1
                           #After placing the
                
                #Next elif statement defines the kill zone for walkers
                elif np.sqrt((Xseed-col)**2+(Yseed-row)**2)>Radius:
                    lattice[row][col]=2
    
    #The colours for the back and line colour are inputted
    cmap = colors.ListedColormap([BackColour, LineColour, BackColour])

    # Initialize variables and Booleans
    randomWalkersCount = 0
    MissedWalkerCount = 0
    CheckClusterComplete = False
    AddedWalkerCount=0
    IntervalUsed=[]
    
    #While the cluster hasn't reached the edge of the lattice, the following
    #while statement can process
    while not CheckClusterComplete:
        #This releases a single walker, and increases the counter of amount of
        #walkers by one
        randomWalkersCount += 1
        random.seed()

        #Within the lattice, this line will produce a position for the walker
        #to be injected into.
        pos=RandomPos(Radius, Xseed, Yseed)

        #Initialises boolean variables, these are used to check if the edge
        #of the lattice has been found or if the position is suitable
        #for sticking
        FriendFound = False #not near other particle
        EdgeFound=False #not near the edge of the field


        # Single walker is sent out, stops if they have found something to 
        #stick on or exits at the boundary of the lattice.
        while not FriendFound and not EdgeFound:
            # Using function NeighbourCheck, it can see if there is 
            posNew,FriendFound, EdgeFound, ExitBoundary = NeighbourCheck(BiasAmount, BiasChoice,pos,LatticeSize,lattice)

            # Add to the cluster if near a friend
            if FriendFound:
                #Random number between 0 and 1 produces to compare with
                #probability chosen by user
                Compare = np.random.rand()
            
                if Compare <= Probability:
                    #If Compare is less or equal to the probability, then
                    #the walker can stick to a neighbouring walker.
                    #Add one to the Walker Count
                    
                    lattice[pos[1]][pos[0]] = 1
                    AddedWalkerCount+=1
                
                else:
                    #Otherwise, we just add one to the count of non-stick
                    #walkers.
                    MissedWalkerCount += 1
            
            #If no friend is found then the position is saved, which allows,
            #so this is just another step in the random walk of the walker.
            else:
                pos = posNew
        
        intervalSavePic=range(2,400000,500)
        
        if randomWalkersCount in intervalSavePic:
            print("Added ", randomWalkersCount, " random walkers.", " Cluster: ", AddedWalkerCount)
            
        if GIFChoice:
            if randomWalkersCount in intervalSavePic:
                
                IntervalUsed.append(randomWalkersCount) #append to the used count
                label=str(randomWalkersCount)
                plt.matshow(lattice, interpolation='nearest',cmap=cmap)
                plt.title("DLA Cluster, Radius of "+ str(Radius), fontsize=18)
                plt.xlabel("$x$", fontsize=12)
                plt.ylabel("$y$", fontsize=12)
                plt.savefig("images/cluster{}.png".format(label), dpi=200)
                plt.close()

        #If the max amount of walkers has been reached then the 
        #CheckClusterComplete becomes true and this
        #process is finished.
        if randomWalkersCount==MaxWalker:

            CheckClusterComplete = True

        

        #If it has found a particle to stick with and the edge of the lattice
        #has been found, then CheckClusterComplete becomes true and the 
        #process is finished.
        if FriendFound and ExitBoundary:
            CheckClusterComplete = True
    
    #Creates a figure that shows the lattice, using the colours inputted above
    plt.matshow(lattice, interpolation='nearest',cmap=cmap)
    plt.title("DLA Cluster, Radius of "+ str(Radius), fontsize=18)
    plt.xlabel("$x$", fontsize=12)
    plt.ylabel("$y$", fontsize=12)
    plt.savefig("images/cluster.png", dpi=200)
    plt.close()

    print(IntervalUsed)

    #If the user chose to have a GIF, then the following is ran:
    if GIFChoice:
        
        #We use the imageio module to get a 'writer' this can be used to 
        #append to the 'movie' file all the images that were produced in the
        #above processes.  
        with imageio.get_writer('images/movie.gif', mode='I') as writer:
           
            for i in IntervalUsed:
                
                #This is what the file name will be called
                filename="images/cluster"+str(i)+".png"
    
                image = imageio.imread(filename)
                
                #This appends the recently created file to the movie file
                writer.append_data(image)
                #This line deletes the file after it has been appended to the 
                #movie file
                os.remove(filename)
            
            image = imageio.imread("images/cluster.png")
            writer.append_data(image)
            
    return AddedWalkerCount, lattice


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