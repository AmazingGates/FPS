# This is where we create a class where all objects of our game will be processed
# We will have to import this module to our main.py file
from sprite_object import *
from npc import *

class ObjectHandler: # This is our Object Handler class
    def __init__(self, game): # This is the constructor method for our Object Handler class
        self.game = game # These are our attributes
        self.sprite_list = [] # These are our attributes
        self.npc_list = [] # We will use this ObjectHandler class to display our npc
        self.npc_sprite_path = "Resources/NPC" # Here we will create a separate list for npc and write the path
        #to the corresponding folder
        self.static_sprite_path = "Resources/Sprites/static_sprites/" # This is how we specify the paths to the
        #corresponding folders with sprites
        self.anim_sprite_path = "Resources/Sprites/animated_sprites/" # This is how we specify the paths to the
        add_sprite = self.add_sprite
        add_npc = self.add_npc # This is where we will create an instance of our npc class to add it
        self.npc_positions = {} # This is where we created a set to store our tiles

        # This will act as a map where we will add our sprites to our game
        add_sprite(SpriteObject(game))
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5))) # This is how we arrange sprites in our game
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        

        # This is where we will add our npc class
        add_npc(NPC(game))
        add_npc(NPC(game, pos=(11.5, 4.5)))
        add_npc(NPC(game, pos=(7.5, 3.5)))
        add_npc(NPC(game, pos=(3.5, 5.5)))
        add_npc(NPC(game, pos=(3.5, 7.5)))
        add_npc(NPC(game, pos=(4.5, 1.5)))
        add_npc(NPC(game, pos=(5.5, 8.5)))
        add_npc(NPC(game, pos=(7.5, 6.5)))
        add_npc(NPC(game, pos=(6.5, 1.5)))
        add_npc(NPC(game, pos=(8.5, 4.5)))
        add_npc(NPC(game, pos=(9.5, 8.5)))
        add_npc(NPC(game, pos=(1.5, 4.5)))
        add_npc(NPC(game, pos=(2.5, 2.5)))
        add_npc(NPC(game, pos=(7.5, 3.5)))
        add_npc(NPC(game, pos=(6.5, 1.5)))
        add_npc(NPC(game, pos=(11.5, 1.5)))
        add_npc(NPC(game, pos=(1.5, 5.5)))
        add_npc(NPC(game, pos=(3.5, 1.5)))
        add_npc(NPC(game, pos=(5.5, 7.5)))
        add_npc(NPC(game, pos=(1.5, 6.5)))
        add_npc(NPC(game, pos=(2.5, 5.5)))


    # This is where we will make an update method where we will call our method of the same name for all sprites in
    #this list
    # We will also write an update to add all enemies to this list 
    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

    def add_npc(self, npc): # For convenience we will make a method for adding npc to this list
        self.npc_list.append(npc)


    def add_sprite(self, sprite): # This is how we create a method for adding sprites
        self.sprite_list.append(sprite)