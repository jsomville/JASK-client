import pygame
import pygame_gui

from pygame_framework.Scene import Scene
from pygame_framework.Colors import Colors
from pygame_framework.Util import Util

from .character import Character

class Character_Selection_Scene(Scene):
    def on_init(self, world):
        self.name = "Character Selection"

        #Redefinie Background color
        self.BACKGROUND = "#45494e" #Colors.OLIVE

        self.title = "Character Selection"
        self.title_font = pygame.font.SysFont("Arial", 24)

        #Pygame GUI 
        self.manager = pygame_gui.UIManager(self.size)
    
        #Create UI
        self.create_gui()
        
        #reference to the world
        self.world = world

        #Last step of intitialisation
        self.inited = True

    def create_gui(self):
        button_width = 120
        button_height = 30
        button_x = 500
        container_width = 600
        container_height = 350
        spacer_y = 10
        base_y  = 60
        base_x = 100

        #New Button
        x = base_x + container_width - button_width
        y = base_y
        rect = pygame.Rect((x,y), (button_width, button_height))
        text = "New"
        id = "#btn_new"
        self.btn_new = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)

        #Character Container
        x = base_x
        y = base_y + spacer_y + button_height
        rect = pygame.Rect(x,y, container_width, container_height)
        html_text = self.load_character()
        id = "#ui_text_box"
        self.ui_text_box = pygame_gui.elements.UITextBox(html_text, rect, manager= self.manager, object_id=id)

        #Select Button
        x = base_x + container_width - button_width
        y = base_y + container_height + (2 * spacer_y) + button_height
        rect = pygame.Rect(x,y, button_width, button_height)
        text = "Select"
        id = "#btn_select"
        self.btn_select = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)
    
    def load_character(self):
        filepath = "src/data/test/character.html"
        with open(filepath, 'r') as page:
            html_text = page.read()
        
        return html_text

    def on_event(self, event):

        self.manager.process_events(event)

        self.event_controls(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if hasattr(event, "ui_element"):
                if event.ui_element == self.btn_new:
                    print("Clicked on New ")
                    self.fire_goto_event("New Character")
                if event.ui_element == self.btn_select:
                    print("Clicked on Select")
                    self.select_character()
                    self.fire_goto_event("Station")
                    
    def select_character(self):
        character = Character()     
        
        self.world.set_character(character)
        
        
    def on_loop(self):
        time_delta = pygame.time.Clock().tick()/1000.0
        self.manager.update(time_delta)
        

    def on_render(self, surface):
        surface.fill(self.BACKGROUND)

        #Draw Title on center surface x
        Util().draw_text_center_x(surface, self.title, self.title_font, Colors.BLACK, 15)

        self.manager.draw_ui(surface)

