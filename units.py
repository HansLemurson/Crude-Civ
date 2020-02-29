from processing import *
###############################
# This section holds the data for the different unit types, which will be used within the Unit class.
UNIT_TYPES = {
  "default":{
    "name": "DEFAULT_UNIT",
    "attack":1,
    "defense":1,
    "movement":1,
    "domain":"land"
  },
  
  "soldier":{
    "name": "Soldier",
    "attack":1,
    "defense":1,
    "movement":1,
    "domain":"land"
  },
  "boat":{
    "name": "Boat",
    "attack":1,
    "defense":1,
    "movement":1,
    "domain":"water"
  },
  "cavalry":{
    "name": "Cavalry",
    "attack":3,
    "defense":2,
    "movement":2,
    "domain":"land"
  },
}

def getUnitData(unit_type):
  if unit_type in UNIT_TYPES:
    return UNIT_TYPES[unit_type]
  else:
    return UNIT_TYPES["default"]


################################################################################
#This class will hold the data for the different units, and the methods to do stuff.
#===============================================================================
class Unit:
  pass
  def __init__(self,tile,unit_type):
    self.data = getUnitData(unit_type)
    self.move_points = self.data["movement"]
    self.max_health = 3
    self.cur_health = self.max_health
    self.tile = tile
    self.is_selected = False
  #-----------------------------------------------------------------------------
  def getLegalMoves(self):
    #Make sure to include checks later about domain, movement cost, and maybe tile ownership.
    neighbor_tiles = self.tile.getNeighbors()
    valid_tiles = [t for t in neighbor_tiles if t.terrain['domain'] == self.data["domain"]]
    return valid_tiles
  #-----------------------------------------------------------------------------
  def canMoveTo(self,target_tile):
    if target_tile in self.getLegalMoves():
      return True # Additional checks can go in here
    else:
      return False
  #-----------------------------------------------------------------------------
  def move(self,new_tile):
    '''Moves the unit to another tile, and removes itself from previous tile.'''
    pass
    new_tile.units.append(self)
    self.tile.units.remove(self)
    self.tile = new_tile
  #-----------------------------------------------------------------------------
  def canAttackTile(self,target_tile):
    pass
  #-----------------------------------------------------------------------------
  def attackTile(self,target_tile):
    pass
  #-----------------------------------------------------------------------------
  def attackUnit(self,target_unit):
    pass
  #-----------------------------------------------------------------------------
  def attemptLegalMoveTo(self,target_tile):
    if self.canMoveTo(target_tile):
      self.move(target_tile)
  #-----------------------------------------------------------------------------
  # def draw(self):
  #   '''Unit draws itself, and any relevant info.'''
  #   x,y = self.tile.getCenter()
  #   size = 0.8*self.tile.grid.size
  #   fill("#FEBAFE")
  #   ellipse(x,y,size,size)
  #   #print out name
  #   textAlign(CENTER,CENTER)
  #   textSize(0.4*size)
  #   fill(0)
  #   text(self.data["name"],x+1,y+0.4*size)
  #   fill("#FFFF00")
  #   text(self.data["name"],x,y+0.4*size)
  #-----------------------------------------------------------------------------
  def drawAt(self,x,y,w,h):
    # Get center coordinates
    xc,yc = x+0.5*w, y+0.5*h
    
    # Draw player color
    fill("#ABCDEF")
    ellipse(xc,yc,0.8*w,0.8*h)
    
    # Draw Unit name
    textAlign(CENTER,CENTER)
    textSize(0.3*w)
    # Draw back-shadow for text
    fill(0) 
    text(self.data["name"],xc+1,yc+(0.4*h))
    # Draw text fore-color
    fill("#FFFF00")
    text(self.data["name"],xc,yc+(0.4*h))
  #-----------------------------------------------------------------------------
  #-----------------------------------------------------------------------------
