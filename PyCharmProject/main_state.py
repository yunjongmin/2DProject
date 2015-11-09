import random
import json
import os

from pico2d import *
from math import *

import game_framework
import enemy
import player_class

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 1000
MISSILE_MAX = 100
SPECIAL_MAX = 3
COLLISION_AREA_3 = 3

name = "MainState"

background = None
player = None
monsters = None
mid_monsters = None
# boss_monster1 = None
player_missile = None
# mid_monster_missile1 = None
# obstacle1 = None
# special1 = None
# r = 100


class Background:
    image1 = None
    image2 = None

    def __init__(self):
        self.x, self.y = CANVAS_WIDTH/2, CANVAS_HEIGHT/2
        self.image = load_image('Resource/Background/back_02.bmp')
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


#
# class BossMonster1:
#     image = None
#
#     def __init__(self):
#         self.nomalX, self.nomalY = 400, 700
#         # self.x, self.y = 500, 600
#         self.frame = random.randint(0, 3)
#         self.degree = 0
#         self.x = self.nomalX +(r*math.sin((self.degree/360)*math.pi))
#         self.y = self.nomalY +(r*math.cos((self.degree/360)*math.pi))
#
#         if BossMonster1.image == None:
#             BossMonster1.image = load_image('Resource/Monster/boss1.png')
#
#     def update(self):
#         self.frame = (self.frame + 1) % 3
#         self.x = self.nomalX +(r*math.sin((self.degree/360)*math.pi))
#         self.y = self.nomalY +(r*math.cos((self.degree/360)*math.pi))
#
#         if self.degree < 710:
#             self.degree += 10
#         else:
#             self.degree = 0
#
#     def draw(self):
#          self.image.clip_draw(self.frame * 512, 0, 512, 512, self.x, self.y)
#
#
# class Obstacle1:
#     image = None
#
#     def __init__(self):
#         self.x, self.y = 100, CANVAS_HEIGHT
#         if Obstacle1.image == None:
#             Obstacle1.image = load_image('Resource/Etc/obstacle1.png')
#
#         self.collisionX1 = [0]
#         self.collisionY1= [0]
#         self.collisionX2 = [0]
#         self.collisionY2= [0]
#
#     def update(self):
#         if self.y > 0 :
#             self.y = self.y - 20
#         else:
#             self.y = CANVAS_HEIGHT
#
#     def draw(self):
#          self.image.clip_draw(0, 0, 86, 135, self.x, self.y)
#
#     def showArea(self):
#         self.collisionX1[0] = (self.x) - 40
#         self.collisionY1[0] = (self.y-25) + 40
#         self.collisionX2[0] = (self.x) + 40
#         self.collisionY2[0] = (self.y-25) - 40
#
#         draw_rectangle(self.collisionX1[0],self.collisionY1[0],self.collisionX2[0],self.collisionY2[0])
#
# class Special1:
#     image = None
#
#     def __init__(self):
#         self.frame = [0]*SPECIAL_MAX
#         self.x = [0]*SPECIAL_MAX
#         self.y= [0]*SPECIAL_MAX
#         self.show= [0]*SPECIAL_MAX
#         i = 0
#         while(i < SPECIAL_MAX):
#             self.frame[i] = random.randint(0, 3)
#             i += 1
#
#         if Special1.image == None:
#             Special1.image = load_image('Resource/Missile/special1.png')
#
#     def showSpecial(self, showX, showY):
#         i = 0
#         while(i < SPECIAL_MAX):
#             if self.show[i] == False:
#                 self.show[i] = True
#                 self.x[i] = showX
#                 self.y[i] = showY
#                 break
#             i += 1
#
#     def update(self):
#         i = 0
#         while(i < SPECIAL_MAX):
#             if self.show[i] == True:
#                 if self.y[i] < CANVAS_HEIGHT:
#                     self.y[i] += 10
#                     self.frame[i] = (self.frame[i] + 1) % 3
#                 else:
#                     self.show[i] = False
#             i += 1
#
#
#     def draw(self):
#         i = 0
#         while(i < SPECIAL_MAX):
#             if self.show[i] == True:
#                 self.image.clip_draw(self.frame[i] * 162, 0, 162, 165, self.x[i] + 2, self.y[i]+ 110)
#             i += 1

def enter():
    global background
    global player
    global monsters
    global mid_monsters
    global player_missile
    # global mid_monster_missile1
    # global boss_monster1
    # global obstacle1
    # global special1
    background = Background()
    player = player_class.Player()
    monsters = [enemy.Monster() for i in range(5)]
    mid_monsters = [enemy.MidMonster() for i in range(2)]
    # boss_monster1 = BossMonster1()
    player_missile =  player_class.PlayerMissile()
    # mid_monster_missile1 = MidMonsterMissile1()
    # obstacle1 = Obstacle1()
    # special1 = Special1()
    pass


def exit():
    global background
    global player
    global monsters
    global mid_monsters
    # global boss_monster1
    global player_missile
    # global mid_monster_missile1
    # global obstacle1
    # global special1

    del(background)
    del(player)
    del(monsters)
    del(mid_monsters)
    # del(boss_monster1)
    del(player_missile)
    # del(mid_monster_missile1)
    # del(obstacle1)
    # del(special1)
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
            player_missile.showMissile(player.x, player.y)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_x:
            player_missile.showSpecial(player.x, player.y)

    pass


def update():
    background.update()
    for monster in monsters:
        monster.update()
    for mid_monster in mid_monsters:
        mid_monster.update()
    # boss_monster1.update()
    player_missile.update()
    # mid_monster_missile1.update()
    # special1.update()
    # obstacle1.update()
    player.update()
    delay(0.1)
    pass


def draw():
    clear_canvas()
    background.draw()
    for monster in monsters:
        monster.draw()
    for mid_monster in mid_monsters:
        mid_monster.draw()
    # boss_monster1.draw()
    player_missile.draw()
    # mid_monster_missile1.draw()
    # special1.draw()
    # obstacle1.draw()
    player.draw()

    player.showArea()
    player_missile.showArea()
    for monster in monsters:
        monster.showArea()
    for mid_monster in mid_monsters:
        mid_monster.showArea()
    # mid_monster_missile1.showArea()
    # obstacle1.showArea()


    update_canvas()
    pass





