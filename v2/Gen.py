import pygame
import random
import sys
import time
import csv

# Constants for colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Directions and their movements
N, S, E, W = 1, 2, 4, 8
DX = { E: 1, W: -1, N: 0, S: 0 }
DY = { E: 0, W: 0, N: -1, S: 1 }
OPPOSITE = { E: W, W: E, N: S, S: N }

# Prompt for default or custom settings
use_defaults = input("Would you like to use default settings? (y/n): ").lower()
if use_defaults == 'y' or use_defaults == '':
    filename = "maze"
    width, height = 10, 10
else:
    filename = input("Enter filename for the maze: ") or "maze"
    width = int(input("Enter maze width: ") or 20)
    height = int(input("Enter maze height: ") or 20)

grid = [[0 for _ in range(width)] for _ in range(height)]

# Pygame setup
pygame.init()
CELL_SIZE = 20
screen = pygame.display.set_mode((width * CELL_SIZE, height * CELL_SIZE))
pygame.display.set_caption("Maze Generator")
clock = pygame.time.Clock()

# Draw the maze
def draw_maze():
    screen.fill(WHITE)
    for y in range(height):
        for x in range(width):
            # Draw walls
            if grid[y][x] & N == 0:
                pygame.draw.line(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE), ((x + 1) * CELL_SIZE, y * CELL_SIZE), 2)
            if grid[y][x] & S == 0:
                pygame.draw.line(screen, BLACK, (x * CELL_SIZE, (y + 1) * CELL_SIZE), ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE), 2)
            if grid[y][x] & W == 0:
                pygame.draw.line(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE), (x * CELL_SIZE, (y + 1) * CELL_SIZE), 2)
            if grid[y][x] & E == 0:
                pygame.draw.line(screen, BLACK, ((x + 1) * CELL_SIZE, y * CELL_SIZE), ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE), 2)
            
            # Draw start and end cells
            if y == 0 and x == 0:
                pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if y == height - 1 and x == width - 1:
                pygame.draw.rect(screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()

# Hunt and Kill algorithm functions
def walk(x, y):
    directions = [N, S, E, W]
    random.shuffle(directions)
    for dir in directions:
        nx, ny = x + DX[dir], y + DY[dir]
        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 0:
            grid[y][x] |= dir
            grid[ny][nx] |= OPPOSITE[dir]
            return nx, ny
    return None

def hunt():
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 0:
                neighbors = []
                if y > 0 and grid[y-1][x] != 0:
                    neighbors.append(N)
                if x > 0 and grid[y][x-1] != 0:
                    neighbors.append(W)
                if x + 1 < width and grid[y][x+1] != 0:
                    neighbors.append(E)
                if y + 1 < height and grid[y+1][x] != 0:
                    neighbors.append(S)

                if neighbors:
                    dir = random.choice(neighbors)
                    nx, ny = x + DX[dir], y + DY[dir]
                    grid[y][x] |= dir
                    grid[ny][nx] |= OPPOSITE[dir]
                    return x, y
    return None

# Main loop for generating the maze
x, y = random.randint(0, width - 1), random.randint(0, height - 1)
while True:
    draw_maze()
    pygame.event.pump()
    time.sleep(0.001)

    result = walk(x, y)
    if result:
        x, y = result
    else:
        result = hunt()
        if result:
            x, y = result
        else:
            break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Display the final maze
draw_maze()

# Export maze as PNG
def save_maze_as_png(filename):
    pygame.image.save(screen, f"{filename}.png")

save_maze_as_png(filename)

# Export maze as CSV
def save_maze_as_csv(filename):
    with open(f"{filename}.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(grid)

save_maze_as_csv(filename)

# Keep the window open to display the final maze
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

