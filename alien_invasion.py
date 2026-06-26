import sys
import pygame
from time import sleep # to pause the game when ship collides aliens
from ship import Ship
from alien import Alien
from bullet import Bullet
from settings import Settings
from game_stats import GameStats

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

        # create an instance to store game stats
        self.stats = GameStats(self)

        # self bcs Ship requires an instance of ai
        # this self here referes to the current ai instance
        self.ship = Ship(self)  

        # the group that holds the bullets/ aliens
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # creat alien instances
        self._creat_fleet()

        # start game if this is active
        self.game_active = True


    def run_game(self):
        '''start the main loop of game'''

        while True:
            #keyboard and mouse events
            #give all events that happened since last while loop
            self._check_events()

            if self.game_active:
                    #update ship movement / position
                    self.ship.update()

                    # update each bullet position in the group
                    self._update_bullets()

                    # update aliens position
                    self._update_aliens()
                
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
         # draw each element in group at defined position by rect attribute
         self.aliens.draw(self.screen)
         for bullet in self.bullets.sprites():
              bullet.draw_bullet()

    def fire_bullet(self):
         '''create a new bullet & add it to the group'''
         if len(self.bullets) <= self.settings.bullets_allowed:
            # create a bullet, give the bullet a reference to this game object
            # so bullet can find screen, settings, and ship position
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
         '''update bullet position, remove old bullets'''
         self.bullets.update()
         for bullet in self.bullets.copy():
              if bullet.rect.bottom <= 0: 
                   self.bullets.remove(bullet)

         self._check_bullet_alien_collisions()
    

    def _check_bullet_alien_collisions(self):
         '''responds to alien-bullet collision'''
         # check if bullet hits alien --> remove both 
         collisions = pygame.sprite.groupcollide(
               self.bullets, self.aliens, True, True
          )
         
         # if no fleet, creat a new fleet
         if not self.aliens:
              # destroy existing bullets, creat new fleet
              self.bullets.empty()
              self._creat_fleet()


    def _creat_fleet(self):
         '''creat the fleet of aliens'''
         # add one alien; keep adding until no room left
         alien = Alien(self)
         # space btwn aliens = 1 alien width, 1 alien height
         alien_width = alien.rect.width
         alien_height = alien.rect.height

         current_x, current_y = alien_width, alien_height
         while current_y < (self.settings.screen_height - 3*alien_height):
              while current_x < (self.settings.screen_width - 2*alien_width):
                   self._creat_alien(current_x, current_y)
                   current_x += 2*alien_width

              # finished row, reset x, increase y 
              current_x = alien_width
              current_y += 2*alien_height
          

    def _creat_alien(self, x_position, y_position):
         '''create an alien and place it in the row'''
         new_alien = Alien(self)
         new_alien.x = x_position # speed
         new_alien.rect.x = x_position
         new_alien.rect.y = y_position
         self.aliens.add(new_alien)

    def _update_aliens(self):
         '''check if fleet on edge, then update each alien's position in fleet'''
         self._check_fleet_edges()
         self.aliens.update()

         # check for alien-ship collision
         if pygame.sprite.spritecollideany(self.ship, self.aliens):
              self._ship_hit()
          
              # check for collision between alien and bottom of screen
              self._check_aliens_bottom()

              

    def _check_fleet_edges(self):
         '''drop y position if any one alien hits either edges'''
         for alien in self.aliens.sprites():
              if alien.check_edges():
                   self._change_fleet_direction()
                   break 
         
    def _change_fleet_direction(self):
         '''drop y position of whole fleet & chnage direction'''
         for alien in self.aliens.sprites():
              alien.rect.y += self.settings.fleet_drop_speed
         self.settings.fleet_direction *= -1

    
    def _ship_hit(self):
         '''respond to ship-alien collision'''
         if self.stats.ships_left > 0:
               # decrese the numebr of ships left
               self.stats.ships_left -= 1

               # remove remaining bullets & aliens
               self.bullets.empty()
               self.aliens.empty()

               # create new fleet & center the ship
               self._creat_fleet()
               self.ship.center_ship()
               # pause
               sleep (0.5)
         else:
              self.game_active = False
              



    def _check_aliens_bottom(self):
         '''check if any alien reach screen bottom'''
         for alien in self.aliens.sprites():
              if alien.rect.bottom >= self.settings.screen_height:
                   # treat this as if alien collided ship
                   self._ship_hit()
                   break     
           
            
         

# True: if the game is ran using this file
# False: if another file tries to start the game
# why? without line 29, if you imported this file elsewhere,
# it would immidiately launch the game; sth we may not want
# python runs the whole file when you import it
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

    