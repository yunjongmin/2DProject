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

MONSTER_HP_MAX = 3
MID_MONSTER_HP_MAX = 6
BOSS_MONSTER_HP_MAX = 50

PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

EXPLOSION_FRAMES_PER_ACTION = 8


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
    image_explosion = None
    collision_area_count = COLLISION_AREA_3
    missile_collision_area_count = MISSILE_MAX

    dieSound = None

    def __init__(self):
        # 몬스터 관련 변수
        self.x, self.y = random.randint(0 + 64, CANVAS_WIDTH - 64), random.randint(CANVAS_HEIGHT, CANVAS_HEIGHT+CANVAS_HEIGHT/2)
        self.frame = random.randint(0, 3)
        self.flag = random.randint(MONSTER_BLUE, MONSTER_PINK)
        self.hp = MONSTER_HP_MAX
        self.socre = self.hp * 100

        if Monster.image_blue == None:
            Monster.image_blue = load_image('Resource/Monster/monster_blue.png')
        if Monster.image_pink == None:
            Monster.image_pink = load_image('Resource/Monster/monster_pink.png')
        if Monster.dieSound == None:
            Monster.dieSound = load_wav('Resource/Sound/mon_die.wav')
            Monster.dieSound.set_volume(5)

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
        self.missile_collisionChecks= [0]*MISSILE_MAX

        for self.missile_collisionCheck in self.missile_collisionChecks:
            self.missile_collisionCheck = False

        # 폭발 관련 변수
        self.explosion_show = False
        self.explosion_frame = 0

        if Monster.image_explosion == None:
            self.image_explosion = load_image('Resource/Explosion/monster_explosion.png')


        self.life_time = 0.0
        self.total_frames = 0.0

    def setShowCheck(self, showCheck):
        self.showCheck = showCheck

    def newCreateMonster(self):
        self.x, self.y = random.randint(0 + 64, CANVAS_WIDTH - 64), random.randint(CANVAS_HEIGHT, CANVAS_HEIGHT+CANVAS_HEIGHT/2)
        self.frame = random.randint(0, 3)
        self.flag = random.randint(MONSTER_BLUE, MONSTER_PINK)
        self.hp = MONSTER_HP_MAX

    def newCreateMonsterMissile(self, index):
        self.missile_show[index] = False
        self.missile_collisionChecks[index] = False
        self.missile_collisionX1[index] = False
        self.missile_collisionY1[index] = False
        self.missile_collisionX2[index] = False
        self.missile_collisionY2[index] = False


    def update(self, frame_time):
        # 몬스터
        self.life_time += frame_time
        distance = Monster.FLY_SPEED_PPS * frame_time
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames/5) % 3
        # self.frame = (self.frame + 1) % 3
        if self.y > 0 :
            self.y = self.y - distance
        else:
            self.x, self.y = random.randint(0 + 64, CANVAS_WIDTH - 64), random.randint(CANVAS_HEIGHT, CANVAS_HEIGHT+CANVAS_HEIGHT/2)

        self.showMissile(self.x, self.y)

        # 미사일
        # self.life_time += frame_time
        distance = Monster.MISSILE_SPEED_PPS * frame_time
        # self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        i = 0
        while(i < MISSILE_MAX):
            if self.missile_show[i] == True:
                if self.missile_y[i] > 0:
                    self.missile_y[i] -= distance
                else:
                    self.missile_show[i] = False
            i += 1


        # 폭발
        if self.explosion_show == True:
            self.explosion_time += frame_time
            if self.explosion_frame < 5 :
                self.explosion_frame =int(self.explosion_time*5)
            else :
                self.explosion_show = False
                self.explosion_frame = 0


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
                self.image_missile.clip_draw(self.missile_frame * 22, 0, 22, 14, self.missile_x[i] - 2, self.missile_y[i] - 30)
            i += 1

        # 폭발관련
        if self.explosion_show == True:
            self.image_explosion.clip_draw(self.explosion_frame * 38, 0, 38, 46, self.explosion_x, self.explosion_y)


    def showArea(self, showCheck):
        self.showCheck = showCheck
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

        # if self.collisionChecks[0] == True:
        #     draw_rectangle_green(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
        # else :
        #     draw_rectangle_red(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
        #
        # if self.collisionChecks[1] == True:
        #     draw_rectangle_green(self.collisionX1[1],self.collisionY1[1],self.collisionX2[1],self.collisionY2[1])
        # else:
        #     draw_rectangle_red(self.collisionX1[1],self.collisionY1[1],self.collisionX2[1],self.collisionY2[1])
        #
        # if self.collisionChecks[2] == True:
        #     draw_rectangle_green(self.collisionX1[2],self.collisionY1[2],self.collisionX2[2],self.collisionY2[2])
        # else:
        #     draw_rectangle_red(self.collisionX1[2],self.collisionY1[2],self.collisionX2[2],self.collisionY2[2])
        if self.showCheck == True:
            draw_rectangle(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
            draw_rectangle(self.collisionX1[1],self.collisionY1[1],self.collisionX2[1],self.collisionY2[1])
            draw_rectangle(self.collisionX1[2],self.collisionY1[2],self.collisionX2[2],self.collisionY2[2])


        # 미사일
        i = 0
        while(i < MISSILE_MAX):
            if self.missile_show[i] == True:
                self.missile_collisionX1[i] = (self.missile_x[i]-3) - 2
                self.missile_collisionY1[i] = (self.missile_y[i]-30) - 2
                self.missile_collisionX2[i] = (self.missile_x[i]-3) + 2
                self.missile_collisionY2[i] = (self.missile_y[i]-30) + 2

                # if self.missile_collisionChecks[i] == True:
                #     draw_rectangle_green(self.missile_collisionX1[i],self.missile_collisionY1[i],self.missile_collisionX2[i],self.missile_collisionY2[i])
                # else :
                #     draw_rectangle_red(self.missile_collisionX1[i],self.missile_collisionY1[i],self.missile_collisionX2[i],self.missile_collisionY2[i])
                if self.showCheck == True:
                    draw_rectangle(self.missile_collisionX1[i],self.missile_collisionY1[i],self.missile_collisionX2[i],self.missile_collisionY2[i])
            i += 1

    def showMissile(self, showX, showY):
        i = 0
        if showY < CANVAS_HEIGHT:
            while(i < MISSILE_MAX):
                self.checkInt = random.randint(0, 10000)
                if self.checkInt > 9995:
                    if self.missile_show[i] == False:
                        self.missile_show[i] = True
                        self.missile_x[i] = showX
                        self.missile_y[i] = showY
                        break
                i += 1

    def showExplosion(self, showX, showY):
        if self.explosion_show == False:
            self.explosion_show = True
            self.explosion_x = showX
            self.explosion_y = showY
            self.explosion_frame = 0
            self.explosion_time = 0

    def get_bb(self, index):
        return self.collisionX1[index], self.collisionY1[index], self.collisionX2[index], self.collisionY2[index]

    def set_collisionCheck(self, index, value, change):
        if change == True:
            self.collisionChecks[index] = value
        elif self.collisionChecks[index] == False:
            self.collisionChecks[index] = value
            if value == True:
                if self.hp > 1:
                    self.hp -= 1
                else :
                    self.showExplosion(self.x, self.y)
                    self.newCreateMonster()
                    Monster.dieSound.play()

    def get_missile_bb(self, index):
        if self.missile_show[index]:
            return self.missile_collisionX1[index], self.missile_collisionY1[index], self.missile_collisionX2[index], self.missile_collisionY2[index]
        else:
            return -100, -100, -100, -100

    def set_missile_collisionCheck(self, index, value, change):
        if change == True:
            self.missile_collisionChecks[index] = value
        elif self.missile_collisionChecks[index] == False:
            self.missile_collisionChecks[index] = value

    def get_score(self):
        if self.hp < MONSTER_HP_MAX and self.hp > 0:
            return 0
        else:
            return self.socre

    def get_special_score(self):
        return 100

    def get_hp(self):
        return self.hp




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
    image_explosion = None
    dieSound = None

    collision_area_count = COLLISION_AREA_3
    missile_collision_area_count = MISSILE_MAX

    def __init__(self):
        # 몬스터 관련 변수
        self.x, self.y = random.randint(0 + 64, CANVAS_WIDTH - 64), random.randint(CANVAS_HEIGHT, CANVAS_HEIGHT+CANVAS_HEIGHT/2)
        self.frame = random.randint(0, 3)
        if random.randint(0, 1) == 0 :
            self.rightMove = True
        else:
            self.rightMove = False
        self.limitMove = MID_MONSTER_LIMIT_MOVE
        self.moveX = random.randint(0, 50)
        self.hp = MID_MONSTER_HP_MAX
        self.socre = self.hp * 100

        if MidMonster.image_red == None:
            MidMonster.image_red = load_image('Resource/Monster/mid_boss_red.png')
        if MidMonster.dieSound == None:
            MidMonster.dieSound = load_wav('Resource/Sound/mon_die.wav')
            MidMonster.dieSound.set_volume(5)

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
        self.missile_collisionChecks= [0]*MISSILE_MAX

        for self.missile_collisionCheck in self.missile_collisionChecks:
            self.missile_collisionCheck = False

        # 폭발 관련 변수
        self.explosion_show = False
        self.explosion_frame = 0

        if MidMonster.image_explosion == None:
            self.image_explosion = load_image('Resource/Explosion/mid_monster_explosion.png')

        self.life_time = 0.0
        self.total_frames = 0.0

    def setShowCheck(self, showCheck):
        self.showCheck = showCheck

    def newCreateMidMonster(self):
        self.x, self.y = random.randint(0 + 64, CANVAS_WIDTH - 64), random.randint(CANVAS_HEIGHT, CANVAS_HEIGHT+CANVAS_HEIGHT/2)
        self.frame = random.randint(0, 3)
        if random.randint(0, 1) == 0 :
            self.rightMove = True
        else:
            self.rightMove = False
        self.limitMove = MID_MONSTER_LIMIT_MOVE
        self.moveX = random.randint(0, 50)
        self.hp = MID_MONSTER_HP_MAX

    def newCreateMidMonsterMissile(self, index):
        self.missile_show[index] = False
        self.missile_collisionChecks[index] = False
        self.missile_collisionX1[index] = False
        self.missile_collisionY1[index] = False
        self.missile_collisionX2[index] = False
        self.missile_collisionY2[index] = False


    def update(self, frame_time):
        # 몬스터
        self.life_time += frame_time
        distance = MidMonster.FLY_SPEED_PPS * frame_time
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames/5) % 3
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
            self.x, self.y = random.randint(0 + 64, CANVAS_WIDTH - 64), random.randint(CANVAS_HEIGHT, CANVAS_HEIGHT+CANVAS_HEIGHT/2)

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

        # 폭발
        if self.explosion_show == True:
            self.explosion_time += frame_time
            if self.explosion_frame < 5 :
                self.explosion_frame =int(self.explosion_time*5)
            else :
                self.explosion_show = False
                self.explosion_frame = 0

    def draw(self):
        # 몬스터
        self.image_red.clip_draw(self.frame * 170, 0, 170, 128, self.x, self.y)

        # 미사일
        i = 0
        while(i < MISSILE_MAX):
            if self.missile_show[i] == True:
                self.image_missile.clip_draw(self.missile_frame * 22, 0, 22, 14, self.missile_x[i] - 2, self.missile_y[i] - 30)
            i += 1

        # 폭발관련
        if self.explosion_show == True:
            self.image_explosion.clip_draw(self.explosion_frame * 55, 0, 55, 81, self.explosion_x, self.explosion_y)

    def showArea(self, showCheck):
        self.showCheck = showCheck
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
        # if self.collisionChecks[0] == True:
        #     draw_rectangle_green(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
        # else :
        #     draw_rectangle_red(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
        #
        # if self.collisionChecks[1] == True:
        #     draw_rectangle_green(self.collisionX1[1],self.collisionY1[1],self.collisionX2[1],self.collisionY2[1])
        # else:
        #     draw_rectangle_red(self.collisionX1[1],self.collisionY1[1],self.collisionX2[1],self.collisionY2[1])
        #
        # if self.collisionChecks[2] == True:
        #     draw_rectangle_green(self.collisionX1[2],self.collisionY1[2],self.collisionX2[2],self.collisionY2[2])
        # else:
        #     draw_rectangle_red(self.collisionX1[2],self.collisionY1[2],self.collisionX2[2],self.collisionY2[2])
        if self.showCheck == True:
            draw_rectangle(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
            draw_rectangle(self.collisionX1[1],self.collisionY1[1],self.collisionX2[1],self.collisionY2[1])
            draw_rectangle(self.collisionX1[2],self.collisionY1[2],self.collisionX2[2],self.collisionY2[2])


        # 미사일
        i = 0
        while(i < MISSILE_MAX):
            if self.missile_show[i] == True:
                self.missile_collisionX1[i] = (self.missile_x[i]-3) - 4
                self.missile_collisionY1[i] = (self.missile_y[i]-30) + 4
                self.missile_collisionX2[i] = (self.missile_x[i]-3) + 4
                self.missile_collisionY2[i] = (self.missile_y[i]-30) - 4

                # if self.missile_collisionChecks[i] == True:
                #     draw_rectangle_green(self.missile_collisionX1[i],self.missile_collisionY1[i],self.missile_collisionX2[i],self.missile_collisionY2[i])
                # else :
                #     draw_rectangle_red(self.missile_collisionX1[i],self.missile_collisionY1[i],self.missile_collisionX2[i],self.missile_collisionY2[i])
                if self.showCheck == True:
                    draw_rectangle(self.missile_collisionX1[i],self.missile_collisionY1[i],self.missile_collisionX2[i],self.missile_collisionY2[i])

            i += 1

    def showMissile(self, showX, showY):
        i = 0
        if showY < CANVAS_HEIGHT:
            while(i < MISSILE_MAX):
                self.checkInt = random.randint(0, 10000)
                if self.checkInt > 9995:
                    if self.missile_show[i] == False:
                        self.missile_show[i] = True
                        self.missile_x[i] = showX
                        self.missile_y[i] = showY
                        break
                i += 1

    def showExplosion(self, showX, showY):
        if self.explosion_show == False:
            self.explosion_show = True
            self.explosion_x = showX
            self.explosion_y = showY
            self.explosion_frame = 0
            self.explosion_time = 0

    def get_bb(self, index):
        return self.collisionX1[index], self.collisionY1[index], self.collisionX2[index], self.collisionY2[index]

    def set_collisionCheck(self, index, value, change):
        if change == True:
            self.collisionChecks[index] = value
        elif self.collisionChecks[index] == False:
            self.collisionChecks[index] = value
            if value == True:
                if self.hp > 1:
                    self.hp -= 1
                else :
                    self.showExplosion(self.x, self.y)
                    self.newCreateMidMonster()
                    MidMonster.dieSound.play()

    def get_missile_bb(self, index):
        # return self.missile_collisionX1[index], self.missile_collisionY1[index], self.missile_collisionX2[index], self.missile_collisionY2[index]
        if self.missile_show[index]:
            return self.missile_collisionX1[index], self.missile_collisionY1[index], self.missile_collisionX2[index], self.missile_collisionY2[index]
        else:
            return -100, -100, -100, -100

    def set_missile_collisionCheck(self, index, value, change):
        if change == True:
            self.missile_collisionChecks[index] = value
        elif self.missile_collisionChecks[index] == False:
            self.missile_collisionChecks[index] = value

    def get_hp(self):
        return self.hp

    def get_score(self):
        print(self.hp)
        if self.hp < MID_MONSTER_HP_MAX and self.hp > 0:
            return 0
        else:
            return self.socre

    def get_special_score(self):
        return 100

class BossMonster:
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
    image_explosion = None
    image_hp = None
    dieSound = None

    collision_area_count = COLLISION_AREA_3
    missile_collision_area_count = MISSILE_MAX

    def __init__(self):
        # 몬스터 관련 변수
        # self.x, self.y = random.randint(0 + 64, CANVAS_WIDTH - 64), random.randint(CANVAS_HEIGHT, CANVAS_HEIGHT+CANVAS_HEIGHT/2)
        self.x = CANVAS_WIDTH / 2
        self.y = CANVAS_HEIGHT+CANVAS_HEIGHT/2
        self.stopY = CANVAS_HEIGHT - (CANVAS_HEIGHT/4)
        self.frame = random.randint(0, 3)
        self.hp = BOSS_MONSTER_HP_MAX
        self.socre = self.hp * 100
        self.degree = 0
        self.r = 100
        self.nomalX, self.nomalY = self.x, self.stopY -100
        self.gameState = True

        if BossMonster.image_red == None:
            BossMonster.image_red = load_image('Resource/Monster/boss.png')
        if BossMonster.image_hp == None:
            BossMonster.image_hp = load_image('Resource/Monster/boss_hp.png')
        if BossMonster.dieSound == None:
            BossMonster.dieSound = load_wav('Resource/Sound/mon_die.wav')
            BossMonster.dieSound.set_volume(5)

        self.collisionX1 = [0]*COLLISION_AREA_3
        self.collisionY1= [0]*COLLISION_AREA_3
        self.collisionX2 = [0]*COLLISION_AREA_3
        self.collisionY2= [0]*COLLISION_AREA_3
        self.collisionChecks= [0]*COLLISION_AREA_3

        for self.collisionCheck in self.collisionChecks:
            self.collisionCheck = False

        # 미사일 관련 변수
        if BossMonster.image_missile == None:
            BossMonster.image_missile = load_image('Resource/Missile/monster_missile.png')
        self.missile_frame = MONSTER_MISSILE_POWER_2

        self.missile_x = [0]*MISSILE_MAX
        self.missile_y= [0]*MISSILE_MAX
        self.missile_show= [0]*MISSILE_MAX
        self.missile_collisionX1 = [0]*MISSILE_MAX
        self.missile_collisionY1= [0]*MISSILE_MAX
        self.missile_collisionX2 = [0]*MISSILE_MAX
        self.missile_collisionY2= [0]*MISSILE_MAX
        self.missile_collisionChecks= [0]*MISSILE_MAX
        for self.missile_collisionCheck in self.missile_collisionChecks:
            self.missile_collisionCheck = False

        self.left_missile_x = [0]*MISSILE_MAX
        self.left_missile_y= [0]*MISSILE_MAX
        self.left_missile_show= [0]*MISSILE_MAX
        self.left_missile_collisionX1 = [0]*MISSILE_MAX
        self.left_missile_collisionY1= [0]*MISSILE_MAX
        self.left_missile_collisionX2 = [0]*MISSILE_MAX
        self.left_missile_collisionY2= [0]*MISSILE_MAX
        self.left_missile_collisionChecks= [0]*MISSILE_MAX
        for self.left_missile_collisionCheck in self.left_missile_collisionChecks:
            self.left_missile_collisionCheck = False

        self.right_missile_x = [0]*MISSILE_MAX
        self.right_missile_y= [0]*MISSILE_MAX
        self.right_missile_show= [0]*MISSILE_MAX
        self.right_missile_collisionX1 = [0]*MISSILE_MAX
        self.right_missile_collisionY1= [0]*MISSILE_MAX
        self.right_missile_collisionX2 = [0]*MISSILE_MAX
        self.right_missile_collisionY2= [0]*MISSILE_MAX
        self.right_missile_collisionChecks= [0]*MISSILE_MAX
        for self.right_missile_collisionCheck in self.right_missile_collisionChecks:
            self.right_missile_collisionCheck = False

        # 폭발 관련 변수
        self.explosion_show = False
        self.explosion_frame = 0

        if BossMonster.image_explosion == None:
            self.image_explosion = load_image('Resource/Explosion/boss_monster_explosion.png')

        self.life_time = 0.0
        self.total_frames = 0.0

    def setShowCheck(self, showCheck):
        self.showCheck = showCheck

    def newCreateBossMonster(self):
        self.hp = 0

    def dieBossMonster(self):
        self.gameState = False
        self.showExplosion(self.x, self.y)
        BossMonster.dieSound.play()

    def newCreateBossMonsterMissile(self, index):
        self.missile_show[index] = False
        self.missile_collisionChecks[index] = False
        self.missile_collisionX1[index] = False
        self.missile_collisionY1[index] = False
        self.missile_collisionX2[index] = False
        self.missile_collisionY2[index] = False

    def newCreateBossMonsterLeftMissile(self, index):
        self.left_missile_show[index] = False
        self.left_missile_collisionChecks[index] = False
        self.left_missile_collisionX1[index] = False
        self.left_missile_collisionY1[index] = False
        self.left_missile_collisionX2[index] = False
        self.left_missile_collisionY2[index] = False

    def newCreateBossMonsterRightMissile(self, index):
        self.right_missile_show[index] = False
        self.right_missile_collisionChecks[index] = False
        self.right_missile_collisionX1[index] = False
        self.right_missile_collisionY1[index] = False
        self.right_missile_collisionX2[index] = False
        self.right_missile_collisionY2[index] = False

    def update(self, frame_time):
        # 몬스터
        self.life_time += frame_time
        distance = BossMonster.FLY_SPEED_PPS * frame_time
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames/5) % 3
        # self.frame = (self.frame + 1) % 3
        if self.gameState == True:
            if self.y > 0 :
                if self.y > self.stopY:
                    self.y = self.y - distance
                else:
                    self.x = self.nomalX +(self.r*math.sin((self.degree/360)*math.pi))
                    self.y = self.nomalY +(self.r*math.cos((self.degree/360)*math.pi))
                    if self.degree < 710:
                        self.degree += 10
                    else:
                        self.degree = 0

            else:
                self.x, self.y = random.randint(0 + 64, CANVAS_WIDTH - 64), random.randint(CANVAS_HEIGHT, CANVAS_HEIGHT+CANVAS_HEIGHT/2)

            # 미사일
            self.life_time += frame_time
            distance = BossMonster.MISSILE_SPEED_PPS * frame_time
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

            i = 0
            while(i < MISSILE_MAX):
                if self.left_missile_show[i] == True:
                    if self.left_missile_y[i] > 0:
                        self.left_missile_y[i] -= distance
                        self.left_missile_x[i] -= distance*(0.5)
                    else:
                        self.left_missile_show[i] = False
                i += 1
            self.showLeftMissile(self.x, self.y)

            i = 0
            while(i < MISSILE_MAX):
                if self.right_missile_show[i] == True:
                    if self.right_missile_y[i] > 0:
                        self.right_missile_y[i] -= distance
                        self.right_missile_x[i] += distance*(0.5)
                    else:
                        self.right_missile_show[i] = False
                i += 1
            self.showRightMissile(self.x, self.y)

        # 폭발
        if self.explosion_show == True:
            self.explosion_time += frame_time
            if self.explosion_frame < 5 :
                self.explosion_frame =int(self.explosion_time*5)
            else :
                self.explosion_show = False
                self.explosion_frame = 0

    def draw(self):
        # 몬스터
        if self.gameState == True:
            self.image_red.clip_draw(self.frame * 512, 0, 512, 512, self.x, self.y)
            imageXSize = 800 * (self.hp/ BOSS_MONSTER_HP_MAX)
            # print("imageXSize %d" % imageXSize)
            self.image_hp.clip_draw(0, 0, (int)(imageXSize), 20, (int)(imageXSize) // 2, 990)

            # 미사일
            i = 0
            while(i < MISSILE_MAX):
                if self.missile_show[i] == True:
                    self.image_missile.clip_draw(self.missile_frame * 22, 0, 22, 14, self.missile_x[i] - 2, self.missile_y[i] - 30)
                if self.left_missile_show[i] == True:
                    self.image_missile.clip_draw(self.missile_frame * 22, 0, 22, 14, self.left_missile_x[i] - 2, self.left_missile_y[i] - 30)
                if self.right_missile_show[i] == True:
                    self.image_missile.clip_draw(self.missile_frame * 22, 0, 22, 14, self.right_missile_x[i] - 2, self.right_missile_y[i] - 30)
                i += 1

        # 폭발관련
        if self.explosion_show == True:
            self.image_explosion.clip_draw(self.explosion_frame * 500, 0, 500, 500, self.explosion_x, self.explosion_y)

    def showArea(self, showCheck):
        self.showCheck = showCheck
        # 몬스터
        self.collisionX1[0] = (self.x) - 110
        self.collisionY1[0] = (self.y+40) - 160
        self.collisionX2[0] = (self.x) + 110
        self.collisionY2[0] = (self.y+40) + 160
        self.collisionX1[1] = (self.x-160) - 50
        self.collisionY1[1] = (self.y+15) - 110
        self.collisionX2[1] = (self.x-160) + 50
        self.collisionY2[1] = (self.y+15) + 110
        self.collisionX1[2] = (self.x+160) - 50
        self.collisionY1[2] = (self.y+15) - 110
        self.collisionX2[2] = (self.x+160) + 50
        self.collisionY2[2] = (self.y+15) + 110
        # draw_rectangle(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
        # draw_rectangle(self.collisionX1[1],self.collisionY1[1],self.collisionX2[1],self.collisionY2[1])
        # draw_rectangle(self.collisionX1[2],self.collisionY1[2],self.collisionX2[2],self.collisionY2[2])
        # if self.collisionChecks[0] == True:
        #     draw_rectangle_green(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
        # else :
        #     draw_rectangle_red(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
        #
        # if self.collisionChecks[1] == True:
        #     draw_rectangle_green(self.collisionX1[1],self.collisionY1[1],self.collisionX2[1],self.collisionY2[1])
        # else:
        #     draw_rectangle_red(self.collisionX1[1],self.collisionY1[1],self.collisionX2[1],self.collisionY2[1])
        #
        # if self.collisionChecks[2] == True:
        #     draw_rectangle_green(self.collisionX1[2],self.collisionY1[2],self.collisionX2[2],self.collisionY2[2])
        # else:
        #     draw_rectangle_red(self.collisionX1[2],self.collisionY1[2],self.collisionX2[2],self.collisionY2[2])
        if self.showCheck == True:
            draw_rectangle(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
            draw_rectangle(self.collisionX1[1],self.collisionY1[1],self.collisionX2[1],self.collisionY2[1])
            draw_rectangle(self.collisionX1[2],self.collisionY1[2],self.collisionX2[2],self.collisionY2[2])


        # 미사일
        i = 0
        while(i < MISSILE_MAX):
            if self.missile_show[i] == True:
                self.missile_collisionX1[i] = (self.missile_x[i]-3) - 4
                self.missile_collisionY1[i] = (self.missile_y[i]-30) + 4
                self.missile_collisionX2[i] = (self.missile_x[i]-3) + 4
                self.missile_collisionY2[i] = (self.missile_y[i]-30) - 4

                # if self.missile_collisionChecks[i] == True:
                #     draw_rectangle_green(self.missile_collisionX1[i],self.missile_collisionY1[i],self.missile_collisionX2[i],self.missile_collisionY2[i])
                # else :
                #     draw_rectangle_red(self.missile_collisionX1[i],self.missile_collisionY1[i],self.missile_collisionX2[i],self.missile_collisionY2[i])
                if self.showCheck == True:
                    draw_rectangle(self.missile_collisionX1[i],self.missile_collisionY1[i],self.missile_collisionX2[i],self.missile_collisionY2[i])

            if self.left_missile_show[i] == True:
                self.left_missile_collisionX1[i] = (self.left_missile_x[i]-3) - 4
                self.left_missile_collisionY1[i] = (self.left_missile_y[i]-30) + 4
                self.left_missile_collisionX2[i] = (self.left_missile_x[i]-3) + 4
                self.left_missile_collisionY2[i] = (self.left_missile_y[i]-30) - 4

                # if self.missile_collisionChecks[i] == True:
                #     draw_rectangle_green(self.missile_collisionX1[i],self.missile_collisionY1[i],self.missile_collisionX2[i],self.missile_collisionY2[i])
                # else :
                #     draw_rectangle_red(self.missile_collisionX1[i],self.missile_collisionY1[i],self.missile_collisionX2[i],self.missile_collisionY2[i])
                if self.showCheck == True:
                    draw_rectangle(self.left_missile_collisionX1[i],self.left_missile_collisionY1[i],self.left_missile_collisionX2[i],self.left_missile_collisionY2[i])

            if self.right_missile_show[i] == True:
                self.right_missile_collisionX1[i] = (self.right_missile_x[i]-3) - 4
                self.right_missile_collisionY1[i] = (self.right_missile_y[i]-30) + 4
                self.right_missile_collisionX2[i] = (self.right_missile_x[i]-3) + 4
                self.right_missile_collisionY2[i] = (self.right_missile_y[i]-30) - 4

                # if self.missile_collisionChecks[i] == True:
                #     draw_rectangle_green(self.missile_collisionX1[i],self.missile_collisionY1[i],self.missile_collisionX2[i],self.missile_collisionY2[i])
                # else :
                #     draw_rectangle_red(self.missile_collisionX1[i],self.missile_collisionY1[i],self.missile_collisionX2[i],self.missile_collisionY2[i])
                if self.showCheck == True:
                    draw_rectangle(self.right_missile_collisionX1[i],self.right_missile_collisionY1[i],self.right_missile_collisionX2[i],self.right_missile_collisionY2[i])

            i += 1

    def showMissile(self, showX, showY):
        i = 0
        if showY < CANVAS_HEIGHT:
            while(i < MISSILE_MAX):
                self.checkInt = random.randint(0, 10000)
                if self.checkInt > 9995:
                    if self.missile_show[i] == False:
                        self.missile_show[i] = True
                        self.missile_x[i] = showX
                        self.missile_y[i] = showY
                        break
                i += 1

    def showLeftMissile(self, showX, showY):
        i = 0
        if showY < CANVAS_HEIGHT:
            while(i < MISSILE_MAX):
                self.checkInt = random.randint(0, 10000)
                if self.checkInt > 9995:
                    if self.left_missile_show[i] == False:
                        self.left_missile_show[i] = True
                        self.left_missile_x[i] = showX
                        self.left_missile_y[i] = showY
                        break
                i += 1

    def showRightMissile(self, showX, showY):
        i = 0
        if showY < CANVAS_HEIGHT:
            while(i < MISSILE_MAX):
                self.checkInt = random.randint(0, 10000)
                if self.checkInt > 9995:
                    if self.right_missile_show[i] == False:
                        self.right_missile_show[i] = True
                        self.right_missile_x[i] = showX
                        self.right_missile_y[i] = showY
                        break
                i += 1

    def showExplosion(self, showX, showY):
        if self.explosion_show == False:
            self.explosion_show = True
            self.explosion_x = showX
            self.explosion_y = showY
            self.explosion_frame = 0
            self.explosion_time = 0

    def get_bb(self, index):
        return self.collisionX1[index], self.collisionY1[index], self.collisionX2[index], self.collisionY2[index]

    def set_collisionCheck(self, index, value, change):
        if self.gameState == True:
            if change == True:
                self.collisionChecks[index] = value
            elif self.collisionChecks[index] == False:
                self.collisionChecks[index] = value
                # print(self.hp)
                if value == True:
                    if self.hp > 0:
                        self.hp -= 1
                    else :
                        self.dieBossMonster()

    def get_missile_bb(self, index):
        # return self.missile_collisionX1[index], self.missile_collisionY1[index], self.missile_collisionX2[index], self.missile_collisionY2[index]
        if self.missile_show[index]:
            return self.missile_collisionX1[index], self.missile_collisionY1[index], self.missile_collisionX2[index], self.missile_collisionY2[index]
        else:
            return -100, -100, -100, -100

    def set_missile_collisionCheck(self, index, value, change):
        if change == True:
            self.missile_collisionChecks[index] = value
        elif self.missile_collisionChecks[index] == False:
            self.missile_collisionChecks[index] = value

    def get_left_missile_bb(self, index):
        # return self.missile_collisionX1[index], self.missile_collisionY1[index], self.missile_collisionX2[index], self.missile_collisionY2[index]
        if self.left_missile_show[index]:
            return self.left_missile_collisionX1[index], self.left_missile_collisionY1[index], self.left_missile_collisionX2[index], self.left_missile_collisionY2[index]
        else:
            return -100, -100, -100, -100

    def set_left_missile_collisionCheck(self, index, value, change):
        if change == True:
            self.left_missile_collisionChecks[index] = value
        elif self.left_missile_collisionChecks[index] == False:
            self.left_missile_collisionChecks[index] = value

    def get_right_missile_bb(self, index):
        # return self.missile_collisionX1[index], self.missile_collisionY1[index], self.missile_collisionX2[index], self.missile_collisionY2[index]
        if self.right_missile_show[index]:
            return self.right_missile_collisionX1[index], self.right_missile_collisionY1[index], self.right_missile_collisionX2[index], self.right_missile_collisionY2[index]
        else:
            return -100, -100, -100, -100

    def set_right_missile_collisionCheck(self, index, value, change):
        if change == True:
            self.right_missile_collisionChecks[index] = value
        elif self.right_missile_collisionChecks[index] == False:
            self.right_missile_collisionChecks[index] = value

    def get_hp(self):
        return self.hp

    def get_score(self):
        if self.hp < BOSS_MONSTER_HP_MAX and self.hp > 0:
            return 0
        else:
            return self.socre

    def get_gameEnd(self):
        return self.gameState


# class Explosion:
#     image = None
#
#     def __init__(self):
#         self.image = load_image('Resource/Explosion/mid_monster_explosion.png')
#         self.x, self.y = 50, 50
#         self.life_time = 0.0
#         self.frame = 0
#         self.total_frames = 0.0
#
#     def update(self, frame_time):
#         self.life_time += frame_time
#         self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
#         self.frame = int(self.total_frames/5) % 5
#     def draw(self):
#         # 몬스터
#         self.image.clip_draw(self.frame * 55, 0, 55, 81, self.x, self.y)