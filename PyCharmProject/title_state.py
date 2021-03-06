import game_framework
import main_state
from pico2d import *


name = "TitleState"
image = None
bgm = None

def enter():
    global image, bgm
    # image = load_image('Resource/Etc/start_logo.png')
    image = load_image('Resource/Etc/start_logo2.png')
    bgm = load_music('Resource/Sound/logo_background.mp3')
    bgm.set_volume(60)
    bgm.repeat_play()
    pass


def exit():
    global image, bgm
    del(image)
    del(bgm)
    pass


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)

    pass


def draw(frame_time):
    clear_canvas()
    image.draw(400, 500)
    update_canvas()
    pass


def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass






