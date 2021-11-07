import pygame as pg
import sys as s
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:#Overall class to manage game
    def __init__(self):
        pg.init()
        self.settings=Settings()        
        self.screen=pg.display.set_mode((self.settings.screen_width, self.settings.screen_height))#Window size        
        pg.display.set_caption("Alien Invasion")
        self.stats=GameStats(self)#instance to store score
        self.sb=Scoreboard(self)
        self.ship=Ship(self)
        self.bullets=pg.sprite.Group()#Group is needed to store all existing bullets
        self.aliens=pg.sprite.Group()#Group is needed to store all existing aliens
        self._create_fleet()
        self.play_button=Button(self, 'Play')
        self.bg_color = (self.settings.bg_color)#Background color
        #Fullscreen mode. Temporary disabled
        #self.screen=pg.dispay.set_mode((0,0), pg.FULLSCREEN)
        #self.settings.screen_width=self.screen.get_rect().width
        #self.settings.screen_height=self.screen.get_rect().height

    
    
    def run_game(self):#Main loop for the game
        while True:#Watch the keyboard or mouse events
            self.check_events() 
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self.update_screen()

    
    def check_events(self):
        for event in pg.event.get():
                if event.type==pg.QUIT:
                    s.exit()
                elif event.type==pg.KEYDOWN:#Moving Ship
                    self._check_keydown_event(event) 
                elif event.type==pg.KEYUP:#Stop moving
                    self._check_keyup_event(event) 
                elif event.type==pg.MOUSEBUTTONDOWN:
                    mouse_pos=pg.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                                    
    
    def _check_keydown_event(self, event):#additional method is applied to optimise the code
        if event.key==pg.K_d:
            self.ship.moving_right=True
        elif event.key==pg.K_a:
            self.ship.moving_left=True
        elif event.key == pg.K_q:
            s.exit()
        elif event.key == pg.K_w:
            self._fire_bullet()
    
    def _check_keyup_event(self, event):#additional method is applied to optimise the code
        if event.key==pg.K_d:
            self.ship.moving_right=False
        if event.key==pg.K_a:
            self.ship.moving_left=False 

    def _fire_bullet(self):
        if len(self.bullets)<self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet) 

    def update_screen(self):
        self.screen.fill(self.bg_color)#Redraw screen after each step through the loop
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()  
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        pg.display.flip()#clean screen

    def _update_bullets(self):
        self.bullets.update()
        #remove old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        #check for collisions
        collisions = pg.sprite.groupcollide(self.bullets, self.aliens,True, True)
        if not self.aliens:
            #Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level +=1
            self.sb.prep_level()
        if collisions:
            for aliens in collisions.values():
                self.stats.score+=self.settings.alien_points*len(aliens)
            self.stats.score +=self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()
    
    

    def _create_fleet(self):
        alien=Alien(self)
        alien_width, alien_height=alien.rect.size

        ship_height=self.ship.rect.height
        available_space_y=self.settings.screen_height-(3*alien_height)-ship_height

        available_rows=available_space_y//(2*alien_height)

        available_space_x=self.settings.screen_width-2*alien_width
        number_aliens_x=available_space_x//(2*alien_width)

        #create a first row of aliens
        for row_number in range(available_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
            
    
    def _create_alien(self, alien_number, row_number):
        alien=Alien(self)
        alien_width, alien_height=alien.rect.size
        alien.x=alien_width+2*alien_width*alien_number
        alien.rect.x=alien.x
        alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
        self.aliens.add(alien)
    
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        #Alien-ship collision
        if pg.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1

    def _ship_hit(self):
        if self.stats.ships_left>0:
            self.stats.ships_left -=1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)#pause
        else:
            self.stats.game_active=False
            pg.mouse.set_visible(False)

    def _check_aliens_bottom(self):
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break   

    def _check_play_button (self, mouse_pos):
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active=True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_score()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pg.mouse.set_visible(False)                    
    
if __name__=='__main__':
    ai=AlienInvasion()
    ai.run_game()
