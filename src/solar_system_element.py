import pygame

class SolarSystemElement(pygame.sprite.Sprite):
    def __init__(self, pos, group : pygame.sprite.Group, image: pygame.image):
        super().__init__(group)
        
        self.image = image
        self.rect = image.get_rect()
        
        #Seems to have a bug with center and Spritegroup
        #self.rect.center = pos
        
        self.rect.centerx = pos[0] - self.rect.width /2
        self.rect.centery = pos[1] - self.rect.height /2
        
        