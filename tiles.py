################################################################################
# Tiles are a data class that hold the items that exist on the map. (so why do they draw?)
# They hold:
#   -Terrain Data
#   -Terrain Improvements
#   -Units
#   -Cities
#   -Ownership?


from processing import *
import terrains
import units

##### Tile Class ===============================================================
class Tile:
  # terrain_colors = {"ocean":WATER,"land":DIRT,"grassland":GRASS,"forest":FOREST,"mountain":MOUNTAIN}
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
    return "<{} @(c:{},r:{})>".format(self.terrain["type"],self.col,self.row)
  #-----------------------------------------------------------------------------
  def __repr__(self):
    return str(self)
  #-----------------------------------------------------------------------------
  def getNeighbors(self):
    # return self.grid.tileNeighbors(self.col,self.row) #The MapGrid way
    return self.grid.getTileNeighbors(self)
  #-----------------------------------------------------------------------------
  # def getCorner(self):
  #   size = self.grid.size
  #   x = self.col*size + self.grid.x_corner
  #   y = self.row*size + self.grid.y_corner
  #   return x,y
  # #-----------------------------------------------------------------------------
  # def getCenter(self):
  #   size = self.grid.size
  #   x = (self.col+0.5)*size + self.grid.x_corner
  #   y = (self.row+0.5)*size + self.grid.y_corner
  #   return x,y
  # #-----------------------------------------------------------------------------
  # def getRect(self):
  #   w,h = self.grid.size,self.grid.size
  #   x = self.col*w + self.grid.x_corner
  #   y = self.row*h + self.grid.y_corner
  #   return x,y,w,h
  # #-----------------------------------------------------------------------------
  # def draw(self):
  #   '''Tile Draws itself and any contents.'''
  #   stroke(0,153)
  #   strokeWeight(1)
  #   fill(self.color)
  #   size = self.grid.size
  #   x,y = self.getCorner()
  #   rect(x,y,size,size)
  #   # Draw Cities
  #   if self.city:
  #     self.city.draw()
  #   # Draw Units
  #   if self.units:
  #     self.units[-1].draw() #Draws "Top" unit
  #     #Add indicator for multiple units
  #     if len(self.units)>1:
  #       textSize(0.6*size)
  #       text("+",x+0.2*size,y+0.2*size)
  #-----------------------------------------------------------------------------
  def drawAt(self,x,y,w,h):
    '''Tile draws itself (and any contents) within a specified rectangle.'''
    #Draw Terrain
    stroke(0,153) # Black border, 60% alpha
    strokeWeight(1) # 1px line
    fill(self.terrain["color"]) # Terrain's color
    rect(x,y,w,h)
    
    # Draw Cities
    if self.city:
      self.city.drawAt()
      
    # Draw Units
    if self.units:
      self.units[-1].drawAt(x,y,w,h) #Draws "Top" unit
      #Add indicator for multiple units
      if len(self.units)>1:
        textSize(0.7*w)
        fill("#000000")
        text("+",(x+1)+(0.2*w),y+(1)+(0.2*h))
        fill("#FFFF00")
        textSize(0.6*w)
        text("+",x+(0.2*w),y+(0.2*h))
        
        
  #-----------------------------------------------------------------------------
