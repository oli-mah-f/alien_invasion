import pygame

class Ship:
    '''class to manage the ship'''

    def __init__(self, ai_game):
        '''initialize the ship and its start position'''
        
        self.screen = ai_game.screen #access to game window
        self.screen_rect = ai_game.screen.get_rect() # creat rectangular obj

        self.settings = ai_game.settings

        #load ship img and get its rectangular
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #align midbottom of img_rect with midbottom of screen_rect
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # flag that controls right/left movements of ship; initially not moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''updates ship's position based on movement flags'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed # based on ship's x value, not the rect

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x
    
    def blitme(self):
        '''draw the ship at the mid bottom'''
        #set the top left corner of image to top left corner of self.rect
        self.screen.blit(self.image, self.rect)


