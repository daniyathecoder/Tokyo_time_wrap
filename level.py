import pygame
from settings import *
from maps import ERA_MAPS

class Tile(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE,TILE_SIZE))
        self.image.fill(color)
        self.rect=self.image.get_rect(topleft=(x,y))

class ExitDesk(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image =pygame.Surface((TILE_SIZE,TILE_SIZE))
        self.fill(EXIT_COLOR)
        self.rect = self.image.get_rec(topleft = (x,y))

class Level:
    def __init__(self,era):
        self.current_era = era
        self.platforms = pygame.sprite.Group()
        self.exit_desk = None
        self.width = 0
        self.height =0
        self.build_level()

    def get_ground_color(self):
        if self.current_era ==1:
            return FEUDAL_GROUND
        if self.current_era == 2:
            return MODERN_GROUND
        if self.current_era ==3 :
            return FUTURE_GROUND

        return FEUDAL_GROUND
            
    def build_level(self):
        self.platforms.empty()
        self.exit_desk = None
        map_data = ERA_MAPS[self.current_era]
        self.width = (len (map_data[0])* TILE_SIZE)
        self.height = (len(map_data)*TILE_SIZE)
        ground_color = (self.get_ground_color())
        for row_index,row in enumerate(map_data):
            for col_index,tile_type in enumerate(row):
                x= col_index*TILE_SIZE
                y= row_index*TILE_SIZE
                #SOLID BLOXCKS
                if tile_type in ("X","5"):
                    tile = Tile(x,y,ground_color)
                    self.platforms.add(tile)
                elif tile_type=="D":
                    self.exit_desk=ExitDesk(x,y)
    def change_era(self,new_era):
        if new_era not in ERA_MAPS :
            return False
        self.current_era = new_era
        self.build_level()
        return True

    def draw(self,screen,camera):
        #draw every platform
        for tile in self.platforms:
            screen_rect = camera.apply(tile.rect) 
            screen.blit(tile.image,screen_rect)

        #draw exit desk 
        if self.exit_desk:
            screen_rect = camera.apply(self.exit_desk.rect)
            screen.blit(self.exit_desk.image,screen_rect)                       

