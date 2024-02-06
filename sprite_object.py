import pygame as pg
from settings import *
import os # These imports are needed for further work with our animation class
from collections import deque # These imports are needed for further work with our animation class

class SpriteObject: # This is our Sprite Object class
    def __init__(self,game,path= "Zombie 3 Sprite.png", pos=(10.5, 3.5), scale=0.7, shift=0.27): # This is our constructor method.
        #The input of the constructor is the path where the sprite is located in its location on the map
        # In the attributes we take the instance of the game in the player coordinates of the sprite
        # We will also load the image of the sprite and create attributes for its width and half of its value
        self.game = game 
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        # Since we have introduced many new attributes, in order to avoid errors, we will define these attributes 
        #in the constructor of our class
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift # This will allow our sprite to shift and change accordingly when drawing

    # We will find the projection of the sprite in a separate method as in raycasting. We will calculate the height of 
    #its projection but here we must take into account that the sprite initially has a different aspect ratio, so
    #we will determine the image ratio and taking into account this coefficient, we will adjust the correct projection
    #size, then we scale the sprite to the calculated projection size, find its position on the screen, taking into
    #account that it does not disappear when its center is outside the edges of the screen
    # The most interesting thing is that we will add this sprite to the array of walls that is obtained from the 
    #results of raycasting
    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj 

        image = pg.transform.scale(self.image, (proj_width, proj_height))
        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT 
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift
        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))


    # First thing we must do is determmine the theta angle. Which is the angle our player is looking at the sprite
    # This is found using the arc tanget of the ratio of the difference between the player and sprite coordinates
    #and theta angle using the add and two function
    # Next we need to find the delta angle. This is the difference between the theta angle and the player's
    #direction angle
    # With the help of the delta we can find how many rays our sprite has shifted relative to the central ray
    def get_sprite(self): # This is where we will write our get sprite method
        dx = self.x - self.player.x # This is where we find the difference between these coordinates
        dy = self.y - self.player.y 
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle # This is how we find the delta angle. But if we do more complex work
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau
        #we need to understand that if the condition shown on the screen is met the delta angle must be increased 
        #by 2p (tau = 2p)
            
        # This is where we will caculate how many rays in the delta angle and as a result we find the x position
        #of the sprite on the screen by adding these rays to the central one and multiplying by the scale value
        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        # To calculate the size of our sprites projection we need to calculate the distance to the sprite 
        #and remove the fishbowl effect for it as we did in the raycasting, and to maintain the performance
        #we will do further calculations if the position of the sprite is inside the visible part of the screen
        #and not too close to our player
        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()
        


    def update(self): # This is our update method
        self.get_sprite() # We will call our get_sprite method from our update method

    





class AnimatedSprite(SpriteObject): # This is where we will create our AnimatedSprite class that will inherit from the
#SpriteObject class.e0f960a24b6862db.gif
    def __init__(self, game, path="Resources/Sprites/Final Fire.png", pos=(11.5, 3.5), 
                 scale=0.8, shift=0.15, animation_time=120):
    # Here, the constructor will receive all the same parameters, except for the new one, the animation time 
        super().__init__(game, path, pos, scale, shift) # First we call the super function to run the constructor
        #of the parent class
        self.animation_time = animation_time # We will also take the value ofthe animation time into the attributes
        self.path = path.rsplit("/", 1)[0] # This is how we get the path to the folder with our sprites
        self.images = self.get_images(self.path) # We will load them using the get images method
        self.animation_time_prev = pg.time.get_ticks() # This is where we define in the attributes, the value of 
        #the previous animation time in the trigger to perform the animation itself
        self.animation_trigger = False

    def update(self): # From this update method we will first call the update method of the parent class
        super().update()
        self.check_animation_time() # Then we will call our two methods 1
        self.animate(self.images) # 2

    def animate(self, images): # To perform the animation of the object itself we use this method
    # If the trigger has a true value, then we rotate the queue of images by one element and assign the
    #self image attribute to the first value from the queue
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]


    def check_animation_time(self): # This is where we will write our method for checking the animation time
        self.animation_trigger = False 
        time_now = pg.time.get_ticks() 
        if time_now - self.animation_time_prev > self.animation_time: # Here, we will compare two time values.
        # The Currrent and Previous. If the difference is greater than the animation time, then we assign the true
        #value to the animation trigger
            self.animation_time_prev = time_now
            self.animation_trigger = True


    def get_images(self, path): # This is where we store all of our images, in the instance of the deque class
        images = deque()
        for file_name in os.listdir(path): # Using the os module, we will get access to the names of all files
            #in the folder indicated by the path, download the images, and place them in the queue
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + "/" + file_name).convert_alpha()
                images.append(img)
        return images 
    
