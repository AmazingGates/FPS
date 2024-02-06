# This is where we will be writing the engine of our game
# Ray Casting comes down to the fact that we need to cast a given number of rays in a certain field 
#of view of our player, and for each ray we need to determine the intersection point with the wall
# To do this we need to find the intersections with vertical and horizontal lines, thus, the ray will have the most
#optimal number of steps. And here we should consider intersections with vertical and horizontal lines as two
#separate cases. If we consider the intersection of the ray with the verticals, then we can see that the ray
#along the x-axis moves to a distance dx equal to the size of the tile we have it equal to 1. In this case
#the movement along the y-axis also goes in equal segments dy, but their value must be calculated
# In the case of horizontal lines the opposite is true, dy is equal to the size of the tile and dx needs to be 
#calculated. It is also important for us to determine the depth delta so that we can calculate the distance to
#the wall for each ray. So to go further, we'll set the settings for ray casting
import pygame as pg
import math
from settings import *

class RayCasting: # This is where we define our RayCasting class in the attributes of which
    def __init__(self, game): #we take an instance of our game and define the instance of our game and define
        self.game = game                  #the RayCast method which will be called from our update method
        self.ray_casting_result = [] # This is where we define the attributes for the results of raycasting 
        self.objects_to_render = [] # The Objects to be drawn
        self.textures = self.game.object_renderer.wall_textures # Here we define a short name for our wall

    def get_objects_to_render(self): # This will be our method to get objects to draw
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:

                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height)) # This is where scale the subsurface
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)#to the projection height, calculate the position of this column texture based on the ray
                #number and add it to the list of objects for rendering

                # We need the depth value the wall collumn texture and its position
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))


    def ray_cast(self): # This is where we calculate the angle for the first ray 
        self.ray_casting_result = []
       
        ox, oy = self.game.player.pos # We will also need the coordinates of our player on the map ox, oy
        x_map, y_map = self.game.player.map_pos # and the coordinates of his tile x-map y-map

        
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001 # We need to subtract half the value of the field of 
        #view from our player's angle and add a small value in in order to avoid the the division by zero error 
        #in further calculations

        texture_vert, texture_hor = 1, 1 # We added this line to avoid errors
        for ray in range(NUM_RAYS): # This is where we will write a loop on the number of rays with the help of 
            #which we calculate the angles for each ray
            sin_a = math.sin(ray_angle) # This is where we calculate the values of the sine and cosine of 
            #the current ray and proceed to the case of the intersection of the ray with verticals
            cos_a = math.cos(ray_angle)

            # Horizontals - For intersections with horizontal lines, we do similar detail work here 
            # First we calculate the depth and the coordinates for the first intersection
            # Then we also calculate the delta_depth and dx values used to cast the ray for this case
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor] # Here we will determine the number of the textures 
                    #of the walls into which the rays collided
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth


            # Verticals - By the value of the cosine of the ray angle it is necessary to determine the x-coordinates
            #of the intersection with the verticals expert. If the cosine is positive, then x_vert will be one more
            #than the x_map value. But witha negative cosine value, expert will not be equal to x_map. Since we need
            #to check the left tile so we subtract a small number from x_map
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, - 1) # Here we will determine the value
            #of the variable dx
            depth_vert = (x_vert - ox) / cos_a # By using trigonometric functions, we calculate the value of the distance
            #of the first intersection with the depth vert and the value of the y coordinate y_vert
            y_vert = oy + depth_vert * sin_a
            # We will use trigonometry to detrermine the delta_depth value and the dy value
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            # We will cast the ray in a cycle by the number of steps equal to the value of the maximum depth here
            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert) # This is where we determine the tile based on the x_vert and y_vert values
                # This is where we check that we did not stumble upon a wall. If this happened, then we break the cycle, if
                #not, then we cast the ray further using the dx dy values and calculate the total value of the ray depth
                if tile_vert in self.game.map.world_map: # Here we will determine the number of the textures 
                    texture_vert = self.game.map.world_map[tile_vert] #of the walls into which the rays collided
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # This is where we will determine the depth we need
            # Based on the calculated depths of the rays, we find the actual texture number
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert) # Here we calculate the correct texture offset in the
                #way that was annouced above


            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor


            # This is how we remove the fishbowl effect
            # To do this, we multiply the depth value by the cosine of the angle which we get by subtracting
            #the value of the ray angle from the angle of the player's direction
            depth *= math.cos(self.game.player.angle - ray_angle)

            # Also, for debugging purposes, we will draw the entire result of raycasting
            #pg.draw.line(self.game.screen, "yellow", (100 * ox, 100 * oy),
                         #(100 * ox + 100 * depth * cos_a, 100 * oy + 100 * depth * sin_a), 2)
                
            # This is where calculate the projection height. We must also take into account the addition 
            #of a tiny number to the depth in order to avoid the division by zero error
            proj_height = SCREEN_DIST / (depth + 0.0001)


            # This is where we will draw our walls using rectangles
            # Taking into account hte scale we will draw a white rectangle and place it according to the number
            #of the ray along the x-axis and in the center of the screen taking into account the projection height 
            # We will also calculate the color in some power dependence on the value of the depth of the ray
            #color = [255 / (1 + depth ** 5 * 0.00002)] * 3
            #pg.draw.rect(self.game.screen, color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE,
                                                     #proj_height))
            # This piece of code became unnecessary so we commented it out

            # Ray Casting Results
            self.ray_casting_result.append((depth, proj_height, texture, offset))
            

            ray_angle += DELTA_ANGLE
    def update(self): 
        self.ray_cast() 
        self.get_objects_to_render() # This is where we will call our object renderer method                                   renederer