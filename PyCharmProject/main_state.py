import random
import json
import os

from pico2d import *
from math import *
from turtle import *

import game_framework

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 1000
MISSILE_MAX = 100
SPECIAL_MAX = 3

name = "MainState"

background = None
player = None
monster1 = None
monster2 = None
mid_monster1 = None
boss_monster1 = None
missile1 = None
monster_missile1 = None
mid_monster_missile1 = None
obstacle1 = None
special1 = None
r = 100


class Background:
    image1 = None
    image2 = None

    def __init__(self):
        self.x, self.y = CANVAS_WIDTH/2, CANVAS_HEIGHT/2
        self.image = load_image('Resource/back_02.bmp')
        self.image1 = self.image
        self.image2 = self.image

    def update(self):
        if self.y > -CANVAS_HEIGHT/2 + 10:
            self.y -= 5
        else:
            self.y = CANVAS_HEIGHT/2
    def draw(self):
        self.image1.draw(self.x, self.y)
        self.image2.draw(self.x, self.y + CANVAS_HEIGHT)

class Player:
    image = None
    moveRight = None
    moveLeft = None
    moveUp = None
    moveDown = None
    # collisionX1, collisionY1, collisionX2, collisionY2

    def __init__(self):
        self.x, self.y = 270, 200
        self.frame = 0
        if Player.image == None:
            Player.image = load_image('Resource/character1.png')

    def update(self):
        self.frame = (self.frame + 1) % 3
        # self.handle_state[self.state](self)
        if self.moveRight:
            if self.x < CANVAS_WIDTH - 10 :
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

    def draw(self):
        self.image.clip_draw(self.frame * 170, 0, 170, 128, self.x, self.y)

class Monster1:
    image = None

    def __init__(self):
        self.x, self.y = 120, 800
        self.frame = random.randint(0, 3)
        if Monster1.image == None:
            Monster1.image = load_image('Resource/monster1.png')

    def update(self):
        self.frame = (self.frame + 1) % 3
        if self.y > 0 :
            self.y = self.y - 5
        else:
            self.y = CANVAS_HEIGHT

        monster_missile1.showMissile(self.x, self.y)

    def draw(self):
        self.image.clip_draw(self.frame * 64, 0, 64, 64, self.x, self.y)

class Monster2:
    image = None

    def __init__(self):
        self.x, self.y = 720, 800
        # self.flyX,  self.flyY
        self.frame = random.randint(0, 3)
        if Monster2.image == None:
            Monster2.image = load_image('Resource/monster2.png')

    def update(self):
        self.frame = (self.frame + 1) % 3
        if self.y > 0 :
            self.y = self.y - 5
        else:
            self.y = CANVAS_HEIGHT


    def draw(self):
        self.image.clip_draw(self.frame * 64, 0, 64, 64, self.x, self.y)

class MidMonster1:
    image = None

    def __init__(self):
        self.x, self.y = 270, 700
        self.frame = random.randint(0, 3)
        if MidMonster1.image == None:
            MidMonster1.image = load_image('Resource/mid_boss1.png')

    def update(self):
        self.frame = (self.frame + 1) % 3
        if self.y > 0 :
            self.y = self.y - 3
        else:
            self.y = CANVAS_HEIGHT

        mid_monster_missile1.showMissile(self.x, self.y)

    def draw(self):
         self.image.clip_draw(self.frame * 170, 0, 170, 128, self.x, self.y)

class BossMonster1:
    image = None

    def __init__(self):
        self.nomalX, self.nomalY = 400, 700
        # self.x, self.y = 500, 600
        self.frame = random.randint(0, 3)
        self.degree = 0
        self.x = self.nomalX +(r*math.sin((self.degree/360)*math.pi))
        self.y = self.nomalY +(r*math.cos((self.degree/360)*math.pi))

        if BossMonster1.image == None:
            BossMonster1.image = load_image('Resource/boss1.png')

    def update(self):
        self.frame = (self.frame + 1) % 3
        self.x = self.nomalX +(r*math.sin((self.degree/360)*math.pi))
        self.y = self.nomalY +(r*math.cos((self.degree/360)*math.pi))

        if self.degree < 710:
            self.degree += 10
        else:
            self.degree = 0

    def draw(self):
         self.image.clip_draw(self.frame * 512, 0, 512, 512, self.x, self.y)

class Missile1:
    image = None

    def __init__(self):
        self.frame = 0
        self.x = [0]*MISSILE_MAX
        self.y= [0]*MISSILE_MAX
        self.show= [0]*MISSILE_MAX

        if Missile1.image == None:
            Missile1.image = load_image('Resource/missile1.png')

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
                self.image.clip_draw(self.frame * 97, 0, 97, 135, self.x[i] + 2, self.y[i]+ 110)
            i += 1

class MonsterMissile1:
    image = None

    def __init__(self):
        self.frame = 0
        self.x = [0]*MISSILE_MAX
        self.y= [0]*MISSILE_MAX
        self.show= [0]*MISSILE_MAX

        if MonsterMissile1.image == None:
            MonsterMissile1.image = load_image('Resource/monster_missile1.png')

    def showMissile(self, showX, showY):
        i = 0
        while(i < MISSILE_MAX):
            if i % 10 == 0:
                if self.show[i] == False:
                    self.show[i] = True
                    self.x[i] = showX
                    self.y[i] = showY
                    break
            i += 1

    def update(self):
        i = 0
        while(i < MISSILE_MAX):
            if i % 10 == 0:
                if self.show[i] == True:
                    if self.y[i] > 0:
                        self.y[i] -= 20
                    else:
                        self.show[i] = False
            i += 1

    def draw(self):
        i = 0
        while(i < MISSILE_MAX):
            if i % 10 == 0:
                if self.show[i] == True:
                    self.image.clip_draw(self.frame * 15, 0, 15, 9, self.x[i] - 2, self.y[i] - 30)
            i += 1

class MidMonsterMissile1:
    image = None

    def __init__(self):
        self.frame = 1
        self.x = [0]*MISSILE_MAX
        self.y= [0]*MISSILE_MAX
        self.show= [0]*MISSILE_MAX

        if MidMonsterMissile1.image == None:
            MidMonsterMissile1.image = load_image('Resource/monster_missile1.png')

    def showMissile(self, showX, showY):
        i = 0
        while(i < MISSILE_MAX):
            if i % 10 == 0:
                if self.show[i] == False:
                    self.show[i] = True
                    self.x[i] = showX
                    self.y[i] = showY
                    break
            i += 1

    def update(self):
        i = 0
        while(i < MISSILE_MAX):
            if i % 10 == 0:
                if self.show[i] == True:
                    if self.y[i] > 0:
                        self.y[i] -= 20
                    else:
                        self.show[i] = False
            i += 1

    def draw(self):
        i = 0
        while(i < MISSILE_MAX):
            if i % 10 == 0:
                if self.show[i] == True:
                    self.image.clip_draw(self.frame * 15, 0, 15, 9, self.x[i] - 2, self.y[i] - 30)
            i += 1

class Obstacle1:
    image = None

    def __init__(self):
        self.x, self.y = 100, CANVAS_HEIGHT
        if Obstacle1.image == None:
            Obstacle1.image = load_image('Resource/obstacle1.png')

    def update(self):
        if self.y > 0 :
            self.y = self.y - 20
        else:
            self.y = CANVAS_HEIGHT

    def draw(self):
         self.image.clip_draw(0, 0, 86, 135, self.x, self.y)

class Special1:
    image = None

    def __init__(self):
        self.frame = [0]*SPECIAL_MAX
        self.x = [0]*SPECIAL_MAX
        self.y= [0]*SPECIAL_MAX
        self.show= [0]*SPECIAL_MAX
        i = 0
        while(i < SPECIAL_MAX):
            self.frame[i] = random.randint(0, 3)
            i += 1

        if Special1.image == None:
            Special1.image = load_image('Resource/special1.png')

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
            if self.show[i] == True:
                self.image.clip_draw(self.frame[i] * 162, 0, 162, 165, self.x[i] + 2, self.y[i]+ 110)
            i += 1

def enter():
    global background
    global player
    global monster1
    global monster2
    global mid_monster1
    global missile1
    global monster_missile1
    global mid_monster_missile1
    global boss_monster1
    global obstacle1
    global special1
    background = Background()
    player = Player()
    monster1 = Monster1()
    monster2 = Monster2()
    mid_monster1 = MidMonster1()
    boss_monster1 = BossMonster1()
    missile1 =  Missile1()
    monster_missile1 = MonsterMissile1()
    mid_monster_missile1 = MidMonsterMissile1()
    obstacle1 = Obstacle1()
    special1 = Special1()
    pass


def exit():
    global background
    global player
    global monster1
    global monster2
    global mid_monster1
    global boss_monster1
    global missile1
    global monster_missile1
    global mid_monster_missile1
    global obstacle1
    global special1

    del(background)
    del(player)
    del(monster1)
    del(monster2)
    del(mid_monster1)
    del(boss_monster1)
    del(missile1)
    del(monster_missile1)
    del(mid_monster_missile1)
    del(obstacle1)
    del(special1)
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
           game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            if player.moveRight == True:
                player.moveRight = False
            player.moveLeft = True
        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
                player.moveLeft = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT :
            if player.moveLeft == True:
                player.moveLeft = False
            player.moveRight = True
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            player.moveRight = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP :
            if player.moveDown == True:
                player.moveDown = False
            player.moveUp = True
        elif event.type == SDL_KEYUP and event.key == SDLK_UP:
            player.moveUp = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN :
            if player.moveUp == True:
                player.moveUp = False
            player.moveDown = True
        elif event.type == SDL_KEYUP and event.key == SDLK_DOWN:
            player.moveDown = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_z:
            missile1.showMissile(player.x, player.y)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_x:
            special1.showSpecial(player.x, player.y)

    pass


def update():
    background.update()
    monster1.update()
    monster2.update()
    mid_monster1.update()
    boss_monster1.update()
    missile1.update()
    monster_missile1.update()
    mid_monster_missile1.update()
    special1.update()
    obstacle1.update()
    player.update()
    delay(0.1)
    pass


def draw():
    clear_canvas()
    background.draw()
    monster1.draw()
    monster2.draw()
    mid_monster1.draw()
    boss_monster1.draw()
    missile1.draw()
    monster_missile1.draw()
    mid_monster_missile1.draw()
    special1.draw()
    obstacle1.draw()
    player.draw()
    update_canvas()
    pass





