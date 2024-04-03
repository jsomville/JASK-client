import pygame
import math

class Ship(pygame.sprite.Sprite):
    def __init__(self, image):
        self.pos = (0,0) #Default Position relative to screen
        
        self.speed = 0
        self.angle = 0
        self.original_image = image
        self.update_image()
        self.rect.center = self.pos
        
        #Ship Specs
        self.max_speed = 20
        self.speed_increment = 2
        self.turn_increment = 5
        self.shield = 100
        
        #Player Position relative to map center
        self.position = (0,0)
        self.update_position()

        
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
        
        self.position = (0,0)
        self.update_position()
    
    
    def shoot(self):
        pass


    def move(self):
        pos = self.position
        rad_angle = math.radians(self.angle)
        
        x = self.position[0] - self.speed * math.cos(rad_angle)
        y = self.position[1] + self.speed * math.sin(rad_angle) # (-) because of coordinate inversion
        
        self.position = (x,y)
    
        self.update_position()
    
    
    def update_position(self):
        dist_from_sun = math.dist((0,0), self.position)
        angle = 0
        if dist_from_sun > 0:
            rad_angle = math.atan2(self.position[1], self.position[0])
            angle = round(math.degrees(rad_angle))
            
        self.position_angle = angle
        self.position_radius = dist_from_sun