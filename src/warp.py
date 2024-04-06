import pygame
import pygame_gui
import random
import math

from pygame_framework.Scene import Scene
from pygame_framework.Colors import Colors
from pygame_framework.Util import Util


MIN_RADIUS = 10
MAX_RADIUS = 200
END_RADIUS = 900
NEW_WARP_LINE_PER_TICK = 2
WARP_LINE_GROW = 15

class Warp_Scene(Scene):
    def on_init(self, world):
        self.name = "Warp"

        #Redefinie Background color
        self.BACKGROUND = Colors.BLACK

        self.title = "Warp"
        self.title_font = pygame.font.SysFont("Arial", 24)

        #Pygame GUI 
        self.manager = pygame_gui.UIManager(self.size)
    
        self.init_warp_line_colors()
    
        #Create UI
        self.create_gui()
        
        self.start_warp()
        
        #reference to the world
        self.world = world

        #Last step of intitialisation
        self.inited = True

    def create_gui(self):
        button_width = 120
        button_height = 30

        #New Return
        x = 10
        y = 200
        rect = pygame.Rect(x, y, button_width, button_height)
        text = "Space"
        id = "#btn_space"
        self.btn_space = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)

    def start_warp(self):
        self.warp_duration = 10000
        self.warp_started = None
        
        self.warp_lines = list()

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
        
        if self.warp_started == None:
            self.warp_started = pygame.time.get_ticks()
        else:
            duration = pygame.time.get_ticks() - self.warp_started
            if duration > self.warp_duration:
                self.warp_ended()
            else:
                center = pygame.display.get_surface().get_rect().center
                
                #Update existing warp lines
                for warp_line in self.warp_lines:
                    if warp_line.lenght < warp_line.max_lenght:
                        #Update Lenght of warp Line
                        warp_line.lenght += WARP_LINE_GROW
                        
                        #Update End of Warp Line
                        radius = MIN_RADIUS + warp_line.lenght
                        x = center[0] + radius * math.cos(warp_line.start_angle)
                        y = center[1] + radius * math.sin(warp_line.start_angle)
                        warp_line.start_point = (x,y)
                    
                    else:
                        warp_line.offset += WARP_LINE_GROW
                        #Update Start Point
                        radius = MIN_RADIUS + warp_line.offset
                        x = center[0] + radius * math.cos(warp_line.start_angle)
                        y = center[1] + radius * math.sin(warp_line.start_angle)
                        warp_line.start_point = (x,y)
                        
                        #Update End Point
                        radius = MIN_RADIUS + warp_line.lenght + warp_line.offset
                        end_radius = radius
                        x = center[0] + radius * math.cos(warp_line.start_angle)
                        y = center[1] + radius * math.sin(warp_line.start_angle)
                        warp_line.end_point = (x,y)
                                                
                        if end_radius >= END_RADIUS:
                            self.warp_lines.remove(warp_line)
                
                #Get some new random lines
                for i in range(NEW_WARP_LINE_PER_TICK):
                    angle = random.randint(0,360)
                    max_lenght = random.randint(150,400)
                    start_angle = math.radians(angle)
                    radius = random.randint(MIN_RADIUS, MAX_RADIUS)
                    
                    x = center[0] + radius * math.cos(start_angle)
                    y = center[1] + radius * math.sin(start_angle)
                    start_point = (x,y)
                    
                    #Random Color
                    col_index = random.randint(0, len(self.warp_line_colors)-1)
                    color = self.warp_line_colors[col_index]
                    
                    wl = WarpLine(start_point, color, start_angle, max_lenght)
                    self.warp_lines.append(wl)
    
    def init_warp_line_colors(self):
        self.warp_line_colors = list()
        self.warp_line_colors.append(Colors.BLUE)
        self.warp_line_colors.append(Colors.BLUE)
        self.warp_line_colors.append(Colors.BLUE)
        self.warp_line_colors.append(Colors.WHITE)
        self.warp_line_colors.append(Colors.WHITE)
        self.warp_line_colors.append(Colors.WHITE)
        self.warp_line_colors.append(Colors.AQUA)
        self.warp_line_colors.append(Colors.BLUE)
        self.warp_line_colors.append(Colors.YELLOW)
           
     
    def warp_ended(self):
        self.warp_started = None
        self.fire_goto_event("Space") 


    def on_render(self, surface):
        surface.fill(self.BACKGROUND)

        self.manager.draw_ui(surface)

        #Draw Title on center surface x
        Util().draw_text_center_x(surface, self.title, self.title_font, Colors.BLACK, 15)
        
        #Draw Lines
        for warp_line in self.warp_lines:
            warp_line.draw(surface)
           

class WarpLine():
    def __init__(self, start_point, color, start_angle, max_lenght):
        self.start_angle = start_angle
        self.max_lenght = max_lenght
        self.start_point = start_point
        self.lenght = 0
        self.offset = 0
        self.end_point = start_point
        self.color = color
    
    
    def draw(self, surface):
        pygame.draw.line(surface, self.color, self.start_point, self.end_point, width = 2)
        
        
        
