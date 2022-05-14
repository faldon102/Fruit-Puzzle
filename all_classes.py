import pygame
from pygame.locals import *
from pygame import mixer

pygame.init()

class Button:

    question_mark_image = pygame.image.load("question_mark.png")

    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def get_image(self):
        return self.image

def change_music(level):
    if level <= 8:
        mixer.music.load("Athletic.mp3")
        mixer.music.play(-1)
    else:
        mixer.music.load("06 Walking The Plains (Fast Version).mp3")
        mixer.music.play(-1)