import pygame

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        
        self.offset= pygame.math.Vector2()
        
        #self.zoom = 1
    
    def custom_draw(self, surface: pygame.Surface, pos):
        
        self.offset = pos
        
        for sprite in self.sprites():
            x = sprite.rect.centerx - self.offset[0]
            y = sprite.rect.centery - self.offset[1]
            surface.blit(sprite.image, (x,y))
