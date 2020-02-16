import pygame as pg
import settings
from pygame.sprite import Sprite


class Ship(Sprite):
    '''A Class to manage our ships '''

    def __init__(self, ai_game):
        '''Initializes the ship and sets its start position'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Loads the ships image and gets its rectangle
        self.image = pg.image.load("images/ufo-1.bmp")
        self.rect = self.image.get_rect()

        #This will store the decimal value for the ship's position on the x and y axis
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Starts each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        #Flags to keep continous movement of the ship
        self.move_right = False
        self.move_left = False

        #These allow the ship to move up and down the screen
        # self.move_down = False
        # self.move_up = False


    def update(self):
        '''This will update the position of the ship based on the flags'''
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.ship_speed
        if self.move_left and self.rect.left > 0:
            self.rect.x -= self.settings.ship_speed

        ''' These are the movement for the ship to go up and down the screen '''
        # if self.move_up and self.rect.top > 0:
        #     self.rect.y -= self.settings.ship_speed
        # if self.move_down and self.rect.bottom < self.screen_rect.bottom:
        #     self.rect.y += self.settings.ship_speed
        

    def blit(self):
        '''Draw the ships at its current location'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''Centers the ship on screen'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)