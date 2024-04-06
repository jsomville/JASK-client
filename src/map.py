import pygame
import pygame_gui
import json

from pygame_framework.Scene import Scene
from pygame_framework.Colors import Colors
from pygame_framework.Util import Util
from pygame_framework.UI_Position import UI_Position

class Map_Scene(Scene):
    def on_init(self, world):
        self.name = "Map"

        #Redefinie Background color
        self.BACKGROUND = "#45494e"

        self.title = "Star Map"
        self.title_font = pygame.font.SysFont("Arial", 24)
        
        self.map_font = pygame.font.SysFont("Arial", 10)

        #Pygame GUI 
        self.manager = pygame_gui.UIManager(self.size)
    
        #Create UI
        self.create_gui()

        #reference to the world
        self.world = world
        print("on init")

        #Last step of intitialisation
        self.inited = True

    def create_gui(self):
        button_width = 120
        button_height = 30

        #New Return
        x = 500
        y = 400
        rect = pygame.Rect(x, y, button_width, button_height)
        text = "Return"
        id = "#btn_return"
        self.btn_return = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)
        
        
    def draw_map(self, surface):
        #Draw stars
        
        for lane in self.world.lanes:
            color = Colors.WHITE
            start = self.world.map[lane[0]]
            end = self.world.map[lane[1]]
            pygame.draw.line(surface, color, start, end, 1)
        
        #Draw Star systems
        for ss in self.world.solarSystems:
            #Draw Star
            color = self.world.get_star_Color(ss["type"])
            radius = 5
            center = ss["screenPosition"]
            pygame.draw.circle(surface, color, center, radius)
            
            #Draw System name
            text = ss["name"]
            img = self.map_font.render(text, True, Colors.WHITE)
            text_rect = img.get_rect(center = (center[0], center[1] + 15))
            surface.blit(img, text_rect)
          
    
        
    def on_event(self, event):

        self.manager.process_events(event)

        self.event_controls(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if hasattr(event, "ui_element"):
                if event.ui_element == self.btn_return:
                    print("Clicked on Return")

                    self.fire_goto_event("Station")

        
    def on_loop(self):
        time_delta = pygame.time.Clock().tick()/1000.0
        self.manager.update(time_delta)
        

    def on_render(self, surface):
        surface.fill(self.BACKGROUND)

        #Draw Title on center surface x
        Util().draw_text_center_x(surface, self.title, self.title_font, Colors.BLACK, 15)

        self.draw_map(surface)

        self.manager.draw_ui(surface)

