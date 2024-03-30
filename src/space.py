import pygame
import pygame_gui

from pygame_framework.Scene import Scene
from pygame_framework.Colors import Colors
from pygame_framework.Util import Util

class Space_Scene(Scene):
    def on_init(self, world):
        self.name = "Space"

        #Redefinie Background color
        self.BACKGROUND = "#45494e"
        self.BACKGROUND = Colors.BLACK

        self.title = "This is the void of space"
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
        spacer = 10
        base_x = 220
        base_y = 550

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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.world.ship.turn_left()
            elif event.key == pygame.K_RIGHT:
                self.world.ship.turn_right()
            elif event.key == pygame.K_UP:
                self.world.ship.power_up()
            elif event.key == pygame.K_DOWN:
                self.world.ship.power_down()
            elif event.key == pygame.K_r or event.key == pygame.K_R:
                self.world.ship.reset()
            elif event.key == pygame.K_s or event.key == pygame.K_S:
                self.world.ship.shoot()
                
        
    def on_loop(self):
        time_delta = pygame.time.Clock().tick()/1000.0
        self.manager.update(time_delta)

    def on_render(self, surface):
        surface.fill(self.BACKGROUND)

        #Draw Title on center surface x
        #Util().draw_text_center_x(surface, self.title, self.title_font, Colors.BLACK, 15)

        #Draw Map
        self.draw_solar_system(surface)
        
        #Draw Radar
        self.draw_radar(surface)
        
        #Draw Other ships

        #Draw my Ship
        image = self.world.ship.image
        rect = self.world.ship.rect
        rect.center = surface.get_rect().center
        surface.blit(image, rect)

        #Draw The UI
        self.manager.draw_ui(surface)
    
    def draw_solar_system(self, surface):
        current_ss = self.world.get_current_solar_system()
        for planet in current_ss["objects"]:
            print(planet)

    def draw_radar(self, surface):
        pass

