

class Animation():
    def __init__(self,sheet,divisions,static_form):
        self.frames=[]
        x_size=sheet.get_width()/divisions
        for num in range(0,divisions):
            self.frames.append(sheet.subsurface(num*x_size,0,x_size,sheet.get_height()))
        self.frame=0
        self.fps=20
        self.spf=1/self.fps
        self.currentFrame=0
        self.paused=False
        self.static=static_form
    def update(self,elapsed):
        if not self.paused and not self.static:
            self.spf-=elapsed
            if self.spf<0:
                self.currentFrame+=1
                self.spf=1/self.fps
                if self.currentFrame>=len(self.frames):
                    self.currentFrame=0
    def current_frame(self):
        return self.frames[self.currentFrame]
    def pause(self):
        paused=True
    def unpause(self):
        paused=False
    def reset(self):
        self.spf=1/self.fps
        self.currentFrame=0