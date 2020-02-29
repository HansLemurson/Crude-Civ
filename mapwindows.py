#This class will create Map Windows that will show sub-sections of the world map on screen.
#If you ever want to  have worlds that exceed the normal display size, this is what you'll have to do.

# This will handle all the drawing and clicks that the MapGrid class used to (done!)
# Will also need new action to re-center it. (done!)
# This could also be used to draw the terrain screen in the city-view. (maybe extend class?)

# Ugh! This is going to require that the Tile class be completely changed.  
# -->Tiles can no longer "draw" themselves if they don't know what window they're in!<--
# Tile class now has "drawAt()" method that is passed the rectangle it will draw in.

from processing import *

class MapWindow:
  #-----------------------------------------------------------------------------
  def __init__(self,world,col_start,row_start,col_count,row_count, 
                  x_corner=10, y_corner=10, tile_width=40, tile_height=40):
    #What map do you draw?
    self.world = world
    #How much of it do you draw?
    self.col_start = col_start
    self.row_start = row_start
    self.col_count = col_count
    self.row_count = row_count
    self.col_end = col_start + col_count - 1
    self.row_end = row_start + row_count - 1
    # self.mapArea = # (Cache the sub-array)
    
    #Where do you draw it.
    self.x_corner = x_corner
    self.y_corner = y_corner
    self.tile_width = tile_width
    self.tile_height = tile_height
    self.window_width = tile_width*col_count
    self.window_height = tile_height*row_count
    
    #Is anything selected?
    self.selected_tile = None
    self.selected_unit = None
  #-----------------------------------------------------------------------------
  def setPos(self,x_corner,y_corner):
    self.x_corner = x_corner
    self.y_corner = y_corner
  #-----------------------------------------------------------------------------
  def setTileSize(self,tile_width,tile_height):
    self.tile_width = tile_width
    self.tile_height = tile_height
  #-----------------------------------------------------------------------------
  def setMapArea(self,col_start,row_start,col_count,row_count):
    """Set the sub-area of the map for the Window to display."""
    self.col_start = col_start
    self.row_start = row_start
    self.col_count = col_count
    self.row_count = row_count
    self.col_end = col_start + col_count - 1
    self.row_end = row_start + row_count - 1
    self.window_width = self.tile_width*col_count
    self.window_height = self.tile_height*row_count
    # self.mapArea = self.getMapArea()
  #-----------------------------------------------------------------------------
  def getMapArea(self):
    pass
  #-----------------------------------------------------------------------------
  def hasMouse(self):
    """Returns whether the mouse cursor is within the Window's area"""
    return (0 < mouseX-self.x_corner < self.window_width) and (0 < mouseY-self.y_corner < self.window_height)
  #-----------------------------------------------------------------------------
  def withinWindow(self,tile):
    col_in_window = self.col_start <= tile.col <= self.col_end
    row_in_window = self.row_start <= tile.row <= self.row_end
    return col_in_window and row_in_window
  #-----------------------------------------------------------------------------
  def atWindowEdge(self,tile):
    """Returns whether a given tile is at the edge of the window"""
    return (tile.col == self.col_start) or (tile.col == self.col_end) or (tile.row == self.row_start) or (tile.row == self.row_end)
  #-----------------------------------------------------------------------------
  def distanceToWindowEdge(self,tile):
    """Returns how many tiles away from window's edge a tile is."""
    col_distance = min(abs(tile.col-self.col_start), abs(tile.col-self.col_end))
    row_distance = min(abs(tile.row-self.row_start), abs(tile.row-self.row_end))
    return min(col_distance,row_distance)
  #-----------------------------------------------------------------------------
  def tileWithMouse(self):
    """Returns reference to the tile which the mouse is over."""
    window_col = (mouseX-self.x_corner)//self.tile_width
    window_row = (mouseY-self.y_corner)//self.tile_height
    
    world_col = window_col + self.col_start
    world_row = window_row + self.row_start
    
    if self.world.inGrid(world_col,world_row):
      return self.world.getTile(world_col,world_row)
      # return self.world.getTile((world_col,world_row)) # mapgrid way
    
  #-----------------------------------------------------------------------------
  def recenterOnTile(self,tile):
    """Re-centers the Map Window on the chosen tile, rounding to the upper left."""
    new_col_start = tile.col - self.col_count//2
    new_row_start = tile.row - self.row_count//2
    self.setMapArea(new_col_start,new_row_start,self.col_count,self.row_count)
  #-----------------------------------------------------------------------------
  def getRect(self,tile):
    """Gives the x,y,w,h for a tile to be drawn in this Window."""
    window_col = tile.col - self.col_start
    window_row = tile.row - self.row_start
    
    w,h = self.tile_width,self.tile_height
    
    x = window_col*w + self.x_corner
    y = window_row*h + self.y_corner
    
    return x,y,w,h
    # All in one line...
    # return ((tile.col-self.col_start)*self.tile_width+self.x_corner, (tile.row-self.row_start)*self.tile_height+self.y_corner, self.tile_width, self.tile_height)
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def handleClick(self):
    if self.hasMouse(): #Pay attention only to clicks within window.
      clicked_tile = self.tileWithMouse()
      if clicked_tile: #Make sure that a tile exists where clicked.
        if mouseButton == LEFT:
          self.leftClick(clicked_tile)
        if mouseButton == RIGHT:
          self.rightClick(clicked_tile)
  #-----------------------------------------------------------------------------
  def leftClick(self,clicked_tile):
    self.selected_tile = clicked_tile
    if self.selected_tile.units: #If the selected tile has any units
      self.selected_unit = self.selected_tile.units[-1] # Select the last one
    else:
      self.selected_unit = None
    self.recenterOnTile(clicked_tile)
  #-----------------------------------------------------------------------------
  def rightClick(self,clicked_tile):
    if self.selected_unit: #If a unit is selected
      self.selected_unit.attemptLegalMoveTo(clicked_tile)
      self.selected_tile = self.selected_unit.tile
    print self.distanceToWindowEdge(clicked_tile)
    if self.distanceToWindowEdge(clicked_tile) <= 2:
      self.recenterOnTile(clicked_tile)
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def drawTile(self,tile):
    # Would contain code to determine how to draw tiles from within this class.
    # Maybe makes sense for totally separating Data from UI.  Will get to it later.
    pass
  #-----------------------------------------------------------------------------
  def outlineTiles(self,tiles,color="#FFFFCC",alpha = 170, flash = False):
    """Takes a list of tiles and draws outlines around their rectangles."""
    stroke(color,alpha)
    strokeWeight(3)
    noFill()
    for t in tiles:
      if self.withinWindow(t): #Only draw stuff if it's inside the window.
        x,y,w,h = self.getRect(t)
        rect(x,y,w,h)
  #-----------------------------------------------------------------------------
  def highlightTiles(self,tiles,color="#FFFFCC",alpha = 85, flash = False):
    """Takes a list of tiles and draws a colored overlay inside them."""
    strokeWeight(3)
    stroke(color,alpha)
    fill(color,alpha)
    for t in tiles:
      if self.withinWindow(t): #Only draw stuff if it's inside the window.
        x,y,w,h = self.getRect(t)
        rect(x+0.1*w,y+0.1*h,0.8*w,0.8*h) #rectangle 10% in from the edges
  #-----------------------------------------------------------------------------
  def draw(self):
    # Set up background
    stroke(255)
    strokeWeight(1)
    fill(0)
    rect(self.x_corner-1,self.y_corner-1,self.window_width+2,self.window_height+2)
    # Draw tiles from chosen sub-section of the map
    for row in range(self.row_start,self.row_end+1):
      for col in range(self.col_start,self.col_end+1):
        tile = self.world.getTile(col,row) #This is the WorldMap way
        # tile = self.world.getTile((col,row)) #This is the MapGrid way
        if tile:
          tr = self.getRect(tile)
          tile.drawAt(*tr) 
    
    # Draw selection graphics.
    # For tiles
    if self.selected_tile: #If a tile is selected
      self.outlineTiles([self.selected_tile]) #Send it to the outlining function
    # For units
    if self.selected_unit:
      self.highlightTiles(self.selected_unit.getLegalMoves())
  #-----------------------------------------------------------------------------
