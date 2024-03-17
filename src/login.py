#!/usr/bin/env python3

import pygame
import pygame_gui

from pygame_framework.Scene import Scene
from pygame_framework.Colors import Colors
from pygame_framework.Util import Util

class Login_Scene(Scene):
    def on_init(self):
        self.name = "Login"

        #Redefinie Background color
        self.BACKGROUND = "#45494e" #Colors.OLIVE

        self.title = "Login"
        self.title_font = pygame.font.SysFont("Arial", 24)

        #Pygame GUI 
        self.manager = pygame_gui.UIManager(self.size)
        #self.manager = pygame_gui.UIManager(self.size, themedefinitionfile)

        #Create the GUI
        self.create_gui()

        #Last step of intitialisation
        self.inited = True

    def create_gui(self):

        x = 200
        y = 120
        textbox_width = 200
        default_height = 30
        label_width = 80
        column_space = label_width + 10

        rect = pygame.Rect(x,y,label_width,default_height)
        text = "Email :"
        self.lbl_username = pygame_gui.elements.UILabel(rect, text, self.manager)
        
        rect = pygame.Rect(x + column_space,y,textbox_width,default_height)
        id = "#txt_email"
        self.txt_username = pygame_gui.elements.UITextEntryLine(rect, self.manager, object_id = id)
        self.txt_username.set_text_length_limit(120)

        y = y + default_height + 20
        rect = pygame.Rect(x,y,label_width,default_height)
        text = "Password : "
        self.lbl_password = pygame_gui.elements.UILabel(rect, text, self.manager)

        rect = pygame.Rect(x + column_space,y,textbox_width,default_height)
        id = "#txt_password"
        self.txt_password = pygame_gui.elements.UITextEntryLine(rect, self.manager, object_id = id)
        self.txt_password.set_text_hidden(is_hidden = True)
        self.txt_password.set_text_length_limit(20)

        button_width = 120
        button_height = 30

        button_y = 450
        x = 350
        rect = pygame.Rect((x,button_y), (button_width, button_height))
        text = "Cancel"
        id = "#btn_cancel"
        self.btn_cancel = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)

        x = x + button_width + 20
        rect = pygame.Rect((x,button_y), (button_width, button_height))
        text = "Login"
        id = "#btn_login"
        self.btn_login = pygame_gui.elements.UIButton(relative_rect=rect, text=text, manager= self.manager, object_id = id)

    
    def on_event(self, event):

        self.manager.process_events(event)

        self.event_controls(event)

        # pygame_gui.UI_BUTTON_PRESSED is the same as pygame.USEREVENT + 1
        if event.type == pygame.USEREVENT + 1:
            if hasattr(event, "ui_element"):
                if event.ui_element == self.btn_login:
                    print("Clicked on Login")
                    username = self.txt_username.get_text()
                    password = self.txt_password.get_text()

                    #TODO : Add Validation
                    print(f'Username:{username} Password:{password}')
                
                    #Got to Character Creation Scene
                    self.fire_goto_event("Character Selection")

                if event.ui_element == self.btn_cancel:
                    print("Clicked on Cancel")

                    #Fire Event Quit
                    self.fire_goto_event(None)

        
        


    def on_loop(self):
        time_delta = pygame.time.Clock().tick()/1000.0
        self.manager.update(time_delta)
        

    def on_render(self, surface):
        surface.fill(self.BACKGROUND)

         #Draw Title on center surface x
        Util().draw_text_center_x(surface, self.title, self.title_font, Colors.BLACK, 15)

        self.render_controls(surface)

        self.manager.draw_ui(surface)

