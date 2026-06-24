import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''to manage bullets fired from te top of ship'''

    def __init__(self, ai_game):
        '''initialize bullet objects at the ship's current position'''
        #why ai_game as argument? if u don't, the class needs a long param list [screen, settings, ship]
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # creat a bullet rect at (0,0)
        self.rect = pygame.Rect(0,0, 
                                self.settings.bullet_width, 
                                self.settings.bullet_height)
        # set the position of bullet rect to the top of ship (current position)
        self.rect.midtop = ai_game.ship.rect.midtop

        # bullet's y position, as it is needed later to adjust bullet speed
        self.y = float(self.rect.y)

    def update(self):
        '''move the bullet up the screen'''
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        '''draw bullet on screen'''
        pygame.draw.rect(self.screen, self.color, self.rect)
