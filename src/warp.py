import pygame
import pygame_gui

from pygame_framework.Scene import Scene
from pygame_framework.Colors import Colors
from pygame_framework.Util import Util

class Warp_Scene(Scene):
    def on_init(self):
        self.name = "Warp"

        #Redefinie Background color
        self.BACKGROUND = "#45494e"

        self.title = "Warp"
        self.title_font = pygame.font.SysFont("Arial", 24)

        #Pygame GUI 
        self.manager = pygame_gui.UIManager(self.size)
    
        #Create UI
        self.create_gui()

        #Last step of intitialisation
        self.inited = True

    def create_gui(self):
        button_width = 120
        button_height = 30

        #New Return
        x = 500
        y = 400
        rect = pygame.Rect(x, y, button_width, button_height)
        text = "Space"
        id = "#btn_space"
        self.btn_space = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)


    def on_event(self, event):

        self.manager.process_events(event)

        self.event_controls(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if hasattr(event, "ui_element"):
                if event.ui_element == self.btn_space:
                    print("Clicked on Space")

                    self.fire_goto_event("Space")

        
    def on_loop(self):
        time_delta = pygame.time.Clock().tick()/1000.0
        self.manager.update(time_delta)
        

    def on_render(self, surface):
        surface.fill(self.BACKGROUND)

        #Draw Title on center surface x
        Util().draw_text_center_x(surface, self.title, self.title_font, Colors.BLACK, 15)

        self.manager.draw_ui(surface)

