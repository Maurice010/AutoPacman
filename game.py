import pygame
import sys
from settings import *
from sprites import *
from layout import *

class Game:
    def __init__(self, width, height, title):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)

    def new(self):
        self.allSprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.food = pygame.sprite.Group()
        self.layout = Layout.getLayout()
        self.player = Player(self, self.layout.pac_pos[1], self.layout.pac_pos[0])
        self.getWalls(self.layout.walls)
        self.getFood(self.layout.food)

    def getWalls(self, walls):
        for x in range(len(walls)):
            for y in range(len(walls[0])):
                if walls[x][y] == True:
                    Wall(self, y, x)

    def getFood(self, food):
        for x in range(len(food)):
            for y in range(len(food[0])):
                if food[x][y] == True:
                    Food(self, y, x)

    def drawGrid(self):
        for x in range(0, width, tileSize):
            pygame.draw.line(self.screen, (255, 255, 255), (x, 0), (x, height))
        for y in range(0, height, tileSize):
            pygame.draw.line(self.screen, (255, 255, 255), (0, y), (width, y))

    def run(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(60) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def update(self):
        self.allSprites.update(self.dt, self.walls)

    def draw(self):
        self.screen.fill("black")
        self.drawGrid()
        self.allSprites.draw(self.screen)
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()

game = Game(width, height, title)
game.new()
while True:
    game.run()