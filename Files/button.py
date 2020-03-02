import pygame.font 

class Button:
    '''Represents the start button for our game'''

    def __init__(self,ai_game, msg):
        '''Initializes the buttons attributes'''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # These are the buttons dimensions
        self.width, self.height = 150, 60
        self.button_color = (0, 25, 0)
        self.text_color = (255, 255, 255)
        # Arguments say (use default font) and (48 is the size)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and centers it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #buttons message
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        '''Turns msg into a image and centers the text'''
        self.msg_image = self.font.render(msg, True, self.text_color,
                            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draws message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)