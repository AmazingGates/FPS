# This is where we will create our Non Playable Characters

from sprite_object import *
from random import randint, random, choice


class NPC(AnimatedSprite): # This is where we will ceate and define our NPC class. It will also inherit 
    #from our AnimatedSprite class.
    def __init__(self, game, path="Resources/NPC/Zombie 3 Sprite.png", pos=(10.5, 5.5),
                 scale=1, shift=0.38, animation_time=180): # This is our constructor method. This
        #is where we will specify the parameters already known to us and then don't forget to the super 
        #function
        super(). __init__(game, path, pos, scale, shift, animation_time)
        # First, using the get images methodwe will load all the sprites for animation from the folders 
        #voiced at the beginning.
        self.attack_images = self.get_images(self.path + "/Attack")
        self.death_images = self.get_images(self.path + "/Death")
        self.idle_images = self.get_images(self.path + "/Idle")
        self.pain_images = self.get_images(self.path + "/Pain")
        self.walk_images = self.get_images(self.path + "/Walk")

# Next we will define a number of parameters for the npc. We will include in them the attack distance
# It's movement speed, size, amount of health, damage dealt, hit accuracy and boolean parametrs
# Whether the npc is alive and in pain
        self.attack_dist = randint(3, 6)
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.ray_cast_value = False # This ray_cast is for one ray, between our player and the npc
        self.frame_counter = 0 # This is how we will create the npc death animation that only plays once
        self.player_search_trigger = False # This is where we will define the player search trigger in the
        #constructor of our class

# This is where we will write our update method to start the animation and get the projection of the current sprite
    def update(self): # This is our update method
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()
        #self.draw_ray_cast()
# These are the same check_wall and check_wall_collision methods we used for our player. In order for the collision
#checking method to work correctly, only the size of the enemy itself must be taken into acount since here the
#increments do not depend on the delta time.   
    def check_wall(self,x,y):
        return (x,y) not in self.game.map.world_map
    
    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

# This is where we will create and define our movement method. Let's make him move to the tile where our player is.
# Then we calculate the angle for the npc if we looked at the center of this tile. Knowing this angle, we can 
#calculate the increments for the x and y axis. To start the movement of the npc we apply to these increments the 
#same methods for determining the collision with thewalls that we used for the player
    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos

        #pg.draw.rect(self.game.screen, "blue", (100 * next_x, 100 * next_y, 100, 100))
        if next_pos not in self.game.object_handler.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed 
            self.check_wall_collision(dx, dy)

# This is where we will write our method for attacking
    def attack(self):
        if self.animation_trigger:
            self.game.sound.npc_shot.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)


# This is where we will create our npc death animation method. For this we will use the frame counter and 
#compare its value with the number of sprites for this type of animation. We will include this method in the 
#npc logic when it is no longer alive.
    def animate_death(self):
        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1


# This is where we will create a method to animate the pain. Let it happen within one animation intervals, and based
#on the call to the hit test method in the npc, we will call the animation or further use the idle behavior
    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

# This is where we will write our method that checks if our player fired a shot.
    def check_hit_in_npc(self):
        if self.ray_cast_value and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width: # This is
            #how we get the npc position on our screen to be in the center, taking into account its projection 
            #value in width, and in this case we stop the bullet and set the pain variable to a true value
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage # This is how we add damage to our npc
                self.check_health()


# This is where we will create a method to check npc health. In the case where the npc health ends, the npc
#is no longer alive and we can play the sound of his death
    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.sound.npc_death.play()

# This is where we will write the logic for our npc. This will be based on whether he is alive or not, so just turn
#on the animation od idle_images
    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc() # This is where we can get the raycasting value and
            #write it to a separate variable
            self.check_hit_in_npc()

            if self.pain:
                self.animate_pain()

            elif self.ray_cast_value: # Here we will turn on the movement animation in the case when there is a 
            #direct line of sight to the player and use the walk_images for our movement.
                self.player_search_trigger = True # This is where we will create a player search trigger, which will
                #take on a true value as soon as the enemy sees us
                if self.dist < self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement() # Here we will use our movement method for the npc


            elif self.player_search_trigger: # This is where we will program the npc to chase us even if he can't see us
                self.animate(self.walk_images)
                self.movement()

            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()

    
# This is where we will make sure that bullets can't pass through walls by making sure there is a line of sight
#between our player and the npc or not (Also use "self.ray_cast_value = False" in our NPC class).
# To do this we will need almost the entire code of the raycast function until the projection is calculated. We
#will copy it from the raycasting class
    @property
    def map_pos(self):
        return int(self.x), int(self.y)
# First we will need to check if the player is in the same tile with the enemy  
    def ray_cast_player_npc(self): # This is where we calculate the angle for the first ray 
        if self.game.player.map_pos == self.map_pos: # This is where we check if our player and npc are on the same tile
            return True
        
        # This is where we will enter variables for the distances to the player and to the walls for verticals
        #and horizontals 
        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0
       
        ox, oy = self.game.player.pos # We will also need the coordinates of our player on the map ox, oy
        x_map, y_map = self.game.player.map_pos # and the coordinates of his tile x-map y-map

        
        ray_angle = self.theta # The angle between the npc and the player is known to us. This is theta angle

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
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor # This is where we will raycast for one ray and if this ray hits a wall
                #or an npc then we will record these distances
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
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map: # Here we will determine the number of the textures 
                wall_dist_v = depth_vert # This is where we will raycast for one ray and if this ray hits a wall
                #or an npc then we will record these distances
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth 

        player_dist = max(player_dist_v, player_dist_h) # This is where we will find the maximum values
        #for these distances and based on this we can determine whether there is a direct line of sight
        #between our player and npc or not
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False
    
    # To make it clear how this method works, let's draw such a result of raycasting as an orange line.
    # Then we will run this drawing from our update method.
    def draw_ray_cast(self):
        pg.draw.circle(self.game.screen, "red", (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_player_npc():
            pg.draw.line(self.game.screen, "orange", (100 * self.game.player.x, 100 * self.game.player.y),
                         (100 * self.x, 100 * self.y), 2)