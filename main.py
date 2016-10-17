import pygame
import math
import random
import map
import camera
from entity import Player
from MapManager import Map_Manager


pygame.init()
width,height=640,480
win=pygame.display.set_mode((width,height))
clk=pygame.time.Clock()
cam=camera.camera(width,height,800,450)
Map_Manager=Map_Manager("test.tmx",cam)
while True:
    #events
    elapsed=clk.tick()/1000
    evt=pygame.event.poll()
    keys = pygame.key.get_pressed()
    if evt.type==pygame.QUIT:
        break;
    else:
        Map_Manager.events(evt,keys)
    # #update
    Map_Manager.update(elapsed)
    #rendering
    win.fill((0,0,0))
    Map_Manager.draw(win)
    pygame.display.flip()
pygame.quit()
