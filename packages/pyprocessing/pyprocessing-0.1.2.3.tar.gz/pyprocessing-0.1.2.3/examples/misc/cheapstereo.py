"""
An example on how to display a simple scene on some computers which 
provide a cheap stereo scheme whereby an extended desktop is mapped onto
two projectors which then display the two halves of the logical screen
onto the same physical screen. Two polarizing filters set to a 90 degree
angle from each other are mounted in front of the projector lenses. Using
viewing glasses with matching polarizing filters for each eye allows
the proper image separation. 

The present program only works on such systems when the window is resized
to occupy the whole desktop (so that the two cubes are mapped each to one half
of the desktop)
"""

from pyprocessing import *

def setup():
  """Initialization and setup."""
  # window setup
  size(200, 100, resizable=True)
  # Illumination setup
  lights()
  # A global rotation angle
  global angle
  angle = 0.0
  
def scene():
  """Draws a simple scene."""
  global angle
  angle += 0.1
  glPushMatrix ()
  glRotatef (angle, 0, 1, 0)
  box(45)
  glPopMatrix()
  
def draw():
  """Display callback."""
  # Projection setup
  glMatrixMode (GL_PROJECTION)
  glLoadIdentity()
  gluPerspective (60,width*0.5/height, 1, 200)
  # clear screen
  background (200)
  # First camera
  glViewport (0,0,width/2,height)
  glMatrixMode (GL_MODELVIEW)
  glLoadIdentity()
  gluLookAt (-2, 10, 100, 0, 0, 0, 0, 1, 0)
  scene()
  # Second camera  
  glViewport (width/2,0,width/2,height)
  glMatrixMode (GL_MODELVIEW)
  glLoadIdentity()
  gluLookAt (2, 10, 100, 0, 0, 0, 0, 1, 0)
  scene()
  
run()
