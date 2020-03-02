import pygame as pg
from pygame.sprite import Sprite
import settings

class Alien(Sprite):
    '''This class will represent the alien ships'''

    def __init__(self, ai_game):
        '''Initializing the alien ships and sets start position'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        self.image = pg.image.load('Images/alien_2.bmp')
        self.rect = self.image.get_rect()

        # This will set the start position for the alien fleet
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Stores the alien's exact horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        '''Moves alien ship right or left'''
        self.x += (self.settings.alien_speed *
                    self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        '''Returns True if aliens hit the edge'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
