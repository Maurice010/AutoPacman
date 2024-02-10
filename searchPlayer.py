import pygame
from settings import *
from searchAlgorithms import *
from sprites import *

class HumanPlayer(Player):
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
    
    def update(self, dt, walls):
        self.get_keys()
        self.animatePlayer()
        self.eat()

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

class AutoPlayer(Player):
    def update(self, dt, walls):
        if not self.between_tiles and self.validDirection():
            if len(self.game.ans) != 0:
                self.directionVec_temp = self.game.ans.pop(0)
                
            self.directionVec = self.directionVec_temp
            current_tile = self.rect.centerx // tileSize, self.rect.centery // tileSize
            self.last_pos = pygame.math.Vector2(current_tile) * tileSize
            self.next_pos = self.last_pos + self.directionVec * tileSize
            self.between_tiles = True

        self.animatePlayer()
        self.eat()

        if self.pos != self.next_pos:
            delta = self.next_pos - self.pos
            if delta.length() > (self.directionVec * playerSpeed * dt).length():
                self.pos += self.directionVec * playerSpeed * dt
                self.between_tiles = True
            else:
                self.pos = self.next_pos
                self.directionVec_temp = pygame.math.Vector2(0, 0)
                self.between_tiles = False

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        if pygame.sprite.spritecollide(self, walls, False):
            self.pos = self.last_pos
            self.next_pos = self.last_pos
            self.directionVec = pygame.math.Vector2(0, 0)
            self.between_tiles = False
            
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y