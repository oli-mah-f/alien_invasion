import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''to represent a single alien'''

    def __init__(self, ai_game):
        '''intialize an alien and set its staring position'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #start each alien near top left screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x) # speed

    def update(self):
        '''move alien right or left'''
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
        
    def check_edges(self):
        '''return true if alien at the screen edge'''
        screen_rect = self.screen.get_rect()
        if (self.rect.right >= screen_rect.right) or (self.rect.left <= 0):
            return True
        else: return False