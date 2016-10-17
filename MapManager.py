import pygame
import math
import random
import entity
import map
import camera

class Map_Manager:
    def __init__(self,map_name,camera):
        self.next=""
        self.current_maps=[]
        self.name_list=[]
        self.current_map=0
        while self.next!=None:
            self.current_maps.append(map.map(map_name))
            self.name_list.append(map_name)
            self.next=self.current_maps[-1].get_next_map()
            map_name=self.next
        spawn=self.current_maps[self.current_map].get_p_spawn()
        self.player=entity.Player(spawn[0],spawn[1],32,32)
        self.current_map=0
        self.camera=camera
        self.camera.cam_max_x=self.current_maps[self.current_map].map_width()
        self.camera.cam_max_y=self.current_maps[self.current_map].map_height()
    def change_map(self):
        self.current_map+=1
        spawn=self.current_maps[self.current_map].get_p_spawn()
        self.player.reset_spawn(spawn[0],spawn[1])
        self.camera.cam_max_x=self.current_maps[self.current_map].map_width()
        self.camera.cam_max_y=self.current_maps[self.current_map].map_height()
    def events(self,event,keys):
        self.player.dx=0
        self.player.apply_force(0,120)
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and self.player.movement==entity.movement.nothing:
                self.player.dy=-150
                self.player.movement=entity.movement.jumping
            if event.key==pygame.K_s and not self.player.movement==entity.movement.jumping:
                self.player.down=True
            if event.key==pygame.K_r:
                spawn=self.current_maps[self.current_map].get_p_spawn()
                self.player.x=spawn[0]
                self.player.y=spawn[1]
                self.player.dx=0
                self.player.dy=0
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_s and self.player.down:
                self.player.down=False
        if keys[pygame.K_d]:
            self.player.dx=150
        if keys[pygame.K_a]:
            self.player.dx=-150
        if self.player.dy==0:
            self.player.movement=entity.movement.nothing
    def update(self,elapsed):
        self.player.apply_force(0,120)
        self.current_maps[self.current_map].collisions(elapsed,self.player,self.camera.x,self.camera.y)
        self.player.update(elapsed)
        self.camera.update(self.player,elapsed)
        self.current_maps[self.current_map].update(elapsed)
        if self.current_maps[self.current_map].done:
            self.change_map()
    def draw(self,window):
        self.current_maps[self.current_map].draw(window,self.camera)
        self.player.draw(window,self.camera.x,self.camera.y)