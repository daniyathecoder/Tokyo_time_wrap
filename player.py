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

        self.position = pygame.math.Vector2(x,y)
        self.velocity = pygame.math.Vector2(0,0)

        self.speed=PLAYER_SPEED
        self.on_ground = False
    
    def handle_input(self): 
        self.velocity.x = 0
        
        #CHECK KEYS CURRENTLY HELD DOWN
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = self.speed
        #jumping(only if on ground)
    def jump(self):
        if self.on_ground:
            self.velocity.y= JUMP_FORCE

            self.on_ground = False

    def apply_gravity(self):
        #continually pulls the player down
        self.velocity.y += GRAVITY
        if self.velocity.y  > TERMINAL_VELOCITY:
            self.velocity.y = TERMINAL_VELOCITY

    def move_horizontal(self,platforms):
        self.position.x += self.velocity.x
        self.rect.x = round(self.position.x)

        # CHECK IF HITTING LEFT OR RIGHT SIDE OF PLATFORM
        collisions = pygame.sprite.spritecollide(self,platforms,False)
        for tile in collisions:
            if self.velocity.x>0 : #moving right
                self.rect.right = tile.rect.left
                self.position.x = self.rect.x
            elif self.velocity.x<0: #moving left
                self.rect.left = tile.rect.right
                self.position.x =self.rect.x

    def move_vertical(self,platforms):
        self.position.y += self.velocity.y
        self.rect.y = round(self.position.y)
        self.on_ground = False          
        #check if landing on top or hitting the ceiling
        collisions= pygame.sprite.spritecollide(self,platforms,False)  
        for tile in collisions:
            if self.velocity.y >0: #falling downward
                self.rect.bottom = tile.rect.top
                self.position.y =self.rect.y
                self.velocity.y =0
                self.on_ground =True

            elif self.velocity.y<0: #hitting the ceiling
                self.rect.top = tile.rect.bottom
                self.position.y = self.rect.y
                self.velocity.y =0    

    def update(self,platforms):
        self.handle_input()
        self.apply_gravity()
        # processing collisions one by one to avoid clipping though walls
        self.move_horizontal(platforms)
        self.move_vertical(platforms)


