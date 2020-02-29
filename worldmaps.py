# This class will hold an array of Tiles, and the code to generate a new map.

import random
import tiles
import terrains

NEIGHBOR_OFFSETS = (
  (-1,-1),(-1,0),(-1,1),
  (0,-1),       (0,1),
  (1,-1),(1,0),(1,1),)

class WorldMap:
  #-----------------------------------------------------------------------------
  def __init__(self,columns,rows):
    self.game_state = None
    self.cols = columns
    self.rows = rows
    self.tiles = self.makeMap(columns,rows)
  #-----------------------------------------------------------------------------
  # Generates a map as a Tile array and returns it
  def makeMap(self,cols,rows):
    # Apply weights to land types because py2 doesn't have random.choices()
    lands = ["grassland"]*5+["forest"]*3+["mountain"]*2
    waters = ['ocean']

    land_chance = 0.5
    
    # Set up the new tile array
    new_map = []
    for r in range(rows):
      new_row = []
      for c in range(cols):
        # Choose terrain type for tile
        is_land = random.random()<land_chance
        if is_land:
          new_terrain = random.choice(lands)
        else:
          new_terrain = random.choice(waters)
        # Add tile to grid
        new_tile = tiles.Tile(self,new_terrain,c,r)
        new_row.append(new_tile)
      new_map.append(new_row)
    return new_map
  #-----------------------------------------------------------------------------
  def getTile(self,col,row):
    "Returns a tile reference if col and row are in the grid."
    return self.tiles[row][col] if self.inGrid(col,row) else None
  #-----------------------------------------------------------------------------
  def inGrid(self,col,row):
    '''Returns whether a given column and row are actually within the Grid'''
    return 0<=row<self.rows and 0<=col<self.cols
  #-----------------------------------------------------------------------------
  def getTileNeighbors(self,tile):
    col,row = tile.col,tile.row
    #List comprehension version
    return [self.tiles[row+dr][col+dc] for dr,dc in NEIGHBOR_OFFSETS if self.inGrid(col+dc,row+dr)]
    
    # #"normal python" version
    # neighbors = []
    # for dr,dc in NEIGHBOR_OFFSETS:
    #   if self.inGrid(col+dc,row+dr):
    #     neighbors.append(self.tiles[row+dr][col+dc])
    # return neighbors
  #-----------------------------------------------------------------------------
  #-----------------------------------------------------------------------------
