# This file will store our main game settings
# We must export our settings.py file to our main.py file
# We must export our player settings to our player.py file
# This is also where we will set the settings for our ray casting

import math

RES = WIDTH, HEIGHT = 1600, 900 # This will set the screen resolution of our width and height
HALF_WIDTH = WIDTH // 2 # This is how we calculate half the resoultion value for the width of our screen
HALF_HEIGHT = HEIGHT // 2 # This is how we calculate half the resoultion value for the width of our screen
FPS = 0 # This will set our frames per second

# This is where we will define our players settings
PLAYER_POS = 1.5, 5 # This is where we will define our players position on our map
PLAYER_ANGLE = 0 # This is where we define our players angle and direction
PLAYER_SPEED = 0.004 # This is how we set our players speed of movement
PLAYER_ROT_SPEED = 0.002 # This is how we set our players rotational speed
PLAYERS_SIZE_SCALE = 60
PLAYER_MAX_HEALTH = 100

MOUSE_SENSITIVITY = 0.0003 # This will set our mouses sensitivity
MOUSE_MAX_REL = 40 # This defines our maximum relative movement  in the left and right border of the screen
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

# This is where we will define the color for the floor in the settings file
# Then we can add the loaded sky
FLOOR_COLOR = (30, 30, 30) 

FOV = math.pi / 3 # This is where we define the field of view for our player
HALF_FOV = FOV / 2# The number of rays for the whole game 
NUM_RAYS = WIDTH // 2 # it is enough to take half of the resolution width value
HALF_NUM_RAYS = NUM_RAYS // 2 # Based on the number of rays we will define the angle between the rays delta angle
DELTA_ANGLE = FOV / NUM_RAYS 
MAX_DEPTH = 20 #and define the maximum depth

# We will use a tangent function to get the ratio of half the resolution width to the tangent of half the value
#of our players field of veiw
SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV) # This is where we calculate the correct distance for the 
                                              #screen location 

# This is where we determine the scaling factor since the number of rays we have is less than the screen
#resolution in width. This is odne specifically to maintain better performance
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 256 # This is where we define the size for our textures in the game
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2 # This is how we calculate half of it's value