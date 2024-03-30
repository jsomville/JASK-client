import pygame

class Ship(pygame.sprite.Sprite):
    def __init__(self, image):
        self.pos = (100,100)
        
        self.speed = 0
        self.angle = 0
        self.original_image = image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        
        #Ship Specs
        self.max_speed = 50
        self.speed_increment = 1
        self.turn_increment = 5
        self.shield = 100
        
    def turn_left(self):
        self.turn(-self.turn_increment)
    
    def turn_right(self):
        self.turn(self.turn_increment)
    
    def turn(self, amount):
        self.angle += amount
        
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        
    def power_up(self):
        self.speed(self.speed_increment)
    
    def power_down(self):
        self.speed(-self.speed_increment)
        
    def speed(self, amount):
        self.speed += amount
        
        if self.speed < 0:
            self.speed = 0
        elif self.speed > self.max_speed:
            self.speed = self.max_speed
    
    def reset(self):
        self.angle = 0
        self.speed = 0
    
    def shoot(self):
        pass
