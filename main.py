#########1#########2#########3#########4#########5#########6#########7#########8
from processing import *
import random
# import mapgrids
import worldmaps
import mapwindows
import gamestates

# import units
# import tiles
####################### Globals ################################################
# NEIGHBOR_OFFSETS = (
#   (-1,-1),(-1,0),(-1,1),
#   (0,-1),       (0,1),
#   (1,-1),(1,0),(1,1),)

####################### Classes ################################################

# Classes successfully transferred to their own files.
# Look up:
# mapgrids.py <-- Has been deprecated, split into MapWindow, WorldMap, and GameState
# tiles.py
# terrains.py
# units.py

#

###################### Objects #################################################


world = worldmaps.WorldMap(12,12)
game = gamestates.GameState(world)
game.addUnitAt("warrior",5,7)
game.addUnitAt("soldier",7,5)
game.addUnitAt("cavalry",2,9)
game.addUnitAt("boat",1,2)

window1 = mapwindows.MapWindow(world,0,0,13,13)
window1.setPos(10,10)
# window2 = mapwindows.MapWindow(world,1,-1,5,5)
# window2.setPos(320,10)

UI = [window1]

###################### Processing I/O ##########################################
#-----------------------------------------------------------------------------
def setup():
  size(600,600)
  for thing in UI:
    thing.draw()
#-----------------------------------------------------------------------------
def keyPressed():
  # # Random-Walk over Land tiles (even for boats!)
  # if key == ' ':
  #   for unit in game.units:
  #     neighbors = world.tileNeighbors(unit.tile.col,unit.tile.row)
  #     land = [t for t in neighbors if t.terrain["type"] != "ocean"]
  #     if land:  
  #       target = random.choice(land)
  #       unit.move(target)
  # for thing in UI:
  #   thing.draw()
  pass
#-----------------------------------------------------------------------------
def mouseClicked():
  for thing in UI:
    thing.handleClick()
  for thing in UI:
    thing.draw()
#-----------------------------------------------------------------------------
def draw():
  pass
#-----------------------------------------------------------------------------
run()

################################################################################
# DESIGN PLANS
# "Game" consists of "User Interface" and "Game State"
# 
# =User Interface will deterimine *what* gets shown on the screen at any given time.
# --Main View will be the Map Window, Information panel, and Menu buttons
#   --Map Windows will keep track of their own "selections".
#   --Info Panel will need to be passed references from Main Map Window.
# --City View will show the info for a chosen city
# --Empire View will show info about the empire as a whole
# 
# =Game State will hold what the game *is* at the moment, and control how the parts interact with each other.
# --"Turns" will control what happens when.
#   --Most things will happen just once per turn.
#   --Some things will be "refreshed" each turn.
# --"Nations" will have cities, units, technology, money, and treaties.
# --"World Map" will hold all the map tiles, along with their cities and units.
# ----Should this hold a "selected unit" and "selected tile"?
#     \-NO.  Let Map Windows have their own selections.  It's all UI stuff.
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
############################################################
