import random
import json
import os

from pico2d import *
from math import *

import game_framework
import enemy_class
import player_class
import obstacle_class
import title_state
import textUI_class

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 1000
MISSILE_MAX = 100
COLLISION_AREA_3 = 3

name = "MainState"

# 게임 시작, 종료 판단
gameState = None
# 오브젝트 충돌체크 사각형
collisionRectShow = None

background = None
player = None
monsters = None
mid_monsters = None
boss_monster = None
player_missile = None
player_protect_missile = None
# mid_monster_missile1 = None
obstacle = None
player_special_missile = None
textUI = None



class Background:
    # image1 = None
    # image2 = None

    def __init__(self):
        self.image = load_image('Resource/Background/back_02.bmp')
        self.speed_down = 100
        self.down = 0
        self.screen_width = CANVAS_WIDTH
        self.screen_height = CANVAS_HEIGHT

        self.bgm = load_music('Resource/Sound/background.mp3')
        self.bgm.set_volume(7)
        self.bgm.repeat_play()

        self.gameover_image = load_image('Resource/Etc/gameover.png')

    def update(self, frame_time):
        self.down = (self.down + frame_time * self.speed_down) % self.image.h

    def draw(self):
        y = int(self.down)
        h = min(self.image.h - y, self.screen_height)
        self.image.clip_draw_to_origin(0, y, self.screen_width, h, 0, 0)
        self.image.clip_draw_to_origin(0, 0, self.screen_width, self.screen_height - h, 0, h)

        if player.get_game_start() == False:
            self.gameover_image.clip_draw(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, CANVAS_WIDTH/2, CANVAS_HEIGHT/2)


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
#             BossMonster1.image = load_image('Resource/Monster/boss.png')
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
    global player_protect_missile
    global obstacle
    global player_special_missile
    global collisionRectShow
    global textUI
    global boss_monster

    collisionRectShow = False

    background = Background()
    player = player_class.Player()
    player.setShowCheck(collisionRectShow)
    monsters = [enemy_class.Monster() for i in range(5)]
    mid_monsters = [enemy_class.MidMonster() for i in range(2)]
    boss_monster = enemy_class.BossMonster()
    player_missile =  player_class.PlayerMissile()
    player_missile.setShowCheck(collisionRectShow)
    player_protect_missile =  player_class.PlayerMissile_S()
    player_protect_missile.setShowCheck(collisionRectShow)
    obstacle = obstacle_class.Obstacle()
    player_special_missile = player_class.SpecialMissile()
    player_special_missile.setShowCheck(collisionRectShow)
    textUI = textUI_class.TextUI()

    # global explosion
    # explosion = enemy_class.Explosion()


def destroy_world():
    global background
    global player
    global monsters
    global mid_monsters
    global boss_monster
    global player_missile
    global player_protect_missile
    global obstacle
    global player_special_missile
    global textUI


    del(background)
    del(player)
    del(monsters)
    del(mid_monsters)
    del(boss_monster)
    del(player_missile)
    del(player_protect_missile)
    del(obstacle)
    del(player_special_missile)
    del(textUI)

    # global explosion
    # del(explosion)

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
    global collisionRectShow

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_z:
            if player.get_player() == player_class.PLAYER_A :
                player_missile.showMissile(player.x, player.y)
            elif player.get_player() == player_class.PLAYER_S :
                player_protect_missile.showMissile(player.x, player.y)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_x:
            player_special_missile.showSpecial(player.x, player.y)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_r:
            if collisionRectShow == True:
                collisionRectShow = False
            else:
                collisionRectShow = True
        else:
            player.handle_event(event)
    pass


def collide(a, front_index, b, back_index):
    left_a, bottom_a, right_a, top_a = a.get_bb(front_index)
    left_b, bottom_b, right_b, top_b = b.get_bb(back_index)

    if left_a == 0 and bottom_a == 0 and right_a == 0 and top_a == 0:
        return False
    if left_b == 0 and bottom_b == 0 and right_b == 0 and top_b == 0:
        return False

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

    if left_a == 0 and bottom_a == 0 and right_a == 0 and top_a == 0:
        return False
    if left_b == 0 and bottom_b == 0 and right_b == 0 and top_b == 0:
        return False

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

    # 캐릭터 영역 초기화
    for i in range(0, player.collision_area_count):
        if player.collisionChecks[i] == True:
            player.set_collisionCheck(i, False, True)

    # 캐릭터 미사일 영역 초기화
    for i in range(0, player_missile.collision_area_count):
        if player_missile.collisionChecks[i] == True:
            player_missile.set_collisionCheck(i, False, True)

    # 캐릭터_S 미사일 영역 초기화
    if player_protect_missile.collisionCheck == True:
        player_protect_missile.set_collisionCheck(False, True)

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


    if player.get_game_start() == True:
        # 캐릭터와 몬스터 충돌 체크
        for i in range(0, player.collision_area_count):
            for monster in monsters:
                for j in range(0, monster.collision_area_count):
                    result = collide(player, i, monster, j)
                    player.set_collisionCheck(i, result, False)
                    monster.set_collisionCheck(j, result, False)
                    if result == True:
                        monster.newCreateMonster()
                        player.set_minusHp()
                        # if(player.hp < 1):
                        #     game_framework.change_state(title_state)

        # 캐릭터 미사일과 몬스터 충돌 체크
        for i in range(0, player_missile.collision_area_count):
            for monster in monsters:
                for j in range(0, monster.collision_area_count):
                    result = collide(player_missile, i, monster, j)
                    player_missile.set_collisionCheck(i, result, False)
                    monster.set_collisionCheck(j, result, False)
                    if result == True:
                        player.plus_score(monster.get_score())
                        player_missile.delete_missile(i)
                        # monster.newCreateMonster()

         # 캐릭터_S 미사일과 몬스터 미사일과 충돌 체크
        for monster in monsters:
            for j in range(0, monster.missile_collision_area_count):
                result = missile_collide(player_protect_missile, 0, monster, j)
                player_protect_missile.set_collisionCheck(result, False)
                monster.set_missile_collisionCheck(j, result, False)
                if result == True:
                    monster.newCreateMonsterMissile(j)

                 # 캐릭터_S 미사일과 몬스터 미사일과 충돌 체크
        for mid_monster in mid_monsters:
            for j in range(0, mid_monster.missile_collision_area_count):
                result = missile_collide(player_protect_missile, 0, mid_monster, j)
                player_protect_missile.set_collisionCheck(result, False)
                mid_monster.set_missile_collisionCheck(j, result, False)
                if result == True:
                    mid_monster.newCreateMidMonsterMissile(j)

        # 캐릭터 특수 미사일과 몬스터 충돌 체크
        for i in range(0, player_special_missile.collision_area_count):
            for monster in monsters:
                for j in range(0, monster.collision_area_count):
                    result = collide(player_special_missile, i, monster, j)
                    player_special_missile.set_collisionCheck(i, result, False)
                    monster.set_collisionCheck(j, result, False)
                    if result == True:
                        player.plus_score(monster.get_score())
                        monster.newCreateMonster()

        # 캐릭터와 몬스터 미사일과 충돌 체크
        for i in range(0, player.collision_area_count):
            for monster in monsters:
                for j in range(0, monster.missile_collision_area_count):
                    result = missile_collide(player, i, monster, j)
                    player.set_collisionCheck(i, result, False)
                    monster.set_missile_collisionCheck(j, result, False)
                    if result == True:
                        monster.newCreateMonsterMissile(j)
                        player.set_minusHp()

        # 캐릭터와 중간 몬스터 충돌 체크
        for i in range(0, player.collision_area_count):
            for mid_monster in mid_monsters:
                for j in range(0, mid_monster.collision_area_count):
                    result = collide(player, i, mid_monster, j)
                    player.set_collisionCheck(i, result, False)
                    mid_monster.set_collisionCheck(j, result, False)
                    if result == True:
                        mid_monster.newCreateMidMonster()
                        player.set_minusHp()

        # 캐릭터 미사일과 중간 몬스터 충돌 체크
        for i in range(0, player_missile.collision_area_count):
            for mid_monster in mid_monsters:
                for j in range(0, mid_monster.collision_area_count):
                    result = collide(player_missile, i, mid_monster, j)
                    player_missile.set_collisionCheck(i, result, False)
                    mid_monster.set_collisionCheck(j, result, False)
                    if result == True:
                        player.plus_score(mid_monster.get_score())
                        player_missile.delete_missile(i)
                        # mid_monster.newCreateMidMonster()

        # 캐릭터 특수 미사일과 중간 몬스터 충돌 체크
        for i in range(0, player_special_missile.collision_area_count):
            for mid_monster in mid_monsters:
                for j in range(0, mid_monster.collision_area_count):
                    result = collide(player_special_missile, i, mid_monster, j)
                    player_special_missile.set_collisionCheck(i, result, False)
                    mid_monster.set_collisionCheck(j, result, False)
                    if result == True:
                        player.plus_score(mid_monster.get_score())
                        mid_monster.newCreateMidMonster()

        # 캐릭터와 중간 몬스터 미사일과 충돌 체크
        for i in range(0, player.collision_area_count):
            for mid_monster in mid_monsters:
                for j in range(0, mid_monster.missile_collision_area_count):
                    result = missile_collide(player, i, mid_monster, j)
                    player.set_collisionCheck(i, result, False)
                    mid_monster.set_missile_collisionCheck(j, result, False)
                    if result == True:
                        mid_monster.newCreateMidMonsterMissile(j)
                        player.set_minusHp()

         # 캐릭터와 특수 장애물 충돌 체크
        for i in range(0, player.collision_area_count):
            for j in range(0, obstacle.collision_area_count):
                result = collide(player, i, obstacle, j)
                player.set_collisionCheck(i, result, False)
                obstacle.set_collisionCheck(j, result, False)

    textUI.set_playerScore(player.get_score())
    background.update(frame_time)
    for monster in monsters:
        monster.update(frame_time)
    for mid_monster in mid_monsters:
        mid_monster.update(frame_time)
    # boss_monster.update(frame_time)
    obstacle.update(frame_time)

    if player.get_game_start() == True:
        player_missile.update(frame_time)
        player_protect_missile.update(frame_time, player.get_playerX(), player.get_playerY())
        player_special_missile.update(frame_time)
        player.update(frame_time)

    # explosion.update(frame_time)

    delay(0.03)
    pass


def draw(frame_time):
    clear_canvas()
    background.draw()
    for monster in monsters:
        monster.draw()
    for mid_monster in mid_monsters:
        mid_monster.draw()
    obstacle.draw()
    # boss_monster.draw()
    if player.get_game_start() == True:
        player_missile.draw()
        player_protect_missile.draw()
        player_special_missile.draw()
        player.draw()
    textUI.draw()

    # if collisionRectShow == True:
    player.showArea(collisionRectShow)
    player_missile.showArea(collisionRectShow)
    player_protect_missile.showArea(collisionRectShow)
    player_special_missile.showArea(collisionRectShow)
    # boss_monster.showArea(collisionRectShow)
    for monster in monsters:
        monster.showArea(collisionRectShow)
    for mid_monster in mid_monsters:
        mid_monster.showArea(collisionRectShow)
    obstacle.showArea(collisionRectShow)

    # explosion.draw()

    update_canvas()
    pass





