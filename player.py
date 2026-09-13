import pygame 
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()

        #CREATING PLAYER(A SOLID RECTANGULAR BOX)
        self.image=pygame.Surface((PLAYER_WIDTH,PLAYER_HEIGHT))
        self.image.fill(DORAEMON_BLUE)

        #DEFINING ITS PHYSICAL POSITION
        self.rect=self.image.get_rect(topleft=(x,y))

        
        # tracking precise floating positioning using numbers
        self.pos_x = x
        self.pos_y = y
        self.rect.x =int(self.pos_x)
        self.rect.y = int(self.pos_y)

        # movement speeds
        self.velocity_x =0
        self.velocity_y = 0
        self.speed=5
        self.on_ground = False



        
    def handle_input(self): 
        self.velocity_x = 0
        
        #CHECK KEYS CURRENTLY HELD DOWN
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed
        #jumping(only if on ground)
        if (keys[pygame.K_LEFT] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.velocity_y = JUMP_FORCE
            self.on_ground = False

    def apply_gravity(self):
        #continually pulls the player down
        self.velocity_y += GRAVITY
        if self.velocity_y  > TERMINAL_VELOCITY:
            self.velocity_x = TERMINAL_VELOCITY

    def check_horizontal_collisions(self,platforms):
        self.pos_x += self.velocity_x
        self.rect.x = int(self.pos_x)

        # CHECK IF HITTING LEFT OR RIGHT SIDE OF PLATFORM
        hits= pygame.sprite.spritecollide(self,platforms,False)
        for tile in hits:
            if self.velocity_x>0 : #moving right
                self.rect.right = tile.rect.left
                self.pos_x = self.rect.x
            elif self.velocity_x<0: #moving left
                self.rect.left = tile.rect.right
                self.pos_x =self.rect.x

    def check_vertical_collisions(self,platforms):
        self.pos_y += self.velocity_y
        self.rect.y = int(self.pos_y)
        self.on_ground = False          
        #check if landing on top or hitting the ceiling
        hits= pygame.sprite.spritecollide(self,platforms,False)  
        for tile in hits:
            if self.velocity_y >0: #falling downward
                self.rect.bottom = tile.rect.top
                self.pos_y =self.rect.y
                self.velocity_y =0
                self.on_ground =True

            elif self.velocity_y<0: #hitting the ceiling
                self.rect.top = tile.rect.bottom
                self.pos_y = self.rect.y
                self.velocity_y =0    

    def update(self,platforms):
        self.handle_input()
        self.apply_gravity()
        # processing collisions one by one to avoid clipping though walls
        self.check_horizontal_collisions(platforms)
        self.check_vertical_collisions(platforms)


