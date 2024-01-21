import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos_x, pos_y):
        # General info about the player
        pygame.sprite.Sprite.__init__(self, game.allSprites)
        self.game = game

        # Player position
        self.pos = pygame.math.Vector2(pos_x, pos_y) * tileSize
        self.directionVec = pygame.math.Vector2(0, 0)
        self.directionVec_temp = pygame.math.Vector2(0, 0)
        self.last_pos = self.pos
        self.next_pos = self.pos

        # Player movement
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.between_tiles = False

        # Player graphics
        self.images = []
        for i in range(1, 5):
            self.images.append(pygame.transform.scale(pygame.image.load(f'assets/pacman/{i}.png'), (tileSize, tileSize)))
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def updateDirection(self):
        if self.directionVec == (-1, 0):
            self.game.screen.blit(images[])

    def validDirection(self):
        x = int(self.rect.centerx // tileSize + self.directionVec_temp.x)
        y = int(self.rect.centery // tileSize + self.directionVec_temp.y)

        return not self.game.layout.walls[y][x]

    def get_keys(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.directionVec_temp = pygame.math.Vector2(-1, 0)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.directionVec_temp = pygame.math.Vector2(1, 0)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.directionVec_temp = pygame.math.Vector2(0, -1)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.directionVec_temp = pygame.math.Vector2(0, 1)

        if self.directionVec_temp != pygame.math.Vector2(0, 0) and not self.between_tiles and self.validDirection():
            self.directionVec = self.directionVec_temp
            current_tile = self.rect.centerx // tileSize, self.rect.centery // tileSize
            self.last_pos = pygame.math.Vector2(current_tile) * tileSize
            self.next_pos = self.last_pos + self.directionVec * tileSize
            self.between_tiles = True
        
        print(self.directionVec, self.directionVec_temp)
    
    def update(self, dt, walls):
        self.get_keys()

        if self.pos != self.next_pos:
            delta = self.next_pos - self.pos
            if delta.length() > (self.directionVec * playerSpeed * dt).length():
                self.pos += self.directionVec * playerSpeed * dt
                self.between_tiles = True
            else:
                self.pos = self.next_pos
                self.between_tiles = False
                
                if self.validDirection():
                    self.directionVec = self.directionVec_temp
                current_tile = self.rect.centerx // tileSize, self.rect.centery // tileSize
                self.last_pos = pygame.math.Vector2(current_tile) * tileSize
                self.next_pos = self.last_pos + self.directionVec * tileSize

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        if pygame.sprite.spritecollide(self, walls, False):
            self.pos = self.last_pos
            self.next_pos = self.last_pos
            self.directionVec = pygame.math.Vector2(0, 0)
            self.between_tiles = False
            
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, pos_x, pos_y):
        # General info about the wall
        self.groups = game.allSprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = pos_x
        self.y = pos_y
        
        # Wall graphics
        self.image = pygame.Surface((tileSize, tileSize))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * tileSize
        self.rect.y = pos_y * tileSize

class Food(pygame.sprite.Sprite):
     def __init__(self, game, pos_x, pos_y):
        self.groups = game.allSprites, game.food
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = pos_x
        self.y = pos_y

        self.image = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (tileSize // 2, tileSize // 2), foodRadius)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * tileSize
        self.rect.y = pos_y * tileSize