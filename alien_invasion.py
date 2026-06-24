import sys
import pygame
from ship import Ship
from bullet import Bullet
from settings import Settings

class AlienInvasion:
    '''Overall class to manage game assets and behavior.'''

    def __init__(self):
        '''initialize the game'''
        pygame.init()
        self.clock = pygame.time.Clock() # game rate


        # define attribute: screen here bcs other funcs have to be able to modify the screen
        self.settings = Settings() # create an instance
        #custom display size
        """ self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        ) """
        # full screen display
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption('Alien Invasion')

        # self bcs Ship requires an instance of ai
        # this self here referes to the current ai instance
        self.ship = Ship(self)  

        # the group that holds the bullets
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        '''start the main loop of game'''

        while True:
            #keyboard and mouse events
            #give all events that happened since last while loop
            self._check_events()

            #update ship movement / position
            self.ship.update()

            # update each bullet position in the group
            self.bullets.update()
                
            # remove bullets that reach the top of screen
            for bullet in self.bullets.copy():
                 if bullet.rect.bottom <= 0:
                      self.bullets.remove(bullet)
            #print(len(self.bullets))

            # redraw the screen through each pass
            self._update_screen()
            
            #update game screen
            pygame.display.flip()
            #make the loop run 60 times per sec
            self.clock.tick(60) 

    # helper methods, leading with _
    def _check_events(self):
        '''responds to keyboard and mouse events'''
        for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    print('exiting')
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                     self._check_keydown_events(event)
                          
                elif event.type == pygame.KEYUP:
                     self._check_keyup_events(event)

    def _check_keydown_events(self, event):
         '''respnds to keypresses'''
         if event.key == pygame.K_RIGHT:
              self.ship.moving_right = True
         elif event.key == pygame.K_LEFT:
              self.ship.moving_left = True
         elif event.key == pygame.K_q:
              sys.exit()
         elif event.key == pygame.K_SPACE:
              self.fire_bullet()

    def _check_keyup_events(self, event):
         '''responds to keyy releases'''
         if event.key == pygame.K_RIGHT:
              self.ship.moving_right = False
         elif event.key == pygame.K_LEFT:
              self.ship.moving_left = False  

    def _update_screen(self):
         '''update images on the screen, and flip to the new screen'''
         self.screen.fill(self.settings.bg_color)
         self.ship.blitme()
         for bullet in self.bullets.sprites():
              bullet.draw_bullet()

    def fire_bullet(self):
         '''create a new bullet & add it to the group'''
         if len(self.bullets) <= self.settings.bullets_allowed:
            # create a bullet, give the bullet a reference to this game object
            # so bullet can find screen, settings, and ship position
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
         

# True: if the game is ran using this file
# False: if another file tries to start the game
# why? without line 29, if you imported this file elsewhere,
# it would immidiately launch the game; sth we may not want
# python runs the whole file when you import it
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

    