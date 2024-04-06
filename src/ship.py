import pygame
import math

class Ship(pygame.sprite.Sprite):
    def __init__(self, image):
        
        self.pos = (0,0) #Default Position relative to screen
        
        self.speed = 0
        self.angle = -90
        
        self.original_image = image
        self.update_image()
        self.rect.center = self.pos
        
        #Ship Specs
        self.max_speed = 15
        self.speed_increment = 1
        self.turn_increment = 3
        self.shield = 100
        
        #TO FIX
        self.map_center = (15730, 15730)
        
        #Player Position relative to map center
        self.position = self.map_center
        self.update_position()
        
        
    def set_position(self, pos):
        self.position = pos
        print(f"Ship.set_position : {pos}")
        
    def turn_left(self):
        self.turn(self.turn_increment)
    
    
    def turn_right(self):
        self.turn(-self.turn_increment)
    
    
    def update_image(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle + 90)
        self.rect = self.image.get_rect()
        
        
    def turn(self, amount):
        self.angle += amount
        
        self.angle = self.angle % 360
        self.update_image()
        
        
    def power_up(self):
        val = self.speed_increment
        self.set_speed(val)
    
    
    def power_down(self):
        self.set_speed(-self.speed_increment)
      
        
    def set_speed(self, amount):
        self.speed += amount
        
        if self.speed < 0:
            self.speed = 0
        elif self.speed > self.max_speed:
            self.speed = self.max_speed
    
    
    def reset(self):
        self.angle = 0
        self.speed = 0
        
        self.update_image()
        
        self.position = self.map_center
        self.update_position()
    
    
    def shoot(self):
        pass


    def move(self):
        rad_angle = math.radians(self.angle)
        
        x = self.position[0] - self.speed * math.cos(rad_angle)
        y = self.position[1] + self.speed * math.sin(rad_angle) # (-) because of coordinate inversion
        
        self.position = (x,y)
    
        self.update_position()
    
    
    def update_position(self):
        dist_from_sun = math.dist(self.map_center, self.position)
        angle = 0
        if dist_from_sun > 0:
            dx = self.position[0] - self.map_center[0]
            dy = self.position[1] - self.map_center[1]
            rad_angle = math.atan2(dy, dx)

            angle = math.degrees(rad_angle)
            
        self.position_angle = angle
        self.position_radius = dist_from_sun