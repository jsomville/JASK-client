import pygame
import pygame_gui
import math

from pygame_framework.Scene import Scene
from pygame_framework.Colors import Colors
from pygame_framework.Util import Util

from .camera import Camera

class Space_Scene(Scene):
    def on_init(self, world):
        self.name = "Space"

        #Redefinie Background color
        self.BACKGROUND = "#45494e"
        self.BACKGROUND = Colors.BLACK

        self.title = "This is the void of space"
        self.title_font = pygame.font.SysFont("Arial", 24)
        self.helper_font = pygame.font.SysFont("Arial", 10)

        #Pygame GUI 
        self.manager = pygame_gui.UIManager(self.size)
    
        #Create UI
        self.create_gui()
        self.create_temp_gui()
        
        #reference to the world
        self.world = world
        self.map = None
        
        self.show_mini_map = True
        self.show_helper = True
        self.show_orbit = True
        self.show_radar = True

        #Last step of intitialisation
        self.inited = True
        
    def create_temp_gui(self):
        button_width = 120
        button_height = 30
        spacer = 10
        base_x = 700
        base_y = 20

        #Temporary Dock
        x = base_x
        y = base_y
        rect = pygame.Rect(x, y, button_width, button_height)
        text = "Dock to station"
        id = "#btn_dock"
        self.btn_dock = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)

        #Temporary Die
        x = base_x + (button_width + spacer) * 1
        y = base_y
        rect = pygame.Rect(x, y, button_width, button_height)
        text = "Die !"
        id = "#btn_die"
        self.btn_die = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)

        #Temporary Warp
        x = base_x + (button_width + spacer) * 2
        y = base_y
        rect = pygame.Rect(x, y, button_width, button_height)
        text = "Warp"
        id = "#btn_warp"
        self.btn_warp = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)

    def create_gui(self):
        button_width = 100
        button_height = 30
        base_x = 10
        base_y = 150
        
        #Toggle Mini Map
        x = base_x
        y = base_y
        rect = pygame.Rect(x, y, button_width, button_height)
        text = "Mini Map"
        id = "#btn_mini_map"
        self.btn_mini_map = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)
        
        #Toggle Radar
        y = y + 40
        rect = pygame.Rect(x, y, button_width, button_height)
        text = "Radar"
        id = "#btn_radar"
        self.btn_radar = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)
        
        #Toggle Orbit
        y = y + 40
        rect = pygame.Rect(x, y, button_width, button_height)
        text = "Orbit"
        id = "#btn_orbit"
        self.btn_orbit = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)

    def on_event(self, event):

        self.manager.process_events(event)

        self.event_controls(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if hasattr(event, "ui_element"):
                if event.ui_element == self.btn_dock:
                    print("Clicked on Dock")

                    self.fire_goto_event("Station")
                elif event.ui_element == self.btn_warp:
                    print("Clicked on Warp")

                    self.fire_goto_event("Warp")
                elif event.ui_element == self.btn_die:
                    print("Clicked on Die")

                    self.fire_goto_event("Die")
                elif event.ui_element == self.btn_mini_map:
                    #Toggle Mini map
                    self.show_mini_map = not self.show_mini_map
                elif event.ui_element == self.btn_orbit:
                    #Toggle Planet Orbit
                    self.show_orbit = not self.show_orbit
                elif event.ui_element == self.btn_radar:
                    #Toggle Radar
                    self.show_radar = not self.show_radar
                    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.world.ship.reset()
            elif event.key == pygame.K_s:
                self.world.ship.shoot()  
        

    
    def check_pressed_keys(self):
        #Check key pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.world.ship.turn_left()
        elif keys[pygame.K_RIGHT]:
            self.world.ship.turn_right()
        elif keys[pygame.K_UP]:
            self.world.ship.power_up()
        elif keys[pygame.K_DOWN]:
            self.world.ship.power_down()
    
    def on_loop(self):
        #For UI manager Timers
        time_delta = pygame.time.Clock().tick()/1000.0
        self.manager.update(time_delta)
        
        #Check if map exists
        if self.map != self.world.character.solar_system:
            self.map = self.world.character.solar_system
            
            #Proces Map
            self.world.process_current_map()
        
        #Handle Keys 
        self.check_pressed_keys()

        #Move the ship
        self.world.ship.move()

    def on_render(self, surface):
        #Background
        surface.fill(self.BACKGROUND)

        #Draw The map & objects
        self.world.draw_map(surface, self.show_orbit)
        
        #Draw Mini Map
        if self.show_mini_map:
            self.draw_mini_map(surface)
        
        #Draw Radar
        if self.show_radar:
            self.draw_radar(surface)
        
        #Draw Text Helpers
        if self.show_helper:
            self.draw_helpers(surface)

        #Draw The UI
        self.manager.draw_ui(surface)


    def draw_mini_map(self, surface: pygame.surface):
        #TO FIX
        radius_max = 140
        y = surface.get_height() - (radius_max * 2) - 50
        top = (10,y)
        PLANET_COLOR = Colors.GRAY
        ORBIT_COLOR = Colors.GRAY
        MINI_MAP_COLOR = Colors.DARK_GRAY
        PLAYER_COLOR = Colors.RED
        PLANET_RADIUS = 2
        PLAYER_RADIUS = 2
        
        size = (radius_max * 2 + 4 ,radius_max * 2 + 4)
        rect = pygame.Rect(top, size)
        pygame.draw.rect(surface, MINI_MAP_COLOR, rect, width=2)
        
        current_ss = self.world.get_current_solar_system()
        center = rect.center
        radius = 2
        for planet in current_ss["objects"]:
            radius = planet["relative_distance"] * (radius_max)
            
            #Draw Planet Orbit
            pygame.draw.circle(surface, ORBIT_COLOR, center, radius, width=1)
            
            #Draw Planet
            rad_angle = math.radians(planet["angle"])
            x = center[0] + radius * math.cos(rad_angle) + PLANET_RADIUS
            y = center[1] + radius * math.sin(rad_angle) + PLANET_RADIUS
            pygame.draw.circle(surface, PLANET_COLOR, (x,y), PLANET_RADIUS)
            
        #Draw my Position
        rel_radius = self.world.ship.position_radius / current_ss["max_distance"]
        radius = rel_radius * radius_max
        angle = self.world.ship.position_angle
        rad_angle = math.radians(angle)
        x = center[0] + radius * math.cos(rad_angle) - PLAYER_RADIUS
        y = center[1] + radius * math.sin(rad_angle) - PLAYER_RADIUS
        pygame.draw.circle(surface, PLAYER_COLOR, (x,y), PLAYER_RADIUS)
    
    def draw_radar(self, surface):
        pass 
            
    def draw_helpers(self, surface):
        #Values
        position = self.world.ship.position
        rounded_pos = round(position[0]), round(position[1])
        
        x = 10
        y = 10
        
        #Draw Position
        text = f"Position : {rounded_pos}"
        self.draw_helper(surface, text, (x,y))
        
        #Draw Speed
        y += 12
        text = f"Speed : {self.world.ship.speed}"
        self.draw_helper(surface, text, (x,y))
        
        #Draw Angle
        y += 12
        text = f"Angle : {self.world.ship.angle}"
        self.draw_helper(surface, text, (x,y))
        
        #Draw Position Angle
        y += 12
        text = f"Position Angle : {self.world.ship.position_angle}"
        self.draw_helper(surface, text, (x,y))
        
        #Draw Position Radius
        y += 12
        text = f"Radius : {self.world.ship.position_radius}"
        self.draw_helper(surface, text, (x,y))
        
        #Draw Max Radius
        y += 12
        max_distance = self.world.get_current_solar_system()["max_distance"]
        text = f"Max Distance: {max_distance}"
        self.draw_helper(surface, text, (x,y))


    def draw_helper(self, surface, text, position):
        img = self.helper_font.render(text, True, Colors.WHITE)
        text_rect = img.get_rect()
        text_rect.x = position[0]
        text_rect.y = position[1]
        surface.blit(img, text_rect)
        
        
