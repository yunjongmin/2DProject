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

    def update(self, frame_time):
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

def create_world():
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
    obstacle = obstacle_class.Obstacle()
    player_special_missile = player_class.SpecialMissile()


def destroy_world():
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


def enter():
    game_framework.reset_time()
    create_world()


def exit():
    destroy_world()


def pause():
    pass


def resume():
    pass


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
           game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_z:
            player_missile.showMissile(player.x, player.y)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_x:
            player_special_missile.showSpecial(player.x, player.y)
        else:
            player.handle_event(event)
    pass


def collide(a, front_index, b, back_index):
    left_a, bottom_a, right_a, top_a = a.get_bb(front_index)
    left_b, bottom_b, right_b, top_b = b.get_bb(back_index)

    if left_a > right_b :
        return False
    if right_a < left_b :
        return False
    if top_a < bottom_b :
        return False
    if bottom_a > top_b :
        return False

    return True


def missile_collide(a, front_index, b, back_index):
    left_a, bottom_a, right_a, top_a = a.get_bb(front_index)
    left_b, bottom_b, right_b, top_b = b.get_missile_bb(back_index)

    if left_a > right_b :
        return False
    if right_a < left_b :
        return False
    if top_a < bottom_b :
        return False
    if bottom_a > top_b :
        return False

    return True


def update(frame_time):

    # for i in range(0, player.collision_area_count):
    #     player.set_collisionCheck(i, False, True)
    # for i in range(0, player_missile.collision_area_count):
    #     player_missile.set_collisionCheck(i, False, True)
    #
    # for i in range(0, player.collision_area_count):
    #     for j in range(0, player_missile.collision_area_count):
    #         result = collide(player, i, player_missile, j)
    #         player.set_collisionCheck(i, result, False)
    #         player_missile.set_collisionCheck(j, result, False)
    #
    # for i in range(0, player_special_missile.collision_area_count):
    #     player_special_missile.set_collisionCheck(i, False, True)
    #
    # for i in range(0, player.collision_area_count):
    #     for j in range(0, player_special_missile.collision_area_count):
    #         result = collide(player, i, player_special_missile, j)
    #         player.set_collisionCheck(i, result, False)
    #         player_special_missile.set_collisionCheck(j, result, False)

    # 캐릭터 영역 초기화
    for i in range(0, player.collision_area_count):
        if player.collisionChecks[i] == True:
            player.set_collisionCheck(i, False, True)

    # 캐릭터 미사일 영역 초기화
    for i in range(0, player_missile.collision_area_count):
        if player_missile.collisionChecks[i] == True:
            player_missile.set_collisionCheck(i, False, True)

    # 캐릭터 특수 미사일 영역 초기화
    for i in range(0, player_special_missile.collision_area_count):
        if player_special_missile.collisionChecks[i] == True:
            player_special_missile.set_collisionCheck(i, False, True)

    # 몬스터 영역 초기화
    for monster in monsters:
        for i in range(0, monster.collision_area_count):
            if monster.collisionChecks[i] == True:
                monster.set_collisionCheck(i, False, True)

    # 몬스터 미사일 영역 초기화
    for monster in monsters:
        for i in range(0, monster.missile_collision_area_count):
            if monster.missile_collisionChecks[i] == True:
                monster.set_missile_collisionCheck(i, False, True)

    # 중간 몬스터 영역 초기화
    for mid_monster in mid_monsters:
        for i in range(0, mid_monster.collision_area_count):
            if mid_monster.collisionChecks[i] == True:
                mid_monster.set_collisionCheck(i, False, True)

    # 중간 몬스터 미사일 영역 초기화
    for mid_monster in mid_monsters:
        for i in range(0, mid_monster.missile_collision_area_count):
            if mid_monster.missile_collisionChecks[i] == True:
                mid_monster.set_missile_collisionCheck(i, False, True)

    # 특수 장애물 영역 초기화
    for i in range(0, obstacle.collision_area_count):
        if obstacle.collisionChecks[i] == True:
            obstacle.set_collisionCheck(i, False, True)

    # 캐릭터와 몬스터 충돌 체크
    for i in range(0, player.collision_area_count):
        for monster in monsters:
            for j in range(0, monster.collision_area_count):
                result = collide(player, i, monster, j)
                player.set_collisionCheck(i, result, False)
                monster.set_collisionCheck(j, result, False)

    # 캐릭터 미사일과 몬스터 충돌 체크
    for i in range(0, player_missile.collision_area_count):
        for monster in monsters:
            for j in range(0, monster.collision_area_count):
                result = collide(player_missile, i, monster, j)
                player_missile.set_collisionCheck(i, result, False)
                monster.set_collisionCheck(j, result, False)
                if result == True:
                    player_missile.delete_missile(i)
                    monster.newCreateMonster()

    # 캐릭터 특수 미사일과 몬스터 충돌 체크
    for i in range(0, player_special_missile.collision_area_count):
        for monster in monsters:
            for j in range(0, monster.collision_area_count):
                result = collide(player_special_missile, i, monster, j)
                player_special_missile.set_collisionCheck(i, result, False)
                monster.set_collisionCheck(j, result, False)
                if result == True:
                    monster.newCreateMonster()

    # 캐릭터와 몬스터 미사일과 충돌 체크
    for i in range(0, player.collision_area_count):
        for monster in monsters:
            for j in range(0, monster.missile_collision_area_count):
                result = missile_collide(player, i, monster, j)
                player.set_collisionCheck(i, result, False)
                monster.set_missile_collisionCheck(j, result, False)

    # 캐릭터와 중간 몬스터 충돌 체크
    for i in range(0, player.collision_area_count):
        for mid_monster in mid_monsters:
            for j in range(0, mid_monster.collision_area_count):
                result = collide(player, i, mid_monster, j)
                player.set_collisionCheck(i, result, False)
                mid_monster.set_collisionCheck(j, result, False)

    # 캐릭터 미사일과 중간 몬스터 충돌 체크
    for i in range(0, player_missile.collision_area_count):
        for mid_monster in mid_monsters:
            for j in range(0, mid_monster.collision_area_count):
                result = collide(player_missile, i, mid_monster, j)
                player_missile.set_collisionCheck(i, result, False)
                mid_monster.set_collisionCheck(j, result, False)
                if result == True:
                    player_missile.delete_missile(i)
                    mid_monster.newCreateMidMonster()

    # 캐릭터 특수 미사일과 중간 몬스터 충돌 체크
    for i in range(0, player_special_missile.collision_area_count):
        for mid_monster in mid_monsters:
            for j in range(0, mid_monster.collision_area_count):
                result = collide(player_special_missile, i, mid_monster, j)
                player_special_missile.set_collisionCheck(i, result, False)
                mid_monster.set_collisionCheck(j, result, False)
                if result == True:
                    mid_monster.newCreateMidMonster()

    # 캐릭터와 중간 몬스터 미사일과 충돌 체크
    for i in range(0, player.collision_area_count):
        for mid_monster in mid_monsters:
            for j in range(0, mid_monster.missile_collision_area_count):
                result = missile_collide(player, i, mid_monster, j)
                player.set_collisionCheck(i, result, False)
                mid_monster.set_missile_collisionCheck(j, result, False)

     # 캐릭터와 특수 장애물 충돌 체크
    for i in range(0, player.collision_area_count):
        for j in range(0, obstacle.collision_area_count):
            result = collide(player, i, obstacle, j)
            player.set_collisionCheck(i, result, False)
            obstacle.set_collisionCheck(j, result, False)




    background.update(frame_time)
    for monster in monsters:
        monster.update(frame_time)
    for mid_monster in mid_monsters:
        mid_monster.update(frame_time)
    # boss_monster1.update()
    player_missile.update(frame_time)
    player_special_missile.update(frame_time)
    obstacle.update(frame_time)
    player.update(frame_time)


    delay(0.03)
    pass


def draw(frame_time):
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





