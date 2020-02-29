# This class will handle the drawing of terrain tiles to the screen. (NOT ANY MORE)
# 
# Important questions:  
# - How will sub-sections of the greater world map be handled?  "Grid Windows"?
#   --Yes! The MapWindow class.
# - How will you draw terrain data within the city interface?
#   --Make a MapWindow.  Perhaps a sublclass to display city-related info.
# - What about minimaps?
# 
# I think eventually this class will be passed a reference to a "world", and then have method calls to determine
# how to react to it.  The data is universal, but the interactions are local.
#
# Or maybe this class will be that "world", and will lose its draw() methods.  
# Drawing will be done by "Window" classes.
#
# What I have ended up doing is creating 3 new classes to replace this: 
#   MapWindow, WorldMap, and GameState
# !!!!!!!!!!!!-->MapGrids is no longer necessary.<--!!!!!!!!!!!!!!!!!!!!!

from processing import *
import random
import tiles
import units


NEIGHBOR_OFFSETS = (
  (-1,-1),(-1,0),(-1,1),
  (0,-1),       (0,1),
  (1,-1),(1,0),(1,1),)
  
##### MapGrid Class ===============================================================
#The MapGrid holds an array of tiles and handles their interactions.
class MapGrid:
  """The Grid holds an array of Tiles and handles their interactions."""
  #-----------------------------------------------------------------------------
  def __init__(self,columns,rows,size=40,x_corner=20,y_corner=20):
    self.x_corner = x_corner
    self.y_corner = y_corner
    self.cols = columns
    self.rows = rows
    self.selected_tile = None
    self.size = size #The size of one tile (assume a square)
    self.tiles = self.makeMap(columns,rows) # Array of Tiles
    self.units = [] # List of units on map
    self.selected_unit = None # The unit currently selected
    self.cities = []
  #-----------------------------------------------------------------------------
  # Generates a map as a Tile array and returns it
  def makeMap(self,cols,rows):
    lands = ["grassland","forest","mountain"]
    lands_weight = [5,3,2]
    land_distro = []
    land_chance = 0.5
    # Apply weights to land types because py2 doesn't have random.choices()
    for i in range(len(lands)):
      for j in range(lands_weight[i]):
        land_distro.append(lands[i])
    waters = ['ocean']
    # Set up the new tile array
    new_map = []
    for r in range(rows):
      new_row = []
      for c in range(cols):
        # Choose terrain type for tile
        is_land = random.random()<land_chance
        if is_land:
          new_terrain = random.choice(land_distro)
        else:
          new_terrain = 'ocean'
        # Add tile to grid
        new_row.append(tiles.Tile(self,new_terrain,c,r))
      new_map.append(new_row)
    return new_map
  #-----------------------------------------------------------------------------
  def addUnit(self,unit_type,col,row):
    """Adds a new unit to the grid at specified location.  Assigns to proper lists."""
    target_coords = self.tiles[row][col]
    unit = units.Unit(target_coords,unit_type)
    target_coords.units.append(unit)
    self.units.append(unit)
  #-----------------------------------------------------------------------------
  def attemptLegalMoveTo(self,target_tile):
    '''If there is a selected unit, and a valid place to move it to, do so.'''
    if self.selected_unit:
      if self.selected_unit.canMoveTo(target_tile): # Check if tile can be moved to
        self.selected_unit.move(target_tile) # Move it there.
        self.selected_tile = target_tile # Bring selection along too
    pass
  #-----------------------------------------------------------------------------
  def hasMouse(self):
    return (0 < mouseX-self.x_corner < self.cols*self.size) and (0 < mouseY-self.y_corner < self.rows*self.size)
  #-----------------------------------------------------------------------------
  def inGrid(self,col,row):
    '''Returns whether a given column and row are actually within the Grid'''
    return 0<=row<self.rows and 0<=col<self.cols
  #-----------------------------------------------------------------------------
  def squareWithMouse(self):
    col = (mouseX-self.x_corner)//self.size
    row = (mouseY-self.y_corner)//self.size
    return (col,row)
  #-----------------------------------------------------------------------------
  def tileWithMouse(self):
    col = (mouseX-self.x_corner)//self.size
    row = (mouseY-self.y_corner)//self.size
    if self.inGrid(col,row):
      return self.tiles[row][col]
    else:
      return None
  #-----------------------------------------------------------------------------
  def getTile(self,coords):
    col,row = coords
    return self.tiles[row][col] if self.inGrid(col,row) else None
  #-----------------------------------------------------------------------------
  def tileNeighbors(self,col,row):
    neighbors = []
    for dr,dc in NEIGHBOR_OFFSETS:
      if self.inGrid(col+dc,row+dr):
        neighbors.append(self.tiles[row+dr][col+dc])
    return neighbors
    # #List comprehension version
    # return [self.tiles[row+dr][col+dc] for dr,dc in NEIGHBOR_OFFSETS if self.inGrid(col+dc,row+dr)]
      
  #-----------------------------------------------------------------------------
  def handleClick(self):
    mcol,mrow = self.squareWithMouse()
    if self.inGrid(mcol,mrow):
      #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      # Handle Left-Clicks 
      if mouseButton == LEFT:
        #Tile selection toggling
        if self.selected_tile == self.tileWithMouse():
          self.selected_tile = None
        else:
          self.selected_tile = self.tileWithMouse()
        #Select unit from tile
        if self.selected_tile and self.selected_tile.units: # If there are units
          self.selected_unit = self.selected_tile.units[-1] # Select last unit
        else:
          self.selected_unit = None
      #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      # Handle Right-Clicks
      elif mouseButton == RIGHT:
        # Attempt to move a unit.
        if self.selected_unit: # If a unit has been selected
          self.attemptLegalMoveTo(self.tileWithMouse())

      #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #-----------------------------------------------------------------------------
  def highlightTiles(self,tiles,color="#FFFFCC",alpha = 85, flash = True):
    strokeWeight(3)
    stroke(color,alpha)
    fill(color,alpha)
    for t in tiles:
      x,y,w,h = t.getRect()
      rect(x+0.1*w,y+0.1*h,0.8*w,0.8*h)
  #-----------------------------------------------------------------------------
  # Draws the whole Grid to the screen
  def draw(self):
    stroke(0)
    strokeWeight(1)
    for r, row in enumerate(self.tiles):
      for c, tile in enumerate(row):
        tile.draw() # Tile draws itself!
        
    # for unit in self.units: #Units instead will be drawn by tiles.
    #   unit.draw()
    
    #Draw selection rectangle
    if self.selected_tile:
      x,y = self.selected_tile.getCorner()
      noFill()
      stroke("#FFFFCC",170)
      strokeWeight(3)
      rect(x,y,self.size,self.size)
      
    #Highlight valid tiles that selected_unit can move to
    if self.selected_unit:
      self.highlightTiles(self.selected_unit.getLegalMoves())
  #-----------------------------------------------------------------------------
