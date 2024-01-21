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