import random

from pico2d import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 1000
COLLISION_AREA_1 = 1
COLLISION_AREA_3 = 3
MISSILE_MAX = 100
MISSILE_POWER_1 = 1
MISSILE_POWER_2 = 2
SPECIAL_MAX = 3
SPECIAL_MISSILE_A = 1

PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Player:
    FLY_SPEED_KMPH = 30.0                    # Km / Hour
    FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
    FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
    FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

    collision_area_count = COLLISION_AREA_3

    image = None
    moveRight = None
    moveLeft = None
    moveUp = None
    moveDown = None

    def __init__(self):
        self.x, self.y = 270, 200
        self.frame = 0
        if Player.image == None :
            Player.image = load_image('Resource/Character/character1.png')
        self.collisionX1 = [0]*COLLISION_AREA_3
        self.collisionY1= [0]*COLLISION_AREA_3
        self.collisionX2 = [0]*COLLISION_AREA_3
        self.collisionY2= [0]*COLLISION_AREA_3
        self.collisionChecks= [0]*COLLISION_AREA_3

        for self.collisionCheck in self.collisionChecks:
            self.collisionCheck = False

        self.life_time = 0.0
        self.total_frames = 0.0

    # def get_collision_area_count(self):
    #     return self.collision_area_count

    def update(self, frame_time):
        self.life_time += frame_time
        distance = Player.FLY_SPEED_PPS * frame_time
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 3

        if self.moveRight:
            if self.x < CANVAS_WIDTH - distance:
                self.x += distance
        elif self.moveLeft:
            if self.x > distance :
                self.x -= distance

        if self.moveUp:
            if self.y < CANVAS_HEIGHT - distance :
                self.y += distance
        elif self.moveDown:
            if self.y > distance :
                self.y -= distance

        self.showArea();

    def draw(self):
        self.image.clip_draw(self.frame * 170, 0, 170, 128, self.x, self.y)

    def showArea(self):
        self.collisionX1[0] = self.x - 20
        self.collisionY1[0] = (self.y+10) - 50
        self.collisionX2[0] = self.x + 20
        self.collisionY2[0] = (self.y+10) + 50
        self.collisionX1[1] = (self.x-40) - 30
        self.collisionY1[1] = (self.y+8) - 20
        self.collisionX2[1] = (self.x-40) + 30
        self.collisionY2[1] = (self.y+8) + 20
        self.collisionX1[2] = (self.x+40) - 30
        self.collisionY1[2] = (self.y+8) - 20
        self.collisionX2[2] = (self.x+40) + 30
        self.collisionY2[2] = (self.y+8) + 20

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

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            if self.moveRight == True:
                self.moveRight = False
            self.moveLeft = True
        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
                self.moveLeft = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT :
            if self.moveLeft == True:
                self.moveLeft = False
            self.moveRight = True
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            self.moveRight = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP :
            if self.moveDown == True:
                self.moveDown = False
            self.moveUp = True
        elif event.type == SDL_KEYUP and event.key == SDLK_UP:
            self.moveUp = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN :
            if self.moveUp == True:
                self.moveUp = False
            self.moveDown = True
        elif event.type == SDL_KEYUP and event.key == SDLK_DOWN:
            self.moveDown = False

    def get_bb(self, index):
        return self.collisionX1[index], self.collisionY1[index], self.collisionX2[index], self.collisionY2[index]

    def set_collisionCheck(self, index, value, change):
        if change == True:
            self.collisionChecks[index] = value
        elif self.collisionChecks[index] == False:
            self.collisionChecks[index] = value

class PlayerMissile:
    PLAYER_MISSILE_SPEED_KMPH = 20.0                    # Km / Hour
    PLAYER_MISSILE_SPEED_MPM = (PLAYER_MISSILE_SPEED_KMPH * 1000.0 / 60.0)
    PLAYER_MISSILE_SPEED_MPS = (PLAYER_MISSILE_SPEED_MPM / 60.0)
    PLAYER_MISSILE_SPEED_PPS = (PLAYER_MISSILE_SPEED_MPS * PIXEL_PER_METER)

    image = None
    power = MISSILE_POWER_1

    collision_area_count = MISSILE_MAX

    def __init__(self):
        self.frame = 0
        self.x = [0]*MISSILE_MAX
        self.y= [0]*MISSILE_MAX
        self.show= [0]*MISSILE_MAX
        if PlayerMissile.image == None:
            PlayerMissile.image = load_image('Resource/Missile/missile1.png')

        self.collisionX1 = [0]*MISSILE_MAX
        self.collisionY1= [0]*MISSILE_MAX
        self.collisionX2 = [0]*MISSILE_MAX
        self.collisionY2= [0]*MISSILE_MAX
        self.collisionChecks= [0]*MISSILE_MAX

        for self.collisionCheck in self.collisionChecks:
            self.collisionCheck = False

        self.life_time = 0.0
        self.total_frames = 0.0

    def showMissile(self, showX, showY):
        i = 0
        while(i < MISSILE_MAX):
            if self.show[i] == False:
                self.show[i] = True
                self.x[i] = showX
                self.y[i] = showY
                break
            i += 1

    def update(self, frame_time):
        self.life_time += frame_time
        distance = PlayerMissile.PLAYER_MISSILE_SPEED_PPS * frame_time
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time

        i = 0
        while(i < MISSILE_MAX):
            if self.show[i] == True:
                if self.y[i] < CANVAS_HEIGHT:
                    self.y[i] += distance
                else:
                    self.show[i] = False
            i += 1

    def draw(self):
        i = 0
        while(i < MISSILE_MAX):
            if self.show[i] == True:
                if self.power == MISSILE_POWER_1:
                    self.image.clip_draw(self.frame * 97, 0, 97, 135, self.x[i] + 2, self.y[i]+ 110)
            i += 1

    def showArea(self):
        i = 0
        while(i < MISSILE_MAX):
            if self.show[i] == True:
                if self.power == MISSILE_POWER_1:
                    self.collisionX1[i] = (self.x[i]) - 20
                    self.collisionY1[i] = (self.y[i]+75) - 20
                    self.collisionX2[i] = (self.x[i]) + 20
                    self.collisionY2[i] = (self.y[i]+75) + 20

                    if self.collisionChecks[i] == True:
                        draw_rectangle_green(self.collisionX1[i],self.collisionY1[i],self.collisionX2[i],self.collisionY2[i])
                    else :
                        draw_rectangle_red(self.collisionX1[i],self.collisionY1[i],self.collisionX2[i],self.collisionY2[i])

            i += 1

    def get_bb(self, index):
        return self.collisionX1[index], self.collisionY1[index], self.collisionX2[index], self.collisionY2[index]

    def set_collisionCheck(self, index, value, change):
        if change == True:
            self.collisionChecks[index] = value
        elif self.collisionChecks[index] == False:
            self.collisionChecks[index] = value


class SpecialMissile:
    PLAYER_SPECIAL_MISSILE_SPEED_KMPH = 13.0                    # Km / Hour
    PLAYER_SPECIAL_MISSILE_SPEED_MPM = (PLAYER_SPECIAL_MISSILE_SPEED_KMPH * 1000.0 / 60.0)
    PLAYER_SPECIAL_MISSILE_SPEED_MPS = (PLAYER_SPECIAL_MISSILE_SPEED_MPM / 60.0)
    PLAYER_SPECIAL_MISSILE_SPEED_PPS = (PLAYER_SPECIAL_MISSILE_SPEED_MPS * PIXEL_PER_METER)

    collision_area_count = SPECIAL_MAX

    image = None
    special_power = SPECIAL_MISSILE_A
    def __init__(self):
        self.frame = [0]*SPECIAL_MAX
        self.x = [0]*SPECIAL_MAX
        self.y= [0]*SPECIAL_MAX
        self.show= [0]*SPECIAL_MAX
        i = 0
        while(i < SPECIAL_MAX):
            self.frame[i] = random.randint(0, 3)
            i += 1

        if SpecialMissile.image == None:
            SpecialMissile.image = load_image('Resource/Missile/special1.png')

        self.collisionX1 = [0]*SPECIAL_MAX
        self.collisionY1= [0]*SPECIAL_MAX
        self.collisionX2 = [0]*SPECIAL_MAX
        self.collisionY2= [0]*SPECIAL_MAX
        self.collisionChecks= [0]*SPECIAL_MAX

        for self.collisionCheck in self.collisionChecks:
            self.collisionCheck = False

        self.life_time = 0.0
        self.total_frames = 0.0

    def showSpecial(self, showX, showY):
        i = 0
        while(i < SPECIAL_MAX):
                if self.show[i] == False:
                    self.show[i] = True
                    self.x[i] = showX
                    self.y[i] = showY
                    break
                i += 1

    def update(self, frame_time):
        self.life_time += frame_time
        distance = SpecialMissile.PLAYER_SPECIAL_MISSILE_SPEED_PPS * frame_time
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time

        i = 0
        while(i < SPECIAL_MAX):
            if self.show[i] == True:
                if self.y[i] < CANVAS_HEIGHT:
                    self.y[i] += distance
                    # self.frame[i] = (self.frame[i] + 1) % 3
                    self.frame[i] = int(self.total_frames) % 3
                else:
                    self.show[i] = False
            i += 1


    def draw(self):
        i = 0
        while(i < SPECIAL_MAX):
            if self.special_power == SPECIAL_MISSILE_A:
                if self.show[i] == True:
                    self.image.clip_draw(self.frame[i] * 162, 0, 162, 165, self.x[i] + 2, self.y[i]+ 110)
                i += 1

    def showArea(self):
        i = 0
        while(i < SPECIAL_MAX):
            if self.show[i] == True:
                if self.special_power == SPECIAL_MISSILE_A:
                    self.collisionX1[i] = (self.x[i]) - 70
                    self.collisionY1[i] = (self.y[i]+110) - 70
                    self.collisionX2[i] = (self.x[i]) + 70
                    self.collisionY2[i] = (self.y[i]+110) + 70

                    if self.collisionChecks[i] == True:
                        draw_rectangle_green(self.collisionX1[i],self.collisionY1[i],self.collisionX2[i],self.collisionY2[i])
                    else :
                        draw_rectangle_red(self.collisionX1[i],self.collisionY1[i],self.collisionX2[i],self.collisionY2[i])

                    # draw_rectangle(self.collisionX1[i],self.collisionY1[i],self.collisionX2[i],self.collisionY2[i])
            i += 1

    def get_bb(self, index):
        return self.collisionX1[index], self.collisionY1[index], self.collisionX2[index], self.collisionY2[index]

    def set_collisionCheck(self, index, value, change):
        if change == True:
            self.collisionChecks[index] = value
        elif self.collisionChecks[index] == False:
            self.collisionChecks[index] = value