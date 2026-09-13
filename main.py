import pygame
import sys
from settings import *
from player import Player
from level import Level
from camera import Camera

class Game:
 def __init__(self):

      pygame.init()
      self.screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
      pygame.display.set_caption("Tokyo Time Wrap - PHASE 3")
      self.clock=pygame.time.Clock()
      self.running =True
      self.current_era = 1
      self.level=Level(self.current_era)
      self.player=Player(100,100)
      self.camera= Camera()
      self.camera.set_world_width(self.level.width)
      self.all_sprites=pygame.sprite.Group()
      self.all_sprites.add(self.player)


 def run(self):
       while self.running:
          self.handle_events()
          self.update()
          self.draw()
          self.clock.tick(FPS)
       pygame.quit()
       sys.exit()

 def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.KEYDOWN:
               if event.key in (pygame.K_SPACE,pygame.K_w,pygame.K_UP): 
                  self.player.jump()  

 def update(self):
       #UPDATing the player entity and tel it where the floors are
       self.player.update(self.level.platforms)
       self.camera.update(self.player)
       if self.level.exit_desk is not None:
          if pygame.sprite.collide_rect(self.player,self.level.exit_desk):
             self.next_era()
       if self.player.rect.top > (self.level.height+200) :
          self.reset_player()

 def next_era(self):
    #already at final era
    if self.current_era >= 3:
       return
    #move to next era
    self.current_era +=1
    #build new level
    self.level.change_era(self.current_era)
    self.reset_player()
    self.camera.set_world_width(self.level.width)
    self.camera.x = 0


 def reset_player(self):
       self.player.position.x =100
       self.player.position.y =100
       self.player.velocity.x = 0
       self.player.velocity.y =0
       self.player.rect.topleft =(100,100)  
       self.player.on_ground = False
       self.camera.x =0

 def draw_background(self):
     if self.current_era == 1:
         self.screen.fill(FEUDAL_SKY)
     elif self.current_era ==2:
         self.screen.fill(MODERN_SKY)
     elif self.current_era==3:
         self.screen.fill(FUTURE_SKY)

 def draw(self):
       self.draw_background()
       self.level.draw(self.screen,self.camera)
       player_screen_rect = (self.camera.apply(self.player.rect))
       self.screen.blit(self.player.image,player_screen_rect)
       # update display
       pygame.display.flip()
if __name__ == "__main__":
   game = Game()
   game.run()       

