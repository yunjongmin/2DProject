import random

from pico2d import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 1000

PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

COLLISION_AREA_1 = 1

class Obstacle:
    FLY_SPEED_KMPH = 25.0                    # Km / Hour
    FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
    FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
    FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

    image = None
    collision_area_count = COLLISION_AREA_1

    def __init__(self):
        self.x, self.y = random.randint(0 + 64, CANVAS_WIDTH - 64), random.randint(CANVAS_HEIGHT, CANVAS_HEIGHT+CANVAS_HEIGHT/2)
        if Obstacle.image == None:
            Obstacle.image = load_image('Resource/Etc/obstacle1.png')

        self.collisionX1 = [0]
        self.collisionY1= [0]
        self.collisionX2 = [0]
        self.collisionY2= [0]
        self.collisionChecks= [0]

        self.collisionCheck = False

        self.life_time = 0.0
        self.total_frames = 0.0

    def setShowCheck(self, showCheck):
        self.showCheck = showCheck

    def update(self, frame_time):
        self.life_time += frame_time
        distance = Obstacle.FLY_SPEED_PPS * frame_time
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 3

        if self.y > 0 :
            self.y = self.y - distance
        else:
            self.x, self.y = random.randint(0 + 64, CANVAS_WIDTH - 64), random.randint(CANVAS_HEIGHT, CANVAS_HEIGHT+CANVAS_HEIGHT/2)

    def draw(self):
         self.image.clip_draw(0, 0, 86, 135, self.x, self.y)

    def showArea(self, showCheck):
        self.showCheck = showCheck
        self.collisionX1[0] = (self.x) - 40
        self.collisionY1[0] = (self.y-25) - 40
        self.collisionX2[0] = (self.x) + 40
        self.collisionY2[0] = (self.y-25) + 40

        # if self.collisionChecks[0] == True:
        #     draw_rectangle_green(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
        # else :
        #     draw_rectangle_red(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
        if self.showCheck == True:
            draw_rectangle(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])

    def get_bb(self, index):
        return self.collisionX1[index], self.collisionY1[index], self.collisionX2[index], self.collisionY2[index]

    def set_collisionCheck(self, index, value, change):
        if change == True:
            self.collisionChecks[index] = value
        elif self.collisionChecks[index] == False:
            self.collisionChecks[index] = value

    def newCreateObstacle(self):
        self.x, self.y = random.randint(0 + 64, CANVAS_WIDTH - 64), random.randint(CANVAS_HEIGHT, CANVAS_HEIGHT+CANVAS_HEIGHT/2)
