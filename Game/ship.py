import pygame as pg
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.screen_rect=ai_game.screen.get_rect()
        self.image=pg.image.load('C:\\Users\\Тимур\\Desktop\\Game\\ship.bmp')
        self.rect=self.image.get_rect()
        self.rect.midbottom=self.screen_rect.midbottom#start every ship in the middle bottom

        #Ship's position
        self.x=float(self.rect.x)

        self.moving_right=False#Movement Flag. base value - False
        self.moving_left=False
    #Update ship's position
    def update(self):
        if self.moving_right and self.rect.right< self.screen_rect.right:#Part after "and"-movement limitation
            self.rect.x +=self.settings.ship_speed
        if self.moving_left and self.rect.left>0:
            self.rect.x-=self.settings.ship_speed
    
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)

