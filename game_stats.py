class GameStats:
    '''track statistics for the game'''

    def __init__(self, ai_game):
        '''initialize statistics'''
        self.settings = ai_game.settings
        self.reset_stats()

        self.score = 0
        self.level = 1

        # never reset high score
        self.high_score = 0


    def reset_stats(self):
        '''initialize statistics that can change during the game'''
        self.ships_left = self.settings.ship_limit