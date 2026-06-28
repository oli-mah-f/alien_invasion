class Settings:
    '''to save and modify the game settings'''

    def __init__(self):
        '''initialize the game settings'''
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 100

        # aliens setting
        self.fleet_drop_speed = 30

        # ship settings
        self.ship_limit = 3

        # scoring settings
        self.alien_points = 10

        self.initialize_dynamic_settings()

        # how much to speed up as player levels up
        self.speedup_scale = 1.3
        # how much to increase alien point value as player levels up
        self.score_scale = 1.5



    def initialize_dynamic_settings(self):
        '''initialize speeds; these will change in value later in game as player levels up'''
        self.bullet_speed = 2.0
        self.alien_speed = 1.0
        self.ship_speed = 4
        # fleet_direction = 1 means right; fleet_direction = -1 means left
        self.fleet_direction = 1

    def increase_speed(self):
        '''speed up the game & increase alien point values as player levels up'''
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)