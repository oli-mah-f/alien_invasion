class Settings:
    '''to save and modify the game settings'''

    def __init__(self):
        '''initialize the game settings'''
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        # bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 100

        # aliens setting
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction = 1 means right; fleet_direction = -1 means left
        self.fleet_direction = 1

        # ship settings
        self.ship_speed = 4
        self.ship_limit = 3
