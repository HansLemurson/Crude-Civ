#########1#########2#########3#########4#########5#########6#########7#########8
from processing import *
import random
import terrains
import units
####################### Globals ################################################
NEIGHBOR_OFFSETS = (
  (-1,-1),(-1,0),(-1,1),
  (0,-1),       (0,1),
  (1,-1),(1,0),(1,1),)

GRASS = '#33CC00'
WATER = '#0066FF'
DIRT = '#654321'
FOREST = '#339966'
MOUNTAIN = '#778899'

####################### Classes ################################################

##### Tile Class ===============================================================
class Tile:
  terrain_colors = {"ocean":WATER,"land":DIRT,"grassland":GRASS,
      "forest":FOREST,"mountain":MOUNTAIN}
  #-----------------------------------------------------------------------------
  def __init__(self,grid,terrain_type,col,row):
    self.col = col
    self.row = row
    self.grid = grid
    self.terrain = terrains.getTerrain(terrain_type)
    self.color = self.terrain["color"]
    self.units = []
    self.city = None
  #-----------------------------------------------------------------------------
  def __str__(self):
    return "<{} @(c:{},r:{})>".format(self.terrain,self.col,self.row)
  #-----------------------------------------------------------------------------
  def __repr__(self):
    return str(self)
  #-----------------------------------------------------------------------------
  #-----------------------------------------------------------------------------
  def getCorner(self):
    size = self.grid.size
    x = self.col*size + self.grid.x_corner
    y = self.row*size + self.grid.y_corner
    return x,y
  #-----------------------------------------------------------------------------
  def getCenter(self):
    size = self.grid.size
    x = (self.col+0.5)*size + self.grid.x_corner
    y = (self.row+0.5)*size + self.grid.y_corner
    return x,y
  #-----------------------------------------------------------------------------
  def draw(self):
    '''Tile Draws itself and any contents.'''
    stroke(0,153)
    strokeWeight(1)
    fill(self.color)
    size = self.grid.size
    x,y = self.getCorner()
    rect(x,y,size,size)
    # Draw Cities
    if self.city:
      self.city.draw()
    # Draw Units
    if self.units:
      self.units[-1].draw() #Draws "Top" unit
      #Add indicator for multiple units
      if len(self.units)>1:
        textSize(0.6*size)
        text("+",x+0.2*size,y+0.2*size)
  #-----------------------------------------------------------------------------

##### Grid Class ===============================================================
#The Grid holds an array of tiles and handles their interactions.
class Grid:
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
        new_row.append(Tile(self,new_terrain,c,r))
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
    return self.tiles[row][col]
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
      stroke("#FFFFCC",200)
      strokeWeight(3)
      rect(x,y,self.size,self.size)
  #-----------------------------------------------------------------------------
###################### Objects #################################################

world = Grid(12,12)
world.addUnit("warrior",5,7)
world.addUnit("soldier",7,5)
world.addUnit("boat",1,2)


###################### Processing I/O ##########################################
#-----------------------------------------------------------------------------
def setup():
  size(520,520)
  world.draw()
#-----------------------------------------------------------------------------
def keyPressed():
  # Random-Walk over Land tiles
  if key == ' ':
    for unit in world.units:
      neighbors = world.tileNeighbors(unit.tile.col,unit.tile.row)
      land = [t for t in neighbors if t.terrain != "ocean"]
      target = random.choice(land)
      unit.move(target)
  world.draw()
#-----------------------------------------------------------------------------
def mouseClicked():
  world.handleClick()
  world.draw()
#-----------------------------------------------------------------------------
def draw():
  pass
#-----------------------------------------------------------------------------
run()
