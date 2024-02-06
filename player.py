# This is where we will create our player. 
# First, we must import our player settings from our settings.py file
# We will need to export our player.py file to our main.py file

# Delta Time - Delta Time is the amount of time that has passed since the last frame. We will
#access the delta time in our main.py file
from settings import * # This is how we import our settings.py file to access our players features
import pygame as pg
import math


class Player: # This is how we create our class of Player
    def __init__(self,game): # This is how we initialize our constructor method for our Player class and pass it an 
        #instance of the game. We will also get the x and y coordinates of our player in the angle of his direction
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False # This is where we create a boolean variable of the shot itself initially with a 
        #False value
        self.health = PLAYER_MAX_HEALTH

    def get_damage(self, damage):
        self.health = damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()

    def single_fire_event(self,event): # In this single fire event method we listen for the event when the player
        #presses the left mouse button. And in the event that the value of shot is false, we assign it a true value
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.Weapon.play()
                self.shot = True
                self.game.weapon.reloading = True 


    def movement(self): # This is where we will define our movement method. We will use the trigonometric
        #functions of sine and cosine to calculate the increments dx and dy by which our player's coordinates 
        #need to be changed. We can use this method for all of our keys
        # In our movement method we can calculate the sine and cosine values from our players direction angle
        # Then set dx and dy to be zero
        # Important Point *** If we want our players movement speed to be independent of the frame rate,
        #then we need to get the Delta Time value for each frame
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        

        # This is how we obtain information about the keys being pressed and according to the above theory
        #calculate the increments dx and dy
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        #self.x += dx # We will no longer use these use these coordinates, instead we will use them in our
        #self.y += dy #in our self.check_wall_collision(dx,dy) method
            
         # This is where we will call our method instead of changing our players coordinates
        self.check_wall_collision(dx, dy)


        # This is how we apply the received increments to the corresponding coordinates of the player and it remains
        #to implement the control of the players direction. For now we will do this for pressing the Left and Right
        #keys while the value should remain within 2*pi
        # tau = 2*pi
        
        # We disabled these keys because we implemented a new mouse_movement method
        #if keys[pg.K_LEFT]:
            #self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        #if keys[pg.K_RIGHT]:
            #self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau


    # This is where we are going to write a check method that will check for collisions against the wall
    def check_wall(self,x,y):
        return (x,y) not in self.game.map.world_map
    
    # Here is where we will use the check method we just created, in the collision check method using the the 
    #computed dx and dy increments in turn we check the new coordinates and only movement if there is no wall
    # We will use this method instead of changing the players coordinates
    def check_wall_collision(self, dx, dy):
        scale = PLAYERS_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    # We will write a test method drawing a player on a plane
    # We will draw his direction of movement as a line and our player himself will be in the form of a circle
    def draw(self):
        #pg.draw.line(self.game.screen, "yellow", (self.x * 100, self.y * 100),
                     #(self.x * 100 + WIDTH * math.cos(self.angle),
                      #self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, "green", (self.x * 100, self.y * 100), 15)

    # This is where we will put our mouse control method
    def mouse_control(self):
        mx, my = pg.mouse.get_pos() # This will check if our x coordinates are within the bounds, if not then set the 
        #cursor to the middle of the screen, then we get the value of the relative mouse movement since the previous
        #frame and clamp this value and as a result we will change the angle of our players direction to the 
        #value rel taking into account the values of sensitivity and delta time
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time


    def update(self): # We will call our movement method through our update method
        self.movement() # This is how we will call our movement method through our update function
        self.mouse_control() # This is where we will make a call to mouse control method

    # For convenience, we will make 2 properties.
    # The first returns the player's coordinates
    # The second integer coordinates to know which tile of the map we are on
    @property
    def pos(self):
        return self.x, self.y
    
    @property
    def map_pos(self):
        return int(self.x), int(self.y)
