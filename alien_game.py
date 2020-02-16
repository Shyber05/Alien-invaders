import sys
from time import sleep

import pygame as pg

from button import Button
from ship import Ship
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    '''Overall Class that will determine the game's aspects and behaviour'''

    def __init__(self):
        '''Initializes game and creates the games resources'''
        pg.init()
        pg.mixer.init()
        self.settings = Settings()

          # This allows us to play in fullscreen
        # self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        self.screen = pg.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption('Alien Invaders')

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)

        # Manages live bullets and aliens
        self.bullets = pg.sprite.Group() 
        self.aliens = pg.sprite.Group()

        self._create_fleet()

        # Makes the Play button.
        self.play_button = Button(self, 'Play')
        
    def play_game(self):
        '''This will start the actual game creating a loop'''
        running = True
        while running:

            self._check_events()
            if self.stats.game_active == True:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
            # Makes the most recent screen visable 
            pg.display.flip()


    def _check_events(self):
        '''Responds to keypresses and mouse clicks'''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                #This is used for Unix systems to close the window
                pg.display.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self._keydown_events(event)
            elif event.type == pg.KEYUP:
                self._keyup_events(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                self._check_play_button(mouse_pos)
        
    def _check_play_button(self, mouse_pos):
        '''Start a new game when the player clicks play'''
        clicked_button = self.play_button.rect.collidepoint(mouse_pos)
        if clicked_button and not self.stats.game_active:
            self._begin_new_instance()

           


    def _keydown_events(self, event):
        '''Responds to pushing down key strokes Moves the ship right, left, up, and down'''
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                self.ship.move_right = True
            elif event.key == pg.K_LEFT: 
                self.ship.move_left = True
            elif event.key == pg.K_SPACE:
                self._fire_bullet()
            elif event.key == pg.K_q:
                pg.display.quit()
                sys.exit()
            elif event.key == pg.K_p:
                self._begin_new_instance()

            '''Movement up and down'''
            # elif event.key == pg.K_UP:
            #     self.ship.move_up = True
            # elif event.key == pg.K_DOWN:
            #     self.ship.move_down = True
                        


    def _begin_new_instance(self):
        '''Starts a new instance of the game'''
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        #Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

        #Hides cursor once game starts
        pg.mouse.set_visible(False)


    def _keyup_events(self, event):
        '''
        Responds to releasing key strokes allowing the ship to stop
        Additional movement is also added to go up and down
        '''
        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                self.ship.move_right = False
            elif event.key == pg.K_LEFT:
                self.ship.move_left = False

        '''Movement up and down'''
            # elif event.key == pg.K_UP:
            #     self.ship.move_up = False
            # elif event.key == pg.K_DOWN:
            #     self.ship.move_down = False


    def _fire_bullet(self):
        '''Creates a new bullet and adds it to the bullets group'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        '''Updates the position of bullets and gets rid of old bullets'''
        self.bullets.update()
        
        # Deletes old bullets that disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._bullet_alien_collision()


    def _bullet_alien_collision(self):
        '''Checks to see if aliens are hit and updates score'''
        
        collision = pg.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collision:
            for aliens in collision.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Upgrade level
            self.stats.level += 1
            self.sb.prep_level()




    def _update_aliens(self):
        '''
        Updates the aliens positions, and
        checks to see if the fleet hits the edge
        '''
        self._check_fleet_edges()
        self.aliens.update()

        if pg.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            print('Ship hit!')

        # Checks if the aliens hit the bottom of screen
        self._check_aliens_bottom()



    def _check_aliens_bottom(self):
        '''Check if any aliens have reached the bottom of screen'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        '''Responds to player being hit by alien'''
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1 
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            pg.mouse.set_visible(True)

    def _check_fleet_edges(self):
        '''Respond if any aliens have reached an edge'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''Drop the entire fleet and change the fleet's direction'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_speed
        self.settings.fleet_direction *= -1




    def _update_screen(self):
        '''Updates images on the screen'''
        self.screen.fill(self.settings.bg_color)
        self.ship.blit()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draws the score info
        self.sb.show_score()

        #Draws the play button
        if not self.stats.game_active:
            self.play_button.draw_button()

        pg.display.flip()

    def _create_fleet(self):
        '''Creates the fleet of alien ships'''
        # Makes alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size                             
        available_space_x = self.settings.screen_width - (2 * alien_width)      
        number_of_ships_x = available_space_x // (2 * alien_width)              

        #Determine number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                            (3 * alien_height) - ship_height) 

        number_rows = available_space_y // (2 * alien_height)
        
        #Creates the full fleet of Alien ships
        for row_number in range(number_rows):
            for alien_number in range(number_of_ships_x):
                self._create_alien(alien_number, row_number)
        

    def _create_alien(self, alien_number, row_number):
            #Creates an alien and places it in a row (refactered)
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number              
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number   
            self.aliens.add(alien)


  

#This is only if the file is called directly
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.play_game()
