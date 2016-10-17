

class camera():
    def __init__(self,win_width,win_height,width,height):
        self.x=0
        self.y=0
        self.width=win_width
        self.height=win_height
        self.cam_min_x=0
        self.cam_min_y=0
        self.cam_max_x=width
        self.cam_max_y=height
    def update(self,player,elapsed):
        newx=player.x-self.width//2
        newy=player.y-self.height//2
        if newx<self.cam_min_x:
            self.x=0
        elif newx>self.cam_max_x-self.width:
            self.x=self.cam_max_x-self.width
        else:
            self.x=newx
        if newy<self.cam_min_y and self.cam_max_y>self.height:
            self.y=0
        elif newy>self.cam_max_y-self.height:
            self.y=self.cam_max_y-self.height
        else:
            self.y=newy
        if player.x+player.dx*elapsed<0 and player.dx<0:
            player.x=0
            player.dx=0
        elif player.x+player.width+player.dx*elapsed>self.cam_max_x and player.dx>0:
            player.x=self.cam_max_x-player.width
            player.dx=0
        if player.y+player.dx*elapsed<0 and player.dy<0:
            player.y=0
            player.dy=0
        elif player.y+player.height+player.dy*elapsed>self.cam_max_y and player.dy>0:
            player.y=self.cam_max_y-player.height
            player.dy=0
    def pos(self):
        return [self.x,self.y]
