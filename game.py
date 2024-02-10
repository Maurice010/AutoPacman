import pygame
import sys
from settings import *
from sprites import *
from layout import *
from searchAlgorithms import *
from searchPlayer import *

class Stopwatch:
    def __init__(self, screen):
        self.font = pygame.font.SysFont("Comic Sans MS", 15)
        self.screen = screen
    
    def showTime(self, time):
        time_str =  str(int(time * 10) / 10)
        text = self.font.render(f"Time: {time_str}", 1, (255,0,0))
        self.screen.blit(text, (4, 4))

class Game:
    def __init__(self, width, height, title):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)

        self.time_seconds = 0
        self.stopwatch = Stopwatch(self.screen)

        self.paused = False
        self.grid_enabled = True

        self.animationCount = 0 # Zmienna uzywana do animacji Pacmana
        self.score = 0 # Zmienna przechowujaca zdobyte punkty

    def adjustScreen(self):
        newWidth = len(self.layout.walls[0]) * 32
        newHeight = len(self.layout.walls) * 32
        self.screen = pygame.display.set_mode((newWidth, newHeight))

    def new(self):
        # Wczytywanie elementow i ich grupowanie
        self.allSprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.food = pygame.sprite.Group()
        self.layout = Layout.getLayout() # Dostosowanie szerokosci ekranu do mapy
        self.adjustScreen()
        self.getWalls(self.layout.walls)
        self.getFood(self.layout.food)
        
        # Odkomentowanie tej wersji zamiast tej niżej da kontrole uzytkownikowi nad Pacmanem
        # self.player = HumanPlayer(self, self.layout.pac_pos[1], self.layout.pac_pos[0])

        # Automatyczny Pacman
        self.player = AutoPlayer(self, self.layout.pac_pos[1], self.layout.pac_pos[0])
        self.searchProblem = Problem(self)
        self.ans = DFS(self.searchProblem)

    def getWalls(self, walls):
        for x in range(len(walls)):
            for y in range(len(walls[x])):
                if walls[x][y] == True:
                    Wall(self, y, x)

    def getFood(self, food):
        for x in range(len(food)):
            for y in range(len(food[x])):
                if food[x][y] == True:
                    Food(self, y, x)

    def drawGrid(self):
        for x in range(0, width, tileSize):
            pygame.draw.line(self.screen, (255, 255, 255), (x, 0), (x, height))
        for y in range(0, height, tileSize):
            pygame.draw.line(self.screen, (255, 255, 255), (0, y), (width, y))

    def gameOver(self):
        if len(self.food) == 0:
            print("Score: ", self.score)
            self.paused = True
            
    def run(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(60) / 1000
            self.events()
            if not self.paused:
                if self.animationCount < 19:
                    self.animationCount += 1
                else:
                    self.animationCount = 0
                self.update()
                self.draw()
                self.time_seconds += self.dt



    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_g:
                    self.grid_enabled = not self.grid_enabled

    def update(self):
        self.allSprites.update(self.dt, self.walls)
        self.gameOver()

    def draw(self):
        self.screen.fill("black")
        if self.grid_enabled:
            self.drawGrid()
        self.allSprites.draw(self.screen)
        self.stopwatch.showTime(self.time_seconds)
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()

game = Game(width, height, title)
game.new()
while True:
    game.run()