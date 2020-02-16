import pygame as pg
from pygame.sprite import Sprite


class Bullet(Sprite):
    '''This class will control the bullets fired from the ship'''

    def __init__(self,ai_game):
        '''This creates a bullet at the ships position'''
        #The super inherits properties from the Sprite class
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet at (0,0) and then set its position to the ship
        # Rect(left, top, width, height) --> Rect
        self.rect = pg.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # This will store the bullet's position as a decimal
        self.y = float(self.rect.y)

    def update(self):
        '''Moves the bullet up the screen'''
        # Updates the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        # Updates the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        '''Draws the bullet to the screen'''
        pg.draw.rect(self.screen,self.color,self.rect)
