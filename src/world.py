import pygame
import json

from .character import Character
from .ship import Ship

class World:
    def __init__(self):
        
        self.load_map()
        self.process_map()
    
    def set_character(self, character):
        self.character = character
        
        #Determine the ship
        image = pygame.image.load('src/data/images/ship/top_view/sparrow.png').convert_alpha()
        
        #Set the ship
        self.ship = Ship(image)
    
    def load_map(self):
        with open('src/data/map.json') as file :
            map = json.load(file)
            
            self.solarSystems = map["SolarSystems"]
    
    def process_map(self):
        self.map = dict()
        self.map_ss = dict()
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
            self.map_ss[name] = ss
            
            #Process links
            for link in ss["links"]:
                #In alphabetical order
                lane = (name, link)
                if name < link:
                    lane = (link, name)
                lanes.append(lane)
            
        #Remove duplicates        
        self.lanes = list(dict.fromkeys(lanes))
    
    def get_current_solar_system(self):
        ss_name = self.character.solar_system
        ss = self.map_ss[ss_name] 
        return ss
        