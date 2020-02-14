from processing import *
###############################
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


########################################
#This will hold the data for the different units.
#===============================================================================
class Unit:
  pass
  def __init__(self,tile,unit_type):
    self.data = getUnitData(unit_type)
    self.move_points = self.data["movement"]
    self.tile = tile
    self.is_selected = False
  #----------------------------------------------------------
  def move(self,new_tile):
    '''Moves the unit to another tile, and removes itself from previous tile.'''
    pass
    new_tile.units.append(self)
    self.tile.units.remove(self)
    self.tile = new_tile
  #----------------------------------------------------------  
  def canMoveTo(self,target_tile):
    neighbor_tiles = self.tile.grid.tileNeighbors(self.tile.col,self.tile.row)
    valid_tiles = [t for t in neighbor_tiles if target_tile.terrain['domain'] == self.data["domain"]]
    #Make sure to include checks later about domain, movement cost, and maybe tile ownership.
    if target_tile in valid_tiles:
      return True
    else:
      return False
  #----------------------------------------------------------
  def draw(self):
    '''Unit draws itself, and any relevant info.'''
    x,y = self.tile.getCenter()
    size = 0.8*self.tile.grid.size
    fill("#FEBAFE")
    ellipse(x,y,size,size)
    #print out name
    textAlign(CENTER,CENTER)
    textSize(0.4*size)
    fill(0)
    text(self.data["name"],x+1,y+0.4*size)
    fill("#FFFF00")
    text(self.data["name"],x,y+0.4*size)
  #----------------------------------------------------------
