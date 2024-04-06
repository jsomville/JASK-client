import pygame
import json
import glob
import os
import random
from pygame_framework.Colors import Colors

from .character import Character
from .ship import Ship
from .camera import Camera
from .solar_system_element import SolarSystemElement

MAP_FILE = 'src/data/new_map.json'
class World:
    def __init__(self):
        #Load Images
        self.load_map_images()
        
        #Load Map
        self.load_map()
        self.process_map()
        
        #Camera
        self.camera = Camera()
    
    
    def set_character(self, character: Character):
        self.character = character
        
        #Determine the ship
        image = pygame.image.load('src/data/images/ship/top_view/sparrow.png').convert_alpha()
        
        #Set the ship
        self.ship = Ship(image)
        x = 15730 /2
        y = 15730 /2
        pos = (x,y)
        self.ship.set_position(pos)
    
    
    def load_map_images(self):
        #Load stars
        path = "src/data/images/star/*.png"
        files = glob.glob(path)
        self.stars_images = dict()
        for file in files:
            basename = os.path.basename(file)
            name = os.path.splitext(basename)[0]
            image = pygame.image.load(file).convert_alpha()
            self.stars_images[name] = image
            
        #Load Planets
        path = "src/data/images/planet/*.png"
        files = glob.glob(path)
        self.planets_images = dict()
        for file in files:
            basename = os.path.basename(file)
            name = os.path.splitext(basename)[0]
            image = pygame.image.load(file).convert_alpha()
            self.planets_images[name] = image
            
        #Load Asteroids
        path = "src/data/images/asteroid/*.png"
        files = glob.glob(path)
        self.asteroids_images = dict()
        self.asteroids_list = list()
        for file in files:
            basename = os.path.basename(file)
            name = os.path.splitext(basename)[0]
            image = pygame.image.load(file).convert_alpha()
            self.asteroids_images[name] = image
            self.asteroids_list.append(name)
        
    
    def load_map(self):
        with open(MAP_FILE)as file :
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
            
            #Process links
            for link in ss["links"]:
                #In alphabetical order
                lane = (name, link)
                if name < link:
                    lane = (link, name)
                lanes.append(lane)
                    
            #set planet attributes
            max = ss["map_size"][0]
            ss["max_distance"] = max
            for planet in ss["objects"]:
                #Relative distance in %
                planet["relative_distance"] = planet["distance"] / max
            
            #Create Map
            self.map[name] = ss["screenPosition"]
            self.map_ss[name] = ss
            
        #Remove duplicates        
        self.lanes = list(dict.fromkeys(lanes))
    
    def get_current_solar_system(self):
        ss_name = self.character.solar_system
        ss = self.map_ss[ss_name] 
        return ss
    
    def process_current_map(self):
        print("process current map")
        ss = self.get_current_solar_system()
        
        # List of Elements to display on space
        self.solar_system_elements = list()
        
        map_size = ss["map_size"]
        
        #Add sun
        pos = (map_size[0] / 2, map_size[1]/2)
        sprite_name = ss["sprite"]
        image= self.stars_images[sprite_name]
        sun = SolarSystemElement(pos, self.camera, image)
        self.solar_system_elements.append(sun)
        print(f"sun : {pos}")
        
        #Loop trough objects
        for object in ss["objects"]:
            #For planets
            if object["type"] == "planet":
                pos = object["position"]
                sprite_name = object["sprite"]
                image = self.planets_images[sprite_name]
                
                planet = SolarSystemElement(pos, self.camera, image)
                planet.name = object["name"]
                self.solar_system_elements.append(planet)
                print(f"planet : {planet.name} pos :{pos}")
        
        #Add random asteroids
        for i in range(1000):
            x = random.randint(0, map_size[0])
            y = random.randint(0, map_size[1])
            pos = (x,y)
            asteroid_type = random.randint(0, len(self.asteroids_list)-1)
            asteroid_name = self.asteroids_list[asteroid_type]
            image = self.asteroids_images[asteroid_name]
            asteroid = SolarSystemElement(pos, self.camera, image)
            self.solar_system_elements.append(asteroid)
    
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
    
    
    def draw_map(self, surface):
        pos = self.ship.position
        
        #Draw SS Elements
        self.camera.custom_draw(surface, pos)
        
        #Draw My ship
        self.draw_my_ship(surface)
    
    
    def draw_my_ship(self, surface):
        #Draw my Ship
        image = self.ship.image
        rect = self.ship.rect
        rect.center = surface.get_rect().center
        surface.blit(image, rect)