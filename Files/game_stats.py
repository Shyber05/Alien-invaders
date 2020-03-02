
class GameStats:
    '''Tracks the in game stats'''

    def __init__(self , ai_game):
        '''Initializes the stats'''
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False

        #High score
        self.high_score = 0 

    def reset_stats(self):
        '''Initializes stats that change throughout the game'''
        self.ships_left = self.settings.ship_limit 
        self.score = 0
        self.level = 1


