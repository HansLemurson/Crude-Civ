###################################################################
# This will keep track of all the data needed to run a game.
###################################################################
import units

class GameState:
  def __init__(self,world):
    self.world = world
    # self.nations = nations
    self.units = [] # These will be put under Nations later
    self.cities = [] # These will be put within Nations later
    self.turn = 0
    
  def addUnitAt(self,unit_type,col,row): #Make sure to update this for nations
    """Adds a new unit to the Game State at specified location.  Assigns to proper lists."""
    target_tile = self.world.getTile(col,row)
    unit = units.Unit(target_tile,unit_type)
    target_tile.units.append(unit)
    self.units.append(unit)
