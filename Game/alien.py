import pygame as pg
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_game):
        #Create alien
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.image=pg.image.load('C:\\Users\\Тимур\\Desktop\\Game\\alien.bmp')
        self.rect=self.image.get_rect()
        #Start each alien ship at the left corner
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        
        self.x=float(self.rect.x)#store horisontal position
    
    def update(self):
        self.x+=(self.settings.alien_speed*self.settings.fleet_direction)
        self.rect.x=self.x

    def check_edges(self):
        screen_rect=self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left<=0:
            return True




    