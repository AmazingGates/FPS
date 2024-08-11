# This is where we will have our main.run() code, which will initialize and run our program

import streamlit as st
import pygame as pg 
import sys
from settings import * # This is how we import our settings.py file to our main.py file
from map import * # This is how we import our map.py file to our main.py file. 
from player import * # This is how we import our player.py file to our main.py file
from raycasting import * # This is how we import our raycasting.py file to our main.py file
# This we will give access to textures
from object_renderer import * # This is how we import our object_renderer to our main.py file
from sprite_object import * # This is how we import our sprite_object to our main.py file
from object_handler import * # This is how we import our object_handler to our main.py file
from weapon import * # This is how we import our weapon file to our main.py file
from sound import * # This is how we import our sound file to our main.py file
from pathfinding import * # This is how we import our pathfinding file to our main.py file

st.header("Welcome To Alia's War Maze")


class Game:
    def __init__(self): # This is how we initialize our constructor method
        pg.init() # This is where we initialize the pygame modules
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES) # This is where we create a screen to display our (RES)
        self.clock = pg.time.Clock() # This will render the set resolution in an instance of the clock 
        #class for frame rate
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game() # This is where we will make a call to our new_game method from our main applications constructor

    def new_game(self): 
        self.map = Map(self) # This is where we will create an instance of our map class in the new_game method
        self.player = Player(self) # This is where we will create an instance of our map class in the new_game method
        # We will need to call 2 methods. The first in our update and the second in our draw
        self.object_renderer = ObjectRenderer(self) # This is where we create an instance of the class of the same name
        self.raycasting = RayCasting(self) # This is how we create an instance of our raycasting class
        #self.static_sprite = SpriteObject(self) # This is where we create an instance of our sprite_object class
        #self.animated_sprite = AnimatedSprite(self)# This is how we create an instance of our animated class
        self.object_handler = ObjectHandler(self) # This is where we create an instance of our Object Handler class
        self.weapon = Weapon(self) # This is where we create an instance of our Weapon class
        self.sound = Sound(self) # This is where we create an instance of our Sound class
        self.pathfinding = Pathfinding(self) # This is where we create an instance of our Pathfinding class
    
    # We will also access the delta time in our update method through an instance of the clock class which
    #was created to set the frame rate
    def update(self): # This is how we will update our screen display information about the current 
        self.player.update()
        self.raycasting.update() # This is how we call our raycasting method update
        self.object_handler.update() # This is how we call our object_handler method
        self.weapon.update() # This is how we call our weapon method
        #self.static_sprite.update() # This is where we will call our static_sprite method
        #self.animated_sprite.update() # This is where we call animated update method
        pg.display.flip()      
        self.delta_time = self.clock.tick(FPS) # This is where we accessed our delta time feature
        pg.display.set_caption(f"{self.clock.get_fps() :.1f}") #number of frames per second in the window caption

    def draw(self): # In the draw method, at each iteration, we will paint our screen black
        #self.screen.fill("black") # It is no longer necessary to fill the screen black because we have a sky image
        self.object_renderer.draw() # This is where we call our draw method for the object renderer
        self.weapon.draw() # This is where we will call our draw method for the weapon
        #self.map.draw() # This is where we will make a call to draw our map from our draw method
        #self.player.draw() # This is where we will make a call to draw our player from our draw method

    def check_events(self): # This is our method for checking events. Here we will check
        self.global_trigger = False
        for event in pg.event.get(): #the events for closing the working window and for pressing the escape key,
                                     #and if such events occur, we will correctly exit the application
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event) # This is where we will trace the actual event of our shot being fire
                # This method will also be called from our main loop
                                     
        

    def run(self): # In this run method will be located our main loop of the game,
        while True: #from this loop we will call the update, draw, and check_events methods
            self.check_events()
            self.update()
            self.draw()


# This is where we create an instance of our game and call the run method
if __name__=="__main__":
    game = Game() # Game instance
    game.run() # run method
         
