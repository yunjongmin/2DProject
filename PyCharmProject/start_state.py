import game_framework
import main_state
from pico2d import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 1000

name = "StartState"
image = None
logo_time = 0.0


def enter():
    global image
    open_canvas(CANVAS_WIDTH,CANVAS_HEIGHT)
    image = load_image('Resource/Etc/kpu_credit.png')
    pass


def exit():
    global image
    del(image)
    close_canvas()
    pass


def update(frame_time):
    global logo_time

    if(logo_time > 1.0):
        logo_time = 0
        #game_framework.quit()
        game_framework.push_state(main_state)
    delay(0.01)
    logo_time += 0.01
    pass


def draw(frame_time):
    global image
    clear_canvas()
    image.draw(400, 500)
    update_canvas()
    pass




def handle_events(frame_time):
    events = get_events()
    pass


def pause(): pass


def resume(): pass



