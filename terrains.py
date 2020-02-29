# THis will hold a list of pre-made terrain data templates from which terrain data can be generated.
# What if I make the dictionary the input for a terrain object?
# What if I make terrain-objects just take a name as their input, 
# then the object itself references the stored data in here to see what data it contains.


# '':'',


void = {
  'type':"void",
  'color': "#123456",
  'domain': 'water',
  'move_cost':1,
  'food':0,
  'resources':0,
  'trade':0,
  'irrigate':'farms',
  'mine':'mine',
  'road':1,
}

ocean = {
  'type':"ocean",
  'color': '#0066FF',
  'domain': 'water',
  'move_cost':1,
  'food':1,
  'resources':0,
  'trade':2,
  'irrigate':None,
  'mine':None,
  'road':None,
}

grassland = {
  'type':"grassland",
  'color': "#339966",
  'domain': 'land',
  'move_cost':1,
  'food':2,
  'resources':0,
  'trade':0,
  'irrigate':'farms',
  'mine':'Forest',
  'road':1,
}

forest = {
  'type':"forest",
  'color': "#339966",
  'domain': 'land',
  'move_cost':2,
  'food':1,
  'resources':2,
  'trade':0,
  'irrigate':'grassland',
  'mine':None,
  'road':1,
}

mountain = {
  'type':"mountain",
  'color': "#778899",
  'domain': 'land',
  'move_cost':3,
  'food':0,
  'resources':2,
  'trade':0,
  'irrigate': None,
  'mine':'mine',
  'road':1,
}

void = {
  'type':"void",
  'color': "#123456",
  'domain': 'land',
  'move_cost':1,
  'food':0,
  'resources':0,
  'trade':0,
  'irrigate':'farms',
  'mine':'mine',
  'road':1,
}

void = {
  'type':"void",
  'color': "#123456",
  'domain': 'land',
  'move_cost':1,
  'food':0,
  'resources':0,
  'trade':0,
  'irrigate':'farms',
  'mine':'mine',
  'road':1,
}

TERRAIN_TYPES = {'ocean':ocean, 'grassland':grassland, 'forest':forest, 'mountain':mountain}

def getTerrain(terrain_name):
  if terrain_name in TERRAIN_TYPES:
    return TERRAIN_TYPES[terrain_name]
  else:
    return void
    
