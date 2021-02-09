# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 17:26:53 2020

@author: User
"""

# =============================================================================
# =============================================================================
# # Welcome to the GUI coding and Runner for my 3rd Year Project.
# # I look forward to your feedback.
# =============================================================================
# =============================================================================

# =============================================================================
#   Imports modules and libraries, as well as the OS system so that
#   files can be read/write from/to and saved.
# =============================================================================

import matplotlib.pyplot as plt
import ctypes
import os
from matplotlib.widgets import Slider, Button, RadioButtons, TextBox

# =============================================================================
#   Imports the custom modules, found in the ZIP file
# =============================================================================

from DLA import Aggregator, FD

#Intialises Variables.

LineColourChoice= 'black'
BackColourChoice = 'white'
SeedChoice = 'Dot'
GIFChoice = True
BiasChoice = 'None'
Choice = 'Just Cluster Generation'

# =============================================================================
#   Toggle FUNCTION
   
#   The defined function toggle is triggered by pressing the 
#   button "Create Cluster."

# =============================================================================

def toggle(event):
    
    #The following sets the variables to the user set variables.
    Radius = int(s_r.val)
    Probability = s_p.val
    MaxWalker = int(txtw.text)
    BiasAmount = s_b.val
    
    #If the user just wants to create a cluster, without exploring the
    #fractional dimensionality of it, they can, using this code:
    if Choice == 'Just Cluster Generation':
            
        #The following closes the figure and passes the variables as 
        #parameters to the cluster generator.
        #Returns the mass (particles in cluster) and the cluster (lattice)..
        mass,lattice = Aggregator(SeedChoice, BiasAmount, BiasChoice, MaxWalker, Probability, Radius, GIFChoice, LineColourChoice, BackColourChoice)
        plt.close()
        #The user can choose whether or not to have a GIF of the cluster
        #creation. 
        #These if statements deal with the possibilites.
        
        if GIFChoice == True:
            
            #If the user has chosen for there to be a GIF, a message 
            #informing them that they can find the cluster GIF and image 
            #in the same file directory as this project.
            #Refer to the ReadMe for generic file path.
            
            ctypes.windll.user32.MessageBoxW(0, "Cluster Image and GIF of Aggregation Saved to File Directory", "Complete", 0)
            
            #These lines of code open both the image and the GIF
            #.\images\ is created in the Aggregator function
            
            os.startfile(".\images\cluster.png", 'open')
            os.startfile(".\images\movie.gif", 'open')
    
        
       
        #If the user does not want a GIF then this if statement is activated. 
        elif GIFChoice == False: 
            
            #Opens just the image file with a different messagebox.
            
            ctypes.windll.user32.MessageBoxW(0, "Cluster Image Saved to File Directory", "Complete", 0)
            
            os.startfile(".\images\cluster.png", 'open')
            
    #If the user would like to explore the Fractional Dimensionality then they
    #can using this code:
    elif Choice == 'Run Fractional Dimensionality':
           
        #Initialises the stopping condition.
        
        Break = 0
        
        
        #To get an accurate result from the process, we need the input to be 
        #greater than 20. The process actually starts from radius 10 up to the 
        #max radius, so the final radius is actually max Radius - 10.
        #The user is encouraged to input values greater than 20 for this
        #reason.
        if Radius > 20:
            
            while Break == 0:
                #Closes all Figures.
                plt.close()
                #Calls the FD function, imported from the DLA file.
                #Passes the parameters, same as the Aggregator function.
                FD(SeedChoice, BiasAmount, BiasChoice, MaxWalker, Probability, Radius, GIFChoice, LineColourChoice, BackColourChoice)            
                
                #Ends the while loop.
                Break = 1
            
                #Closes all Figures. 
                plt.close()
            
            if GIFChoice == True:       
                
                #If the user has chosen for there to be a GIF, a message 
                #informing them that they can find the cluster GIF and image 
                #in the same file directory as this project.
                #Refer to the ReadMe for generic file path.
                
               os.startfile(".\images\movie.gif", 'open')
               ctypes.windll.user32.MessageBoxW(0, "Log-log plot of Mass vs Radius, Cluster Image and GIF of Aggregation Saved to File Directory", "Complete", 0)
            
            elif GIFChoice == False: 
            
                ctypes.windll.user32.MessageBoxW(0, "Log-log plot of Mass vs Radius, Cluster Image Saved to File Directory.", "Complete", 0)        
           
            #Opens just the image file with a different messagebox.
            os.startfile(".\images\cluster.png", 'open')
            os.startfile(".\images\logRadiusMass.png", 'open')
        
        else:
            ctypes.windll.user32.MessageBoxW(0, "For Fractal Dimension process, please select a Radius greater than 20 for accurate results.", "Error", 0)

# =============================================================================
#   CheckGIF FUNCTION
   
#   The defined function CheckGif is triggered by pressing choosing one of the
#   radio buttons for "Creating GIF."

# =============================================================================

def CheckGIF(label):
    #Declares a global variable so that all functions can use the variable
    global GIFChoice
    
    #If statement dependant on user's radiobutton choice
    if label == 'Yes GIF':
        #Program recognises user's desire for a GIF of the aggregation
        GIFChoice = True
    
    elif label == 'No GIF':
        #Program recognises user's desire to not have a GIF of the aggregation
        GIFChoice = False


# =============================================================================
#   CheckLineColour FUNCTION

#   The defined function CheckLineColour is triggered by pressing choosing
#   one of the radio buttons for "Line Colour."

# =============================================================================

def CheckLineColour(label):
    #Declares a global variable so that all functions can use the variable
    #LineColourChoice
    global LineColourChoice
    LineColourChoice = label

# =============================================================================
#   CheckBackColour FUNCTION

#   The defined function CheckBackColour is triggered by pressing choosing
#   one of the radio buttons for "Back Colour."

# =============================================================================

def CheckBackColour(label):
    #Declares a global variable so that all functions can use the variable
    #BackColourChoice
    global BackColourChoice
    BackColourChoice = label
    
# =============================================================================
#   CheckSeedChoice FUNCTION

#   The defined function CheckSeedChoice is triggered by pressing choosing
#   one of the radio buttons for "Seed Choice."

# =============================================================================

def CheckSeedChoice(label):
    #Declares a global variable so that all functions can use the variable
    #SeedChoice
    global SeedChoice
    SeedChoice = label

# =============================================================================
#   CheckBiasChoice FUNCTION

#   The defined function CheckBiasChoice is triggered by pressing
#   choosing one of the radio buttons for "Bias Choice."
#   Value set by the slider, magnitude of bias is updated in 
#   Toggle Function, line 111

# =============================================================================

def CheckBiasChoice(label):
    #Declares a global variable so that all functions can use the variable
    #BiasChoice
    global BiasChoice
    BiasChoice = label


# =============================================================================
#   CheckChoice FUNCTION

#   The defined function CheckChoice is triggered selecting on of the
#   radiobuttons for 'Just Cluster Generation' or
#   'Run Fractional Dimensionality.'

# =============================================================================

def CheckChoice(label):
    global Choice
    Choice = label

# =============================================================================
#   CheckMaxWalkerText FUNCTION

#   The defined function CheckMaxWalkerText is triggered by leaving the
#   textbox for the Max Walker input

# =============================================================================

def CheckMaxWalkerText(event):
    #Gives two possibilities if it is a negative number or a non-number
    try:
        if int(txtw.text) <= 0:
            #If it is a non-positive number, then the user receive a
            #messagebox and the text box resets itself to the initial value.
            
            ctypes.windll.user32.MessageBoxW(0, "Reset to Initial Value (20000), refer to ReadMe", "Error", 0)  
            txtw.text = '20000'
            
    except ValueError:
        #If it is a non-number, then the user receive a
        #messagebox and the text box resets itself to the initial value.
        ctypes.windll.user32.MessageBoxW(0, "Reset to Initial Value (20000), refer to ReadMe", "Error", 0)  
        txtw.text = '20000'
# =============================================================================
#   GUI Control

#   The following code concerns creating the GUI that the user will use to input
#   and choose the various varibles

# =============================================================================

#Produces a figure that acts like an axis of 0 rows and 0 columns, 
#simply comprised of one unit that can be sub-divded

fig, ax = plt.subplots(nrows = 0, ncols = 0)


#This is the slider button for the Radius variable.
#axr is its position on the subplot, which it is relative to.
#The user can choose between 1 and 200, but can only step in units of 1,
#this prevents a non-integer radius and the initial value of 10 means that the user
#is encouraged to use appropriate variable magnitudes.

axr = plt.axes([0.12, 0.00, 0.55, 0.03])
s_r = Slider(axr, 'Radius', 1, 200, valinit=10, valstep = 1)

#This is the slider button for the Probability variable.
#axp is its position on the subplot, which it is relative to.
#The user can choose between 0 (0% chance) and 1 (100% chance)
#but can only step in units of 0.01, meaning all integer percentage values
# between 0% and 100% inclusive are represented.

axp = plt.axes([0.12, 0.05, 0.55, 0.03])
s_p = Slider(axp, 'Probability', 0, 1, valinit=1, valstep = 0.01)

#This is the slider button for the BiasAmount variable.
#axb is its position on the subplot, which it is relative to.
#The user can choose between -0.5 and +0.5, but can only step in units of 0.01,

axb = plt.axes([0.12, 0.10, 0.55, 0.03])
s_b = Slider(axb, 'Bias Amount', -0.5, 0.5, valinit=0.0, valstep = 0.01)

#This is the textbox for the MaxWalker variable.
#axw is its position on the subplot, which it is relative to.
#The user can choose between any non-negative value

axw = plt.axes([0.12, 0.15, 0.55, 0.03])
txtw = TextBox(axw, 'Max Walkers', initial = '20000')
txtw.on_submit(CheckMaxWalkerText)

#This is the Radiobutton for the GIFChoice variable.
#axGIF is its position on the subplot, which it is relative to.
#The user can choose between having a gif or not, with the initial choice
#being 'Yes GIF.'

axGIF = plt.axes([0.5,0.4,0.2,0.5])
GIF = RadioButtons(axGIF,('Yes GIF', 'No GIF'), active = 0, activecolor = 'green')
GIF.on_clicked(CheckGIF)

#This is the Radiobutton for the LineColour variable.
#axLineColour is its position on the subplot, which it is relative to.
#The user can choose between the listed colours, with the initial choice
#being 'black.'

axLineColour = plt.axes([0.2,0.4,0.30,0.5])
LineColour = RadioButtons(axLineColour,('black','white','gold', 'green', 'indigo','red','blue'), active = 0, activecolor = 'green')
LineColour.on_clicked(CheckLineColour)

#This is the Radiobutton for the BackColour variable.
#axBackColour is its position on the subplot, which it is relative to.
#The user can choose between the listed colours, with the initial choice
#being 'white.'

axBackColour = plt.axes([0.0,0.4,0.2,0.5])
BackColour = RadioButtons(axBackColour,('black','white','gold', 'green', 'indigo','red','blue'), active = 1, activecolor = 'green')
BackColour.on_clicked(CheckBackColour)

#This is the Radiobutton for the BiasDirection variable.
#axBiasDirection is its position on the subplot, which it is relative to.
#The user can choose between the have no bias or having a bias on the x-Axis,
#with the initial choice being 'None'

axBiasDirection = plt.axes([0.9,0.4,0.2,0.5])
BiasDirection  = RadioButtons(axBiasDirection, ('None', 'x-Axis'), active = 0, activecolor = 'green')
BiasDirection.on_clicked(CheckBiasChoice)

#This is the Radiobutton for the SeedChoice variable.
#axSeed is its position on the subplot, which it is relative to.
#The user can choose between the listed seed shape choice,
#with the initial choice being 'Dot'

axSeed = plt.axes([0.7,0.4,0.2,0.5])
Seed = RadioButtons(axSeed,('Dot', 'Line', 'Quadrants'), active = 0, activecolor = 'green')
Seed.on_clicked(CheckSeedChoice)

#This is the Button for the Toggle Function.
#axtoggle is its position on the subplot, which it is relative to.
#The user can start the procedure by clicking on the button.

axtoggle = plt.axes([0.12,0.3,0.55,0.06])
btoggle = Button(axtoggle, "Create Cluster", image = None, color = 'teal', hovercolor = 'green')
btoggle.on_clicked(toggle)

axChoice = plt.axes([0.75,0.0,0.5,0.5])
ChooseChoice = RadioButtons(axChoice, ('Just Cluster Generation','Run Fractional Dimensionality'))
ChooseChoice.on_clicked(CheckChoice)