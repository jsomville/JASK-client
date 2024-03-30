import pygame
import pygame_gui
import json

from pygame_framework.Scene import Scene
from pygame_framework.Colors import Colors
from pygame_framework.Util import Util
from pygame_framework.UI_Position import UI_Position

class Map_Scene(Scene):
    def on_init(self):
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
        
        #Load Map
        self.read_map()
        self.process_map()

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


    def read_map(self):
        with open('src/data/map.json') as file :
            map = json.load(file)
            
            self.solarSystems = map["SolarSystems"]
            
    
    def process_map(self):
        self.map = dict()
        lanes=list()
        for ss in self.solarSystems:
            name = ss["name"]
            p_temp = ss["position"]
            
            #Give it an offset
            x = p_temp[0] + 800
            y = p_temp[1] + 100
            ss["screenPosition"] = (x, y)
            
            #Create Map
            self.map[name] = ss["screenPosition"]
            
            #Process links
            for link in ss["links"]:
                #In alphabetical order
                lane = (name, link)
                if name < link:
                    lane = (link, name)
                lanes.append(lane)
            
        #Remove duplicates        
        self.lanes = list(dict.fromkeys(lanes))
        
    def draw_map(self, surface):
        #Draw stars
        for lane in self.lanes:
            color = Colors.WHITE
            start = self.map[lane[0]]
            end = self.map[lane[1]]
            pygame.draw.line(surface, color, start, end, 1)
        
        #Draw Star systems
        for ss in self.solarSystems:
            #Draw Star
            color = self.get_star_Color(ss["type"])
            radius = 5
            center = ss["screenPosition"]
            pygame.draw.circle(surface, color, center, radius)
            
            #Draw System name
            text = ss["name"]
            img = self.map_font.render(text, True, Colors.WHITE)
            text_rect = img.get_rect(center = (center[0], center[1] + 15))
            surface.blit(img, text_rect)
          
    def get_star_Color(self, type):
        color = Colors.BLACK
        if type == "O":
            color = Colors.PURPLE
        elif type == "B":
            color = Colors.BLUE
        elif type == "A":
            color = Colors.WHITE
        elif type == "G":
            color = Colors.YELLOW
        elif type == "F":
            color = Colors.LIME
        elif type == "K":
            color = Colors.ORANGE
        elif type == "M":
            color = Colors.RED
            
        return color
        
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

