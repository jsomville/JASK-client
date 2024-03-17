#!/usr/bin/env python3

import pygame

from .login import Login_Scene
from .characterSelection import Character_Selection_Scene
from .station import Station_Scene
from .market import Market_Scene
from .outfitter import Outfitter_Scene
from .map import Map_Scene
from .job import Job_Scene
from .spaceport import Spaceport_Scene
from .space import Space_Scene
from .warp import Warp_Scene
from .die import Die_Scene

class app:
    def __init__(self):
        self.windowWidth = 800
        self.windowHeight = 600
        self.FPS = 60

        self.scenes = dict()
        self.active_scene = None

        self.title = "JASK - Client"

    
    def on_init(self):

        #pygame initialisation
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.frame_per_sec = pygame.time.Clock()

        #Set the window caption
        pygame.display.set_caption(self.title)

        self.SCREEN_SIZE = (self.windowWidth, self.windowHeight)

        #********
        # Declare scenes
        login_scene = Login_Scene()
        self.add_scene(login_scene)

        character_selection_scene = Character_Selection_Scene()
        self.add_scene(character_selection_scene)

        station_scene = Station_Scene()
        self.add_scene(station_scene)

        market_scene = Market_Scene()
        self.add_scene(market_scene)

        outfitter_scene = Outfitter_Scene()
        self.add_scene(outfitter_scene)

        map_scene = Map_Scene()
        self.add_scene(map_scene)

        job_scene = Job_Scene()
        self.add_scene(job_scene)

        spaceport_scene = Spaceport_Scene()
        self.add_scene(spaceport_scene)

        space_scene = Space_Scene()
        self.add_scene(space_scene)

        warp_scene = Warp_Scene()
        self.add_scene(warp_scene)

        die_scene = Die_Scene()
        self.add_scene(die_scene)

        self.active_scene = self.scenes["Login"]
        #******

        #Enable the control loop 
        self._running = True

    def add_scene(self, aScene):
        aScene.size = self.SCREEN_SIZE
        aScene.on_init()

        self.scenes[aScene.name] = aScene

    def on_event(self, event):
        """Function designed to hanlde events such as user input (keyboard, mouse, etc"""

        #Quit Event
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.USEREVENT:
            #Switch scene event
            if "goto" in event.__dict__:
                # Scene on_event

                next_scene = event.__dict__["goto"]
                if next_scene != None:
                    print("Goto : " + event.__dict__["goto"])

                    if next_scene in self.scenes:
                        self.active_scene = self.scenes[event.__dict__["goto"]]
                    else:
                        raise Exception('Scene' + event.__dict__["goto"] + " not found")
                else:
                    print("Next scene is None so quit")
                    self._running = False

        #Force on_event management on active scene
        if self.active_scene != None:
            if self.active_scene.inited:
                self.active_scene.on_event(event)

    
    def on_loop(self):
        """Function to specify the game logic"""

        #Force on_loop on active scene
        if self.active_scene != None:
            self.active_scene.on_loop()

            self.active_scene = self.active_scene.next

            if self.active_scene == None:
                self._running = False

    def on_render(self):
        """Function specialized for surface rendering only"""

        #Force on_render on active scene
        if self.active_scene != None:
            self.active_scene.on_render(self._display_surf)

        #Refresh Surface
        rect = self._display_surf.get_rect()
        pygame.display.update(rect)

    def on_cleanup(self):
        """Function to handle app uninitialized"""
        print("Application Cleanup")
        pygame.quit()

    def on_execute(self):
        """Main Execute function and main loop, calls on_init, on_event, on_loop, on_logic  """
        
        #Init application and load scenes
        self.on_init()

        #Main Loop
        while (self._running):
            #Handle Events
            for event in pygame.event.get():
                self.on_event(event)

            #Game Logic
            self.on_loop()

            #Render code
            self.on_render()

            #Ensure FPS is respected (try at least)
            self.frame_per_sec.tick(self.FPS)
        
        #On cleanup
        self.on_cleanup()


