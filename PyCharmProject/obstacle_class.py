import random

from pico2d import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 1000

class Obstacle1:
    image = None

    def __init__(self):
        self.x, self.y = random.randint(0 + 64, CANVAS_WIDTH - 64), random.randint(CANVAS_HEIGHT -30, CANVAS_HEIGHT)
        if Obstacle1.image == None:
            Obstacle1.image = load_image('Resource/Etc/obstacle1.png')

        self.collisionX1 = [0]
        self.collisionY1= [0]
        self.collisionX2 = [0]
        self.collisionY2= [0]

    def update(self, frame_time):
        if self.y > 0 :
            self.y = self.y - 20
        else:
            self.x, self.y = random.randint(0 + 64, CANVAS_WIDTH - 64), random.randint(CANVAS_HEIGHT -30, CANVAS_HEIGHT)

    def draw(self):
         self.image.clip_draw(0, 0, 86, 135, self.x, self.y)

    def showArea(self):
        self.collisionX1[0] = (self.x) - 40
        self.collisionY1[0] = (self.y-25) + 40
        self.collisionX2[0] = (self.x) + 40
        self.collisionY2[0] = (self.y-25) - 40

        draw_rectangle(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])