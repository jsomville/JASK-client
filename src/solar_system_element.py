import pygame

class SolarSystemElement(pygame.sprite.Sprite):
    def __init__(self, pos, group : pygame.sprite.Group, image: pygame.image):
        super().__init__(group)
        
        self.image = image
        self.rect = image.get_rect(center = pos)