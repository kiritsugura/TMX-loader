
import pygame
from entity import Player
from entity import movement
import base64
import zlib
import struct
import camera
#Class the represents a tilemap.
class map():
    """
    Constructor,
    :param(fname): the name of the file as represented by a string.
    """
    def __init__(self,fname):
        self.file=fname
        self.name=[]
        self.dx=0
        self.dy=0
        self.x=0
        self.y=0
        self.tiles=None
        self.walls=[]
        self.next=None
        self.next_map=None
        self.done=False
        self.get_file()
    """
        Loads a tilemap text file into memory.
    """
    def get_file(self):
        file=open(self.file,"r")
        if file != None:
            header,rest=[],[]
            for line in file:
                if header !=None:
                    header.append(line)
                    if line.find("</tileset>")==1:
                        self.xml_header(header)
                        header=None
                else:
                    rest.append(line)
            self.load_data(rest)
        file.close()
    def load_data(self,rest) :
        index=0
        items=[]
        objects=[]
        self.tiles=[]
        for x in range(0,self.width):
            self.tiles.append([])
            for y in range(0,self.height):
                self.tiles[x].append((0,0))
        while(len(rest)>index+1):
            if rest[index].find("<layer name=")>0:
                strings=base64.b64decode(rest[index+2])
                data=zlib.decompress(strings)
                fmt=struct.Struct('<L')
                x=0
                y=0
                for byte in range(0,len(data),4):
                    tile=(fmt.unpack(data[byte:byte+4])[0])
                    if tile!=0:
                        width=tile%self.cols-1
                        height=tile//self.cols
                        image=self.textures.subsurface((width*(self.tilewidth+self.x_gap),height*(self.tileheight+self.y_gap),self.tilewidth,self.tileheight))
                        self.tiles[x][y]=(image,x,y)
                    x+=1
                    if x==self.width:
                        y+=1
                        x=0
                index+=5
            elif(rest[index].find("<objectgroup name")>0):
                index+=1
                while rest[index].find("object id=")>0:
                    object=rest[index].split(" ")
                    id=int(object[3][4:-1])
                    name=object[4][6:-1]
                    type=object[5][6:-1]
                    xpos=int(object[6][3:-1])
                    ypos=int(object[7][3:-1])
                    width=int(object[8][7:-1])
                    height=int(object[9][8:-4])
                    objects.append((id,name,type,xpos,ypos,width,height))
                    index+=1
                index+=1
        self.create_objects(objects)
    def create_objects(self,objs):
        for obj in objs:
            if obj[2]=="collision":
                self.walls.append([obj[3],obj[4],obj[5],obj[6]])
            if obj[2]=="spawn":
                self.p_spawn=[obj[3],obj[4]]
            if obj[2]=="portal":
                self.next_map=obj[1]+".tmx"
                self.next=[obj[3],obj[4],obj[5],obj[6]]
    def get_next(self):
        print(self.next)
        if len(self.next)<1:
            return None
        return self.next
    def get_next_map(self):
        print(self.next_map)
        if self.next==None:
            return None
        return self.next_map
    def get_p_spawn(self):
        return self.p_spawn
    def xml_header(self,header):
        info=header[1].split(" ")
        self.width=int(info[4][7:-1])
        self.height=int(info[5][8:-1])
        self.tilewidth=int(info[6][11:-1])
        self.tileheight=int(info[7][12:-1])
        info=header[2].split(" ")
        self.textures=pygame.image.load(info[3][6:-1]+'.png')
        self.tilewidth=int(info[4][11:-1])
        self.tileheight=int(info[5][12:-1])
        if info[6].find("spacing")>=0:
            self.x_gap=int(info[6][9:-1])
            self.y_gap=self.x_gap
        else:
            self.x_gap=0
            self.y_gap=0
        self.tile_count=int(info[7][12:-1])
        self.cols=int(info[8][9:-3])
    """
    Updates the map with the current velocity with respect to time.
    :param(elapsed):the time elapsed since the last frame.
    """
    def update(self,elapsed):
        self.x+=elapsed*self.dx
        self.y+=elapsed*self.dy
    """
    Render function that renders the current tilemap to the screen.
    :param(win): the surface that the tiles will be blit onto.
    """
    def draw(self,win,camera):
        start_x=int(camera.x//self.tilewidth-1)
        start_y=int(camera.y//self.tileheight-1)
        end_x=int(camera.x//self.tilewidth+camera.width//self.tilewidth+1)
        end_y=int(camera.y//self.tileheight+camera.height//self.tileheight+1)
        if start_x<0:
            start_x=0
        if start_y<0:
            start_y=0
        if end_x>self.width:
            end_x=self.width
        if end_y>self.height:
            end_y=self.height
        for x_pos in range(start_x,end_x):
            for y_pos in range(start_y,end_y):
                tile=self.tiles[x_pos][y_pos]
                if tile[0]!=0:
                    win.blit(tile[0],(tile[1]*self.tilewidth-camera.x,tile[2]*self.tileheight-camera.y))
        for wall in self.walls:
            pygame.draw.rect(win,(123,0,0),(wall[0]-camera.x,wall[1]-camera.y,wall[2],wall[3]),2)
    def map_width(self):
        return self.width*self.tilewidth
    def map_height(self):
        return self.height*self.tileheight
    """
    Determines collisions between the player and the landscape.
    :param(player): the player that represents the user.
    """
    def collisions(self,elapsed,player,cam_x,cam_y):
        for wall in self.walls:
            nums=self.cor(wall,player,cam_x,cam_y,elapsed)
            if nums[0]!=0:
                for num in nums:
                    if num==-1:
                        player.y=wall[1]+wall[3]
                        player.dy=0
                        player.acceleration[1]=0
                    elif num==-2:
                        player.x=wall[0]+wall[2]
                        player.dx=0
                        player.acceleration[0]=0
                    elif num==1:
                        player.y=wall[1]-player.height
                        player.dy=0
                        player.acceleration[1]=0
                    elif num==2:
                        player.x=wall[0]-player.width
                        player.dx=0
                        player.acceleration[0]=0
            elif nums[0]==0 and player.dy>1:
                player.movement=movement.falling
        if self.next!=None:
            nums=self.cor(self.next,player,cam_x,cam_y,elapsed)
            if nums[0]!=0:
                self.done=True
    """
    rectangle in the form of [x,y,width,height], all tiles are assumed to be the same size.
    """
    def cor(self,rect,player,off_x,off_y,elapsed):
        nums=[]
        if self.rect_coll((rect[0]-off_x,rect[1]-off_y,rect[2],rect[3]),(((player.x+player.dx*elapsed)+player.width//2)-off_x,(player.y+player.dy*elapsed)-off_y)):
            nums.append(-1)
        if self.rect_coll((rect[0]-off_x,rect[1]-off_y,rect[2],rect[3]),((player.x+player.dx*elapsed)+player.width//2-off_x,(player.y+player.dy*elapsed)+player.height-off_y)):
            nums.append(1)
        if self.rect_coll((rect[0]-off_x,rect[1]-off_y,rect[2],rect[3]),((player.x+player.dx*elapsed)-off_x,(player.y+player.dy*elapsed)+player.height//2-off_y)):
            nums.append(-2)
        if self.rect_coll((rect[0]-off_x,rect[1]-off_y,rect[2],rect[3]),((player.x+player.dx*elapsed)+player.width-off_x,(player.y+player.dy*elapsed)+player.height//2-off_y)):
            nums.append(2)
        if len(nums)==0:
            nums.append(0)
        return nums
    """
    A rectangle contains on a specific point.
    :param(rect1): A reactangle[x,y,width,height] that represents a box.
    :param(point): A point[x,y] that represents an edge of the player sprite.
    """
    def rect_coll(self,rect1,point):
        return rect1[0]<point[0] and rect1[0]+rect1[2]>point[0] and rect1[1]<point[1] and rect1[1]+rect1[3]>point[1]
