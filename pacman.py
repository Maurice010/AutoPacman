import pygame
import os

class Layout:
    def __init__(self, walls, food, pac_pos):
        self.walls = walls
        self.food = food
        self.pac_pos = pac_pos

def getLayout():
    curdir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(curdir)
    f = open("defaultLayout.txt", "r")

    x = 0
    y = 0
    walls = []
    food = []
    pac_pos = (-1, -1)
    walls.append([])
    food.append([])
    
    while True:
        char = f.read(1)
        if not char:
            break

        if char == '\n':
            x += 1
            y = 0
            walls.append([])
            food.append([])
        elif char == '#':
            walls[x].append(True)
            food[x].append(False)
            y += 1
        elif char == '.':
            food[x].append(True)
            walls[x].append(False)
            y += 1
        elif char == 'P':
            pac_pos = (x, y)
            food[x].append(False)
            walls[x].append(False)
            y += 1
        else:
            food[x].append(False)
            walls[x].append(False)
            y += 1

    return Layout(walls, food, pac_pos)

def drawWalls(walls, sWidth, sHeight):
    x_size = 5
    y_size = 5

    for x in range(len(walls)):
        for y in range(len(walls[0])):
            if walls[x][y] == True:
                pygame.draw.rect(screen, "blue", pygame.Rect(y * 30 + sWidth, x * 30 + sHeight, x_size, y_size))

def drawFood(food, sWidth, sHeight):
    x_size = 5
    y_size = 5

    for x in range(len(food)):
        for y in range(len(food[0])):
            if food[x][y] == True:
                pygame.draw.rect(screen, "white", pygame.Rect(y * 30 + sWidth, x * 30 + sHeight, x_size, y_size))

temp = getLayout()

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

sWidth = screen.get_width() / 2
sHeight = screen.get_height() / 2

player_pos = pygame.Vector2(temp.pac_pos[1] * 30 + sWidth, temp.pac_pos[0] * 30 + sHeight)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    pygame.draw.circle(screen, "yellow", player_pos, 10)
    drawWalls(temp.walls, sWidth, sHeight)
    drawFood(temp.food, sWidth, sHeight)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()