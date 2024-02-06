# This is where we will create our Game World
# This will be a 2d array in which values will represent walls and false values will represent empty space
# Our map file must be imported to the main.py file

import pygame as pg

_ = False # This is how we set our Fasle value to a variable (_). This is how we set up the display layout of our world
mini_map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,2,2,2,2,_,_,_,3,3,3,_,_,1],
    [1,_,_,_,_,_,2,_,_,_,_,_,3,_,_,1],
    [1,_,_,_,_,_,2,_,_,_,_,_,3,_,_,1],
    [1,_,_,_,_,_,2,_,_,_,_,_,3,_,_,1],
    [1,_,_,2,2,2,2,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,4,_,_,_,5,_,_,_,_,_,_,_,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]


class Map: # This is where we create our constructor method and an instance of the game class as input to our
           #constructor. Our minimap and world map become attributes. 
    def __init__(self,game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()

    # The world_map will be obtained through a separate method in which we iterate over our array and write the
    #coordinates of elements with only numeric values to the dictionary
    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i,j)] = value

    
# This is where we write the code to display our map to the screen
# We will write a test method draw, iterating over our world map. We will draw each elemment of our map 
#as an unfilled square
    def draw(self):
        [pg.draw.rect(self.game.screen, "darkgray", (pos[0] * 100, pos[1] * 100, 100, 100), 2)
        for pos in self.world_map]