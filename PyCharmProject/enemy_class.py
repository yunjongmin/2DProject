import random

from pico2d import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 1000
COLLISION_AREA_3 = 3
MISSILE_MAX = 100
MONSTER_BLUE = 1
MONSTER_PINK = 2
MONSTER_MISSILE_POWER_1 = 0
MONSTER_MISSILE_POWER_2 = 1
MID_MONSTER_LIMIT_MOVE = 100

PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Monster:
    FLY_SPEED_KMPH = 10.0                    # Km / Hour
    FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
    FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
    FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

    MISSILE_SPEED_KMPH = 20.0                    # Km / Hour
    MISSILE_SPEED_MPM = (MISSILE_SPEED_KMPH * 1000.0 / 60.0)
    MISSILE_SPEED_MPS = (MISSILE_SPEED_MPM / 60.0)
    MISSILE_SPEED_PPS = (MISSILE_SPEED_MPS * PIXEL_PER_METER)

    image_blue = None
    image_pink = None
    image_missile = None
    collision_area_count = COLLISION_AREA_3

    def __init__(self):
        # 몬스터 관련 변수
        self.x, self.y = random.randint(0 + 64, CANVAS_WIDTH - 64), random.randint(CANVAS_HEIGHT -30, CANVAS_HEIGHT)
        self.frame = random.randint(0, 3)
        self.flag = random.randint(MONSTER_BLUE, MONSTER_PINK)
        if Monster.image_blue == None:
            Monster.image_blue = load_image('Resource/Monster/monster_blue.png')
        if Monster.image_pink == None:
            Monster.image_pink = load_image('Resource/Monster/monster_pink.png')

        self.collisionX1 = [0]*COLLISION_AREA_3
        self.collisionY1= [0]*COLLISION_AREA_3
        self.collisionX2 = [0]*COLLISION_AREA_3
        self.collisionY2= [0]*COLLISION_AREA_3
        self.collisionChecks= [0]*COLLISION_AREA_3

        for self.collisionCheck in self.collisionChecks:
            self.collisionCheck = False

        # 미사일 관련 변수
        self.missile_frame = MONSTER_MISSILE_POWER_1
        self.missile_x = [0]*MISSILE_MAX
        self.missile_y= [0]*MISSILE_MAX
        self.missile_show= [0]*MISSILE_MAX

        if Monster.image_missile == None:
            Monster.image_missile = load_image('Resource/Missile/monster_missile.png')

        self.missile_collisionX1 = [0]*MISSILE_MAX
        self.missile_collisionY1= [0]*MISSILE_MAX
        self.missile_collisionX2 = [0]*MISSILE_MAX
        self.missile_collisionY2= [0]*MISSILE_MAX

        self.life_time = 0.0
        self.total_frames = 0.0

    def update(self, frame_time):
        # 몬스터
        self.life_time += frame_time
        distance = Monster.FLY_SPEED_PPS * frame_time
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 3
        # self.frame = (self.frame + 1) % 3
        if self.y > 0 :
            self.y = self.y - distance
        else:
            self.x, self.y = random.randint(0 + 64, CANVAS_WIDTH - 64), CANVAS_HEIGHT

        self.showMissile(self.x, self.y)

        # 미사일
        self.life_time += frame_time
        distance = Monster.MISSILE_SPEED_PPS * frame_time
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        i = 0
        while(i < MISSILE_MAX):
            if self.missile_show[i] == True:
                if self.missile_y[i] > 0:
                    self.missile_y[i] -= distance
                else:
                    self.missile_show[i] = False
            i += 1

    def draw(self):
        # 몬스터
        if self.flag == MONSTER_BLUE:
            self.image_blue.clip_draw(self.frame * 64, 0, 64, 64, self.x, self.y)
        elif self.flag == MONSTER_PINK:
            self.image_pink.clip_draw(self.frame * 64, 0, 64, 64, self.x, self.y)

        # 미사일
        i = 0
        while(i < MISSILE_MAX):
            if self.missile_show[i] == True:
                self.image_missile.clip_draw(self.missile_frame * 15, 0, 15, 9, self.missile_x[i] - 2, self.missile_y[i] - 30)
            i += 1

    def showArea(self):
        # 몬스터
        self.collisionX1[0] = (self.x) - 10
        self.collisionY1[0] = (self.y-4) - 22
        self.collisionX2[0] = (self.x) + 10
        self.collisionY2[0] = (self.y-4) + 22
        self.collisionX1[1] = (self.x-18) - 7
        self.collisionY1[1] = (self.y) - 7
        self.collisionX2[1] = (self.x-18) + 7
        self.collisionY2[1] = (self.y) + 7
        self.collisionX1[2] = (self.x+18) - 7
        self.collisionY1[2] = (self.y) - 7
        self.collisionX2[2] = (self.x+18) + 7
        self.collisionY2[2] = (self.y) + 7

        # draw_rectangle(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
        # draw_rectangle(self.collisionX1[1],self.collisionY1[1],self.collisionX2[1],self.collisionY2[1])
        # draw_rectangle(self.collisionX1[2],self.collisionY1[2],self.collisionX2[2],self.collisionY2[2])

        if self.collisionChecks[0] == True:
            draw_rectangle_green(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
        else :
            draw_rectangle_red(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])

        if self.collisionChecks[1] == True:
            draw_rectangle_green(self.collisionX1[1],self.collisionY1[1],self.collisionX2[1],self.collisionY2[1])
        else:
            draw_rectangle_red(self.collisionX1[1],self.collisionY1[1],self.collisionX2[1],self.collisionY2[1])

        if self.collisionChecks[2] == True:
            draw_rectangle_green(self.collisionX1[2],self.collisionY1[2],self.collisionX2[2],self.collisionY2[2])
        else:
            draw_rectangle_red(self.collisionX1[2],self.collisionY1[2],self.collisionX2[2],self.collisionY2[2])


        # 미사일
        i = 0
        while(i < MISSILE_MAX):
            if self.missile_show[i] == True:
                self.missile_collisionX1[i] = (self.missile_x[i]-3) - 2
                self.missile_collisionY1[i] = (self.missile_y[i]-30) + 2
                self.missile_collisionX2[i] = (self.missile_x[i]-3) + 2
                self.missile_collisionY2[i] = (self.missile_y[i]-30) - 2

                draw_rectangle(self.missile_collisionX1[i],self.missile_collisionY1[i],self.missile_collisionX2[i],self.missile_collisionY2[i])
            i += 1

    def showMissile(self, showX, showY):
        i = 0
        while(i < MISSILE_MAX):
            self.checkInt = random.randint(0, 10000)
            if self.checkInt > 9995:
                if self.missile_show[i] == False:
                    self.missile_show[i] = True
                    self.missile_x[i] = showX
                    self.missile_y[i] = showY
                    break
            i += 1

    def get_bb(self, index):
        return self.collisionX1[index], self.collisionY1[index], self.collisionX2[index], self.collisionY2[index]

    def set_collisionCheck(self, index, value, change):
        if change == True:
            self.collisionChecks[index] = value
        elif self.collisionChecks[index] == False:
            self.collisionChecks[index] = value


class MidMonster:
    FLY_SPEED_KMPH = 13.0                    # Km / Hour
    FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
    FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
    FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

    MISSILE_SPEED_KMPH = 24.0                    # Km / Hour
    MISSILE_SPEED_MPM = (MISSILE_SPEED_KMPH * 1000.0 / 60.0)
    MISSILE_SPEED_MPS = (MISSILE_SPEED_MPM / 60.0)
    MISSILE_SPEED_PPS = (MISSILE_SPEED_MPS * PIXEL_PER_METER)

    image_red = None
    image_missile = None

    collision_area_count = COLLISION_AREA_3

    def __init__(self):
        # 몬스터 관련 변수
        self.x, self.y = random.randint(0 + 64, CANVAS_WIDTH - 64), random.randint(CANVAS_HEIGHT - 30, CANVAS_HEIGHT)
        self.frame = random.randint(0, 3)
        if random.randint(0, 1) == 0 :
            self.rightMove = True
        else:
            self.rightMove = False
        self.limitMove = MID_MONSTER_LIMIT_MOVE
        self.moveX = random.randint(0, 50)
        if MidMonster.image_red == None:
            MidMonster.image_red = load_image('Resource/Monster/mid_boss_red.png')

        self.collisionX1 = [0]*COLLISION_AREA_3
        self.collisionY1= [0]*COLLISION_AREA_3
        self.collisionX2 = [0]*COLLISION_AREA_3
        self.collisionY2= [0]*COLLISION_AREA_3
        self.collisionChecks= [0]*COLLISION_AREA_3

        for self.collisionCheck in self.collisionChecks:
            self.collisionCheck = False

        # 미사일 관련 변수
        self.missile_frame = MONSTER_MISSILE_POWER_2
        self.missile_x = [0]*MISSILE_MAX
        self.missile_y= [0]*MISSILE_MAX
        self.missile_show= [0]*MISSILE_MAX

        if MidMonster.image_missile == None:
            MidMonster.image_missile = load_image('Resource/Missile/monster_missile.png')

        self.missile_collisionX1 = [0]*MISSILE_MAX
        self.missile_collisionY1= [0]*MISSILE_MAX
        self.missile_collisionX2 = [0]*MISSILE_MAX
        self.missile_collisionY2= [0]*MISSILE_MAX

        self.life_time = 0.0
        self.total_frames = 0.0

    def update(self, frame_time):
        # 몬스터
        self.life_time += frame_time
        distance = MidMonster.FLY_SPEED_PPS * frame_time
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 3
        # self.frame = (self.frame + 1) % 3
        if self.y > 0 :
            if self.rightMove == True:
                self.x = self.x + distance
                self.moveX = self.moveX + distance
                if self.moveX > self.limitMove:
                    self.rightMove = False
                    self.moveX = 0
                elif self.x > CANVAS_WIDTH:
                    self.rightMove = False
                    self.moveX = 0
            else:
                self.x = self.x - distance
                self.moveX = self.moveX + distance
                if self.moveX > self.limitMove:
                    self.rightMove = True
                    self.moveX = 0
                elif self.x < 0:
                    self.rightMove = True
                    self.moveX = 0
            self.y = self.y - distance
        else:
            self.x, self.y = random.randint(0 + 64, CANVAS_WIDTH - 64), CANVAS_HEIGHT

        # 미사일
        self.life_time += frame_time
        distance = MidMonster.MISSILE_SPEED_PPS * frame_time
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        i = 0
        while(i < MISSILE_MAX):
            if self.missile_show[i] == True:
                if self.missile_y[i] > 0:
                    self.missile_y[i] -= distance
                else:
                    self.missile_show[i] = False
            i += 1


        self.showMissile(self.x, self.y)

    def draw(self):
        # 몬스터
        self.image_red.clip_draw(self.frame * 170, 0, 170, 128, self.x, self.y)

        # 미사일
        i = 0
        while(i < MISSILE_MAX):
            if self.missile_show[i] == True:
                self.image_missile.clip_draw(self.missile_frame * 15, 0, 15, 9, self.missile_x[i] - 2, self.missile_y[i] - 30)
            i += 1

    def showArea(self):
        # 몬스터
        self.collisionX1[0] = (self.x) - 35
        self.collisionY1[0] = (self.y) - 60
        self.collisionX2[0] = (self.x) + 35
        self.collisionY2[0] = (self.y) + 60
        self.collisionX1[1] = (self.x-54) - 18
        self.collisionY1[1] = (self.y) - 20
        self.collisionX2[1] = (self.x-54) + 18
        self.collisionY2[1] = (self.y) + 20
        self.collisionX1[2] = (self.x+54) - 18
        self.collisionY1[2] = (self.y) - 20
        self.collisionX2[2] = (self.x+54) + 18
        self.collisionY2[2] = (self.y) + 20
        # draw_rectangle(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
        # draw_rectangle(self.collisionX1[1],self.collisionY1[1],self.collisionX2[1],self.collisionY2[1])
        # draw_rectangle(self.collisionX1[2],self.collisionY1[2],self.collisionX2[2],self.collisionY2[2])
        if self.collisionChecks[0] == True:
            draw_rectangle_green(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
        else :
            draw_rectangle_red(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])

        if self.collisionChecks[1] == True:
            draw_rectangle_green(self.collisionX1[1],self.collisionY1[1],self.collisionX2[1],self.collisionY2[1])
        else:
            draw_rectangle_red(self.collisionX1[1],self.collisionY1[1],self.collisionX2[1],self.collisionY2[1])

        if self.collisionChecks[2] == True:
            draw_rectangle_green(self.collisionX1[2],self.collisionY1[2],self.collisionX2[2],self.collisionY2[2])
        else:
            draw_rectangle_red(self.collisionX1[2],self.collisionY1[2],self.collisionX2[2],self.collisionY2[2])


        # 미사일
        i = 0
        while(i < MISSILE_MAX):
            if self.missile_show[i] == True:
                self.missile_collisionX1[i] = (self.missile_x[i]-3) - 4
                self.missile_collisionY1[i] = (self.missile_y[i]-30) + 4
                self.missile_collisionX2[i] = (self.missile_x[i]-3) + 4
                self.missile_collisionY2[i] = (self.missile_y[i]-30) - 4

                draw_rectangle(self.missile_collisionX1[i],self.missile_collisionY1[i],self.missile_collisionX2[i],self.missile_collisionY2[i])
            i += 1

    def showMissile(self, showX, showY):
        i = 0
        while(i < MISSILE_MAX):
            self.checkInt = random.randint(0, 10000)
            if self.checkInt > 9995:
                if self.missile_show[i] == False:
                    self.missile_show[i] = True
                    self.missile_x[i] = showX
                    self.missile_y[i] = showY
                    break
            i += 1
