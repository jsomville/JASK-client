import pygame
import pygame_gui

from pygame_framework.Scene import Scene
from pygame_framework.Colors import Colors
from pygame_framework.Util import Util

class Station_Scene(Scene):
    def on_init(self, world):
        self.name = "Station"

        #Redefinie Background color
        self.BACKGROUND = "#45494e"

        self.title = "Station [Name]"
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
        service_button_width = 200
        service_button_height = 30
        container_width = 650
        image_height = 150
        text_height = 150
        spacer_y = 10
        spacer_x = 25
        base_y  = 30
        base_x = 50

        #New Button
        x = base_x
        y = base_y
        rect = pygame.Rect((x,y), (container_width, image_height))
        text = ""
        id = "#btn_station"
        self.btn_station = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)

        #Station text
        x = base_x
        y = base_y + spacer_y + image_height
        rect = pygame.Rect(x,y, container_width, text_height)
        html_text = self.load_station()
        id = "#ui_text_box"
        self.ui_text_box = pygame_gui.elements.UITextBox(html_text, rect, manager= self.manager, object_id=id)

        #Stations Services
        service_x = base_x
        service_y = base_y + text_height + image_height + 2 * spacer_y
        #Market
        x = self.get_posi_from_grid(service_x, service_button_width, spacer_x, 0)
        y = self.get_posi_from_grid(service_y, service_button_height, spacer_y, 0)
        rect = pygame.Rect((x,y), (service_button_width, service_button_height))
        text = "Market"
        id = "#btn_market"
        self.btn_market = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)

        #Job
        x = self.get_posi_from_grid(service_x, service_button_width, spacer_x, 0)
        y = self.get_posi_from_grid(service_y, service_button_height, spacer_y, 1)
        rect = pygame.Rect((x,y), (service_button_width, service_button_height))
        text = "Job"
        id = "#btn_job"
        self.btn_job = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)

        #Map
        x = self.get_posi_from_grid(service_x, service_button_width, spacer_x, 0)
        y = self.get_posi_from_grid(service_y, service_button_height, spacer_y, 2)
        rect = pygame.Rect((x,y), (service_button_width, service_button_height))
        text = "Map"
        id = "#btn_map"
        self.btn_map = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)

        #Outfitter
        x = self.get_posi_from_grid(service_x, service_button_width, spacer_x, 1)
        y = self.get_posi_from_grid(service_y, service_button_height, spacer_y, 0)
        rect = pygame.Rect((x,y), (service_button_width, service_button_height))
        text = "Outfitter"
        id = "#btn_outfitter"
        self.btn_outfitter = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)

        #Spaceport
        x = self.get_posi_from_grid(service_x, service_button_width, spacer_x, 1)
        y = self.get_posi_from_grid(service_y, service_button_height, spacer_y, 1)
        rect = pygame.Rect((x,y), (service_button_width, service_button_height))
        text = "Spaceport"
        id = "#btn_spaceport"
        self.btn_spaceport = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)

        #Undock
        x = self.get_posi_from_grid(service_x, service_button_width, spacer_x, 2)
        y = self.get_posi_from_grid(service_y, service_button_height, spacer_y, 2)
        rect = pygame.Rect((x,y), (service_button_width, service_button_height))
        text = "Undock"
        id = "#btn_undock"
        self.btn_undock = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)

    def get_posi_from_grid(self, base, width, spacer, grid):
        return base + grid* (width + spacer)

    def load_station(self):
        filepath = "src/data/test/station.html"
        with open(filepath, 'r') as page:
            html_text = page.read()
        
        return html_text

    def on_event(self, event):

        self.manager.process_events(event)

        self.event_controls(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if hasattr(event, "ui_element"):
                if event.ui_element == self.btn_job:
                    print("Clicked on Job ")
                    self.fire_goto_event("Job")
                elif event.ui_element == self.btn_map:
                    print("Clicked on Map")
                    self.fire_goto_event("Map")
                elif event.ui_element == self.btn_market:
                    print("Clicked on Market")
                    self.fire_goto_event("Market")
                elif event.ui_element == self.btn_outfitter:
                    print("Clicked on Outfitter")
                    self.fire_goto_event("Outfitter")
                elif event.ui_element == self.btn_spaceport:
                    print("Clicked on Spaceport")
                    self.fire_goto_event("Spaceport")
                elif event.ui_element == self.btn_undock:
                    print("Clicked on Undock")
                    self.fire_goto_event("Space")
        
    def on_loop(self):
        time_delta = pygame.time.Clock().tick()/1000.0
        self.manager.update(time_delta)
        

    def on_render(self, surface):
        surface.fill(self.BACKGROUND)

        #Draw Title on center surface x
        Util().draw_text_center_x(surface, self.title, self.title_font, Colors.BLACK, 15)

        self.manager.draw_ui(surface)

