#This code adapted from code in Making Music with Computers: Creative Programming in Python-CRC Press (2014) by Andrew R. Brown & Bill Manaris
#Code must be run using the Jython Environment Music - downloadable at https://jythonmusic.me/

#Creates an instrument which produces circles of random size and color. The circles, when clicked, play a note whose pitch is determined by the circle's luminosity and whose volume is determined by the size of the circle.
#Using sliders, the user can control the range of colors and rage of size of circles produced, as well as the speed at which circles appear.


from gui import *
from random import *
from music import *
import time

delay = 500   # initial delay between successive circle/notes
r = 0
b = 0
g = 0
s = 10

 
##### create display on which to draw circles #####
d = Display("Circular Music",950,700)   
d.setColor( Color.BLACK )  # set background color to black


# define callback function for timer
def drawCircle():
   """Draws one random circle and plays the corresponding note."""
 
   global d                         # we will access the display
 
   x = randint(0, d.getWidth())     # x may be anywhere on display
   y = randint(0, d.getHeight())    # y may be anywhere on display
   radius = randint(5, s)          # random radius (5-40 pixels)
   
   red = randint(0+r, 155+r)          
   blue = randint(0, 155+b)           
   green = randint(0, 155+g)
   color = Color(red, green, blue)      
   c = Circle(x, y, radius, color, True)  # create filled circle
   d.add(c)    
   
 
   luminosity = (red + green + blue) / 3   # calculate brightness
   
   def playnote(x, y):
      # now, let's create note based on this circle
      pitch = mapScale(luminosity, 0, 255, C4, C6, MINOR_SCALE)  
       
      # the larger the circle, the louder the note
      dynamic = mapValue(radius, 5, 50, 20, 127) 
       
      # and play note (start immediately, hold for 5 secs)
      Play.noteOn(pitch, dynamic)
   
   def endnote(x, y):
      pitch = mapScale(luminosity, 0, 255, C4, C6, MINOR_SCALE)  
      time.sleep(0.1)
      Play.noteOff(pitch)
      
   
   c.onMouseEnter(playnote)
   c.onMouseExit(endnote)

# create timer for animation
t = Timer(delay, drawCircle)    # one circle per 'delay' milliseconds

def rSet(value):
   global r
   r = value
   
def bSet(value):
   global b
   b = value
   
def gSet(value):
   global g
   g = value
 
def sizeSet(value):
   global s
   s = value
   
 

# define callback function for slider
def timerSet(value):
   global t, d1, title   # we will access these variables
   t.setDelay(value)
   d1.setTitle(title + " (" + str(value) + " msec)")
 

def clearOnSpacebar(key): # for when a key is pressed
   global d
   # if they pressed space, clear display and stop the music
   if key == VK_SPACE:
      d.removeAll() # remove all shapes
      Play.allNotesOff() # stop all notes
      
   
##### create display with slider for user input #####
title = "Control"
xPosition = (d.getWidth() / 3)+650   # set initial position of display
yPosition = d.getHeight() -400
d1 = Display(title, 300, 250, xPosition, yPosition)

# create slider
s1 = Slider(HORIZONTAL, 10, delay*2, delay, timerSet)

s2 = Slider(VERTICAL, 0, 100, r, rSet)
   
s3 = Slider(VERTICAL, 0, 100, b, bSet)
   
s4 = Slider(VERTICAL, 0, 100, g, gSet)
   
s5 = Slider(VERTICAL, 5, 50, s, sizeSet)

d1.add(s1, 25, 10)
d1.add(s2, 25, 50)
d1.add(s3, 75, 50)
d1.add(s4, 125, 50)
d1.add(s4, 175, 50)
d1.add(s5, 225, 50)

d.onKeyDown(clearOnSpacebar)


      
 
t.start()