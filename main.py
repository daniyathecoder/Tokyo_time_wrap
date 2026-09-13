import pygame
import sys
from settings import *
from player import Player
from maps import LEVEL_1_MAP

class Tile(pygame.sprite.Sprite):
   def __init__(self,x,y):
      super().__init__()
      self.image = pygame.Surface((TILE_SIZE,TILE_SIZE))
      self.image.fill(GROUND_BROWN)
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y

class Game:
    def __init__(self):

      pygame.init()
      self.screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
      pygame.display.set_caption("Tokyo Time Wrap - PHASE 2 PHYSICS")
      self.clock=pygame.time.Clock()
      self.is_running =True

      #CREATING A SPRITE UPDATE TO EASILY DRAW UPODATES
      
      self.platforms = pygame.sprite.Group()
      self.all_sprites=pygame.sprite.Group()
      self.build_level()

    def build_level(self):
       #SCAN THROUGH THE MATRIUX IN MAPS.PY 
       for row_index,row in enumerate(LEVEL_1_MAP):
          for col_index,char in enumerate(row):
             x= col_index* TILE_SIZE
             y= row_index* TILE_SIZE

             #CREATE A SOLID PLATFORM
             if char in ['X','5']:
                tile = Tile(x,y)
                self.platforms.add(tile)
                self.all_sprites.add(tile)
       #put nobita near the left edge of the screen,just above the floor
       self.player =Player(100,100)
       self.all_sprites.add(self.player)

    def run(self):
       while self.is_running:
          self.handle_events()
          self.update()
          self.draw()
          self.clock.tick(FPS)
       pygame.quit()
       sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def update(self):
       #UPDATing the player entity and tel it where the floors are
       self.player.update(self.platforms)
       if self.player.rect.top > SCREEN_HEIGHT :
          self.reset_player()

    def reset_player(self):
       self.player.position.x =100
       self.player.position.y =100
       self.player.velocity.x = 0
       self.player.velocity.y =0
       self.player.rect.topleft =(100,100)  

    def draw(self):
       self.screen.fill(SKY_BLUE)

       #drawing everything inside the sprite group onto the game window
       self.all_sprites.draw(self.screen)

       pygame.display.flip()
if __name__ == "__main__":
   game = Game()
   game.run()       

