import pygame as pg
from settings import *

class ObjectRenderer: # This is our ObjectRenderer class that will render all objects in the game 
    def __init__(self, game): # We will take the game instance and rendering screen as attributes of this class
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures() # Here we will access textures for walls through the wall
        #textures attribute. Here we will call the texture loading methd
        self.sky_image = self.get_texture("Alia 12.png", (WIDTH, HALF_HEIGHT)) # The appearance of our sky will depend
        #on the movement of the mouse. 
        self.sky_offset = 0 # This is how we define initial offset for it to equal zero
        self.blood_screen = self.get_texture("Resources/Textures/Blood Screen.jpg", RES)
        self.digit_size = 10
        self.digit_images = [self.get_texture(f"Resources/Textures/digits/{i}.jpg",[self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))

    def draw(self): # We call our render_game_objects method through our main draw method 
        # This is where we call our draw_background method
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()

    def draw_player_health(self):
         health = str(self.game.player.health)
         for i, char in enumerate(health):
              self.screen.blit(self.digits[char], (i * self.digit_size, 0))
         self.screen.blit(self.digits["10"], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
         self.screen.blit(self.blood_screen, (0, 0))

    # This is where we will write the draw background method
    def draw_background(self):
         self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH # Here we will calculate the 
         #offset depending on the relative mouse movement value for the player instance
         self.screen.blit(self.sky_image, (-self.sky_offset, 0)) # Using the blit method, we will place two sky textures
         #taking into account the calculated offset value
         self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
         # And it remains to draw the floor in the form of a rectangle of the assigned color
         pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))
            
    def render_game_objects(self): # Here we use a separate method through an instance of the game class
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True) # This 
        #will sort our list by the first element in tuples in these elements we just have the values of the distances
        #from the player to the walls
        for depth, image, pos in list_objects: # Here we will get access to the list of objects for rendering 
            #iterate over this list and draw the resulting texture collumns on the render screen
                self.screen.blit(image, pos)


    # For convenience we will create a static method for which the path to the texture and its resolution are specified
    # This method loads the texture from the specified path and returns a scaled image
    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    # Here we can write a method for loading textures
    # It will return a dictionary in which the texture number is the key and the texture itself is the value
    # On our map the walls are marked with numbers that indicate exactly which texture to apply to the wall
    def load_wall_textures(self):
        return{
            1: self.get_texture("brick-wall-wall-texture-png-clipart_2942337.png"),
            2: self.get_texture("brick-wall-wall-texture-png-clipart_2942337.png"),
            3: self.get_texture("brick-wall-wall-texture-png-clipart_2942337.png"),
            4: self.get_texture("brick-wall-wall-texture-png-clipart_2942337.png"),
            5: self.get_texture("brick-wall-wall-texture-png-clipart_2942337.png")
        }
