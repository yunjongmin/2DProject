import random
import json
import os

from pico2d import *
from math import *

import game_framework
import enemy_class
import player_class
import obstacle_class

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 1000
MISSILE_MAX = 100
COLLISION_AREA_3 = 3

name = "MainState"

background = None
player = None
monsters = None
mid_monsters = None
# boss_monster1 = None
player_missile = None
# mid_monster_missile1 = None
obstacle = None
player_special_missile = None
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



def enter():
    global background
    global player
    global monsters
    global mid_monsters
    global player_missile
    # global boss_monster1
    global obstacle
    global player_special_missile
    background = Background()
    player = player_class.Player()
    monsters = [enemy_class.Monster() for i in range(5)]
    mid_monsters = [enemy_class.MidMonster() for i in range(2)]
    # boss_monster1 = BossMonster1()
    player_missile =  player_class.PlayerMissile()
    obstacle = obstacle_class.Obstacle1()
    player_special_missile = player_class.SpecialMissile()
    pass


def exit():
    global background
    global player
    global monsters
    global mid_monsters
    # global boss_monster1
    global player_missile
    global obstacle
    global player_special_missile

    del(background)
    del(player)
    del(monsters)
    del(mid_monsters)
    # del(boss_monster1)
    del(player_missile)
    del(obstacle)
    del(player_special_missile)
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
            player_special_missile.showSpecial(player.x, player.y)

    pass


def update():
    background.update()
    for monster in monsters:
        monster.update()
    for mid_monster in mid_monsters:
        mid_monster.update()
    # boss_monster1.update()
    player_missile.update()
    player_special_missile.update()
    obstacle.update()
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
    player_special_missile.draw()
    obstacle.draw()
    # obstacle1.draw()
    player.draw()

    player.showArea()
    player_missile.showArea()
    player_special_missile.showArea()
    for monster in monsters:
        monster.showArea()
    for mid_monster in mid_monsters:
        mid_monster.showArea()
    obstacle.showArea()


    update_canvas()
    pass





