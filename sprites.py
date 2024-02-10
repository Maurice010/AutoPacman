import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos_x, pos_y):
        # General info about the player
        pygame.sprite.Sprite.__init__(self, game.allSprites)
        self.game = game

        # Player movement
        self.pos = pygame.math.Vector2(pos_x, pos_y) * tileSize
        self.directionVec = pygame.math.Vector2(0, 0)
        self.directionVec_temp = pygame.math.Vector2(0, 0)
        self.last_pos = self.pos
        self.next_pos = self.pos
        self.between_tiles = False

        # Player graphics
        self.images = []
        for i in range(1, 5):
            self.images.append(pygame.transform.scale(pygame.image.load(f'assets/pacman/{i}.png'), (32, 32)))
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def animatePlayer(self):
        if self.directionVec == pygame.math.Vector2(1, 0):
            self.image = self.images[self.game.animationCount // 5]
        elif self.directionVec == pygame.math.Vector2(-1, 0):
            self.image = pygame.transform.flip(self.images[self.game.animationCount // 5], True, False)
        elif self.directionVec == pygame.math.Vector2(0, -1):
            self.image = pygame.transform.rotate(self.images[self.game.animationCount // 5], 90)
        elif self.directionVec == pygame.math.Vector2(0, 1):
            self.image = pygame.transform.rotate(self.images[self.game.animationCount // 5], 270)

    def validDirection(self):
        x = int(self.rect.centerx // tileSize + self.directionVec_temp.x)
        y = int(self.rect.centery // tileSize + self.directionVec_temp.y)

        return not self.game.layout.walls[y][x]
    
    def eat(self):
        if pygame.sprite.spritecollide(self, self.game.food, True):
            self.game.score += 10

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