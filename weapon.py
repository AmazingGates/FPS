# This is where we will create our weapons
# We will need to export this module to our main.py file

from sprite_object import *

# This is where we will create a weapons class that will inherit from the animated sprite class
class Weapon(AnimatedSprite):
    def __init__(self, game, path="C:/Users/alpha/Shottaz/Resources/Weapon/Gun 1.png", scale=3, animation_time=90):
    # This is where our constructor method for our Weapon class. This is where we will specify in the parameters only, 
    #the path, scale and time of the animation
    # For weapons, we don't need to calculate the projection size, so we can just scale all the sprites to the
    #specified scale value
    # We also need to calculate the position of the weapon given the scaled sprite size, so that the weapon
    #is centered on the screen
        super(). __init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False# This is where we will have our weapon attributes for reloading the number of sprite 
        #images in the frame
        self.num_images = len(self.images)
        self.frame_counter = 0 
        self.damage = 50 # We will also need to define the damage for the weapon

    def animate_shot(self):# This is where we will have our animated shot method here if the reloading value is true
        #we will assign a false value to the shot variable for the player instance
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)# Then we perform the standard frame by frame animation, but at the same time
                self.image = self.images[0] #we count the number of frames
                self.frame_counter += 1 
                if self.frame_counter == self.num_images: # If this number of frames is equal to the number 
                #of sprites then we return a false to the reloading variable and reset the counter
                    self.reloading = False
                    self.frame_counter = 0
                # Before calling this method, we need to make a call to the method for checking the animation runtime

    # This is where we will add the draw method to draw the weapon and write the update method
    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time() # This is where we will be calling our method to check the animation runtime
        self.animate_shot()
        