import pygame
import numpy as np
import sys
import random
import Utils
from Utils import Planet  
from Utils import SimScreen
from Utils import LaunchScreen

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

display = pygame.display.set_mode((1080,720))

n = 0

launchScreen = LaunchScreen()
launchScreen.DrawMenu()
running =  True

launch = True
solar = False
Sandbox = False

#Launch Window
while running and launch:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print("1 Pressed")
                #Load Solar System
                solar = True
                launch = False
                simulation = SimScreen()
                simulation.LoadSolarSystem()
            if event.key == pygame.K_2:
                print("2 Pressed")#
                Sandbox = True
                launch = False
                simulation = SimScreen()
                simulation.LoadSandbox()

    
    display.blit(launchScreen.screen, (0,0))

    pygame.display.flip()

    dt = clock.tick(30) / 1000  # limits FPS to 60

while running and solar:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        #TRACKING BODIES
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print("1 pressed!")
                simulation.tracking = True
                simulation.tracked_body = simulation.bodies[0]
                simulation.Pixels_per_metre = 100 / (1.496e+11*0.5)
            if event.key == pygame.K_2:
                print("2 pressed!")
                simulation.tracking = True
                simulation.tracked_body = simulation.bodies[1]
                simulation.Pixels_per_metre = 300 / 400000e3
            if event.key == pygame.K_3:
                print("2 pressed!")
                simulation.tracking = True
                simulation.tracked_body = simulation.bodies[2]
                simulation.Pixels_per_metre = 300 / 400000e3
            if event.key == pygame.K_4:
                print("2 pressed!")
                simulation.tracking = True
                simulation.tracked_body = simulation.bodies[3]
                simulation.Pixels_per_metre = 300 / 400000e3
            if event.key == pygame.K_5:
                print("2 pressed!")
                simulation.tracking = True
                simulation.tracked_body = simulation.bodies[4]
                simulation.Pixels_per_metre = 250 / 400000e3
            if event.key == pygame.K_6:
                print("6 pressed!")
                simulation.tracking = True
                simulation.tracked_body = simulation.bodies[5]
                simulation.Pixels_per_metre = 250 / 400000e3
            if event.key == pygame.K_7:
                print("6 pressed!")
                simulation.tracking = True
                simulation.tracked_body = simulation.bodies[6]
                simulation.Pixels_per_metre = 250 / 400000e3
            if event.key == pygame.K_8:
                print("6 pressed!")
                simulation.tracking = True
                simulation.tracked_body = simulation.bodies[7]
                simulation.Pixels_per_metre = 250 / 400000e3
        # Panning Enviroment    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                simulation.dragging = True
                simulation.tracking = False
                last_mouse_pos = pygame.Vector2(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                simulation.dragging = False
        elif event.type == pygame.MOUSEMOTION and simulation.dragging:
            mouse_pos = pygame.Vector2(event.pos)
            delta = mouse_pos - last_mouse_pos
            simulation.Pan(delta.x, delta.y)
            last_mouse_pos = mouse_pos
        #Zooming
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:   # scroll up
                simulation.Pixels_per_metre *= 1.1
            elif event.button == 5: # scroll down
                simulation.Pixels_per_metre /= 1.1

    Utils.UpdatePositions(dt, simulation.bodies)

    if simulation.tracking:
        simulation.Track(simulation.tracked_body)
    
    simulation.Draw(simulation.bodies)
    display.blit(simulation.screen, (0,0))

    pygame.display.flip()

    dt = clock.tick(100000) / 1000  # limits FPS to 60
    dt = 1/24*24*60*60
    n += 1



dt = 24*60*60*10
while running and Sandbox:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        #TRACKING BODIES
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print("1 pressed!")
                simulation.tracking = True
                simulation.tracked_body = simulation.bodies[0]
                simulation.Pixels_per_metre = 100 / (1.496e+11*0.5)
            if event.key == pygame.K_RETURN:
                print("1 pressed!")
                simulation.AddRandomBody()
           
        # Panning Enviroment    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                simulation.dragging = True
                simulation.tracking = False
                last_mouse_pos = pygame.Vector2(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                simulation.dragging = False
        elif event.type == pygame.MOUSEMOTION and simulation.dragging:
            mouse_pos = pygame.Vector2(event.pos)
            delta = mouse_pos - last_mouse_pos
            simulation.Pan(delta.x, delta.y)
            last_mouse_pos = mouse_pos
        #Zooming
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:   # scroll up
                simulation.Pixels_per_metre *= 1.1
            elif event.button == 5: # scroll down
                simulation.Pixels_per_metre /= 1.1

    Utils.UpdatePositions(dt, simulation.bodies)
    simulation.CheckCollison()
    
    if simulation.tracking:
        simulation.Track(simulation.tracked_body)
    
    simulation.Draw(simulation.bodies)
    display.blit(simulation.screen, (0,0))

    pygame.display.flip()

    dt = clock.tick(30) / 1000  # limits FPS to 60
    dt = 3/24*24*60*60
    n += 1

