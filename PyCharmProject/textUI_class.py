from pico2d import *

class TextUI:

    def __init__(self):
        self.font = load_font("Resource/Font/ConsolaMalgun.TTF", 20)
        self.playerScore = 0

    def update(self,frame_time):
        self.playerScore

    def draw(self):
        # print(self.playerScore)
        self.font.draw(690, 950, "점수:%d" % (self.playerScore))
        pass

    def set_playerScore(self, score):
        self.playerScore = score
