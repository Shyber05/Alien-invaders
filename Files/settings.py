class Settings:
    '''Class used to store all the settings for our Alien takeover.'''

    def __init__(self):
        '''Initialize the games static settings'''
        # Screen settings 
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230) # Grey
        

        self.ship_limit = 2 

              # Bullet settings
        self.bullet_height = 15
        self.bullet_color = (60,50,60)
        self.bullets_allowed = 3
        self.bullet_width = 5

        # Super bullet for testing 
        # self.bullet_width = 600

        #Alien Speed
        self.fleet_speed = 10


        # Speeds up the fleet per level
        self.speedup = 1.2 

        self.initialize_dynamic_settings()
        # How quickly the alien point values increase
        self.score_scale = 1.5


    def initialize_dynamic_settings(self):
        '''These settings change during the game'''
         #Ship settings
        self.ship_speed = 3.3 
        self.alien_speed = 1.5
        self.bullet_speed = 8.0

        #Scoring
        self.alien_points = 50

        # 1 represents to the right; -1 to the left
        self.fleet_direction = 1

        # Increased speed for testing
        # self.alien_speed = 70

    def increase_speed(self):
        '''Increases the speed setting'''
        self.ship_speed *= self.speedup
        self.bullet_speed *= self.speedup
        self.alien_speed *= self.speedup
