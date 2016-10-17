import pygame
import enum
from Animation import Animation

"""
General Entity that has an x,y and respective velocities associated with it.
"""
class Sprite():
    """
    Constructor
    :param(x): the x coordinate.
    :param(y): the y coordinate.
    """
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.dx=0
        self.dy=0
class direction(enum.Enum):
    forward=1
    backward=2
class movement(enum.Enum):
    nothing=0
    jumping=1
    falling=2
"""
A player object that is controlled by the user.
"""
class Player(Sprite):
    """
    Constructor
    :param(x): the x coordinate.
    :param(y): the y coordinate.
    :param(w): the width of the player sprite
    :param(h): the height of the player sprite.
    """
    def __init__(self,x,y,w,h):
        self.x=x
        self.y=y
        self.width=w
        self.height=h
        self.dx=0
        self.dy=0
        image=pygame.image.load("smwsheet.png").subsurface(0,0,96,32)
        image.set_colorkey(image.get_at((0,0)))
        self.acceleration=[0,0]
        self.previous_direction=direction.forward
        self.down=False
        self.animations=[]
        self.animations.append(Animation(image,3,False))
        image=pygame.image.load("smwsheet.png").subsurface(96,0,64,32)
        image.set_colorkey(image.get_at((0,0)))
        self.animations.append(Animation(image,2,True))
        image=pygame.image.load("smwsheet.png").subsurface(224,0,32,32)
        image.set_colorkey(image.get_at((0,0)))
        self.animations.append(Animation(image,1,True))
        self.active_an=0
        self.movement=movement.nothing
    """
    Draws the player to a surface
    :param(win): the surface that the player will be rendered onto.
    """
    def draw(self,win,cam_x,cam_y):
        image=self.animations[self.active_an].current_frame()
        if self.previous_direction==direction.backward:
            image=pygame.transform.flip(image,True,False)
        win.blit(image,(self.x-cam_x,self.y-cam_y))
        pygame.draw.rect(win,(123,0,0),(self.x-cam_x,self.y-cam_y,self.width,self.height),1)
    """
    Updates the player's x and y position.
    :param(elapsed): the time elapsed since that last frame.
    """
    def apply_force(self,dx,dy):
        self.acceleration[0]=dx
        self.acceleration[1]=dy
    def reset_spawn(self,x,y):
        self.dx=0
        self.dy=0
        self.active_an=0
        self.x=x
        self.y=y
    def update(self,elapsed):
        self.active_an=0
        if self.dy!=0 and self.active_an==0:
            self.animations[self.active_an].reset()
            self.active_an=1
        if self.down:
            self.animations[self.active_an].reset()
            self.active_an=2
        self.animations[self.active_an].update(elapsed)
        if self.dx==0 and self.active_an==0:
            self.animations[self.active_an].reset()
        if self.dy>0 and self.active_an==1:
            self.animations[self.active_an].currentFrame=1
        if self.dy<0 and self.active_an==1:
            self.animations[self.active_an].currentFrame=0
        if self.dx<0:
            self.previous_direction=direction.backward
        elif self.dx>0:
            self.previous_direction=direction.forward
        self.x+=elapsed*self.dx
        self.y+=elapsed*self.dy
        self.dx+=self.acceleration[0]*elapsed
        self.dy+=self.acceleration[1]*elapsed