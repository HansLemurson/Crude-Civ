from processing import *

########################################
#This will hold the data for the different units.

class Unit:
  pass
  def __init__(self,tile,type):
    self.type = type
    self.domain = "land"
    self.movement = 2
    self.move_points = self.movement
    self.tile = tile
    self.is_selected = False
  
  def move(self,new_tile):
    '''Moves the unit to another tile, and removes itself from previous tile.'''
    pass
    new_tile.units.append(self)
    self.tile.units.remove(self)
    self.tile = new_tile
    
  def canMoveTo(self,target_tile):
    neighbor_tiles = self.tile.grid.tileNeighbors(self.tile.col,self.tile.row)
    valid_tiles = [t for t in neighbor_tiles if target_tile.terrain['domain'] == self.domain]
    #Make sure to include checks later about domain, movement cost, and maybe tile ownership.
    if target_tile in valid_tiles:
      return True
    else:
      return False
  
  def draw(self):
    '''Unit draws itself, and any relevant info.'''
    x = self.tile.col * self.tile.grid.size + self.tile.grid.x_corner
    y = self.tile.row * self.tile.grid.size + self.tile.grid.y_corner
    size = self.tile.grid.size
    fill("#FEBAFE")
    ellipse(x+0.5*size,y+0.5*size,0.8*size,0.8*size)
