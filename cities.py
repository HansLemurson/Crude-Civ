# This file will contain the code for how cities should operate.
# Cities will have multiple "resource boxes", population, happiness, and terrain.
#
# 
# Citizens let a city "work" terrain tiles, gathering their yields.
# Food goes to the Granary.  When full, a new citizen is added.
# Resources go to the current Project, and once that box is full the Project is completed.
# Trade is split into Gold, Science, and Luxuries.
# Gold and Science are sent to the National pool, luxuries add happiness.
#
# Cities will need to hold a list of Buildings within them.
# Those buildings will give bonuses to their production (or other effects).
# This is gonna get pretty complicated...
# I wonder how I'm going to display all this information.
