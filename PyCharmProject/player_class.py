import random

from pico2d import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 1000
COLLISION_AREA_3 = 3
MISSILE_MAX = 100
MISSILE_POWER_1 = 1
MISSILE_POWER_2 = 2
SPECIAL_MAX = 3
SPECIAL_MISSILE_A = 1


class Player:
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

    def update(self):
        self.frame = (self.frame + 1) % 3

        if self.moveRight:
            if self.x < CANVAS_WIDTH - 10:
                self.x += 10
        elif self.moveLeft:
            if self.x > 10 :
                self.x -= 10

        if self.moveUp:
            if self.y < CANVAS_HEIGHT -10 :
                self.y += 10
        elif self.moveDown:
            if self.y > 10 :
                self.y -= 10

        self.showArea();

    def draw(self):
        self.image.clip_draw(self.frame * 170, 0, 170, 128, self.x, self.y)

    def showArea(self):
        self.collisionX1[0] = self.x - 20
        self.collisionY1[0] = (self.y+10) + 50
        self.collisionX2[0] = self.x + 20
        self.collisionY2[0] = (self.y+10) - 50
        self.collisionX1[1] = (self.x-40) - 30
        self.collisionY1[1] = (self.y+8) + 20
        self.collisionX2[1] = (self.x-40) + 30
        self.collisionY2[1] = (self.y+8) - 20
        self.collisionX1[2] = (self.x+40) - 30
        self.collisionY1[2] = (self.y+8) + 20
        self.collisionX2[2] = (self.x+40) + 30
        self.collisionY2[2] = (self.y+8) - 20
        draw_rectangle(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
        draw_rectangle(self.collisionX1[1],self.collisionY1[1],self.collisionX2[1],self.collisionY2[1])
        draw_rectangle(self.collisionX1[2],self.collisionY1[2],self.collisionX2[2],self.collisionY2[2])


class PlayerMissile:
    image = None
    power = MISSILE_POWER_1

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

    def showMissile(self, showX, showY):
        i = 0
        while(i < MISSILE_MAX):
            if self.show[i] == False:
                self.show[i] = True
                self.x[i] = showX
                self.y[i] = showY
                break
            i += 1

    def update(self):
        i = 0
        while(i < MISSILE_MAX):
            if self.show[i] == True:
                if self.y[i] < CANVAS_HEIGHT:
                    self.y[i] += 10
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
                    self.collisionY1[i] = (self.y[i]+75) + 20
                    self.collisionX2[i] = (self.x[i]) + 20
                    self.collisionY2[i] = (self.y[i]+75) - 20

                    draw_rectangle(self.collisionX1[i],self.collisionY1[i],self.collisionX2[i],self.collisionY2[i])
            i += 1


class SpecialMissile:
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

    def showSpecial(self, showX, showY):
        i = 0
        while(i < SPECIAL_MAX):
                if self.show[i] == False:
                    self.show[i] = True
                    self.x[i] = showX
                    self.y[i] = showY
                    break
                i += 1

    def update(self):
        i = 0
        while(i < SPECIAL_MAX):
            if self.show[i] == True:
                if self.y[i] < CANVAS_HEIGHT:
                    self.y[i] += 10
                    self.frame[i] = (self.frame[i] + 1) % 3
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
                    self.collisionY1[i] = (self.y[i]+110) + 70
                    self.collisionX2[i] = (self.x[i]) + 70
                    self.collisionY2[i] = (self.y[i]+110) - 70

                    draw_rectangle(self.collisionX1[i],self.collisionY1[i],self.collisionX2[i],self.collisionY2[i])
            i += 1