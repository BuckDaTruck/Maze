import pygame
import csv
import sys
from collections import deque

# Constants for colors
RED = (255, 0, 0)  # Start
GREEN = (0, 255, 0)  # End
DARK_GREY = (64, 64, 64)  # Top bar
BLACK = (0, 0, 0)  # Wall
WHITE = (255, 255, 255)  # Background
ORANGE = (255, 165, 0)  # Filled path

# Directions and their movements
N, S, E, W = 1, 2, 4, 8
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}

# Load the CSV file
def load_maze_from_csv(filename):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        grid = [list(map(int, row)) for row in reader]
    return grid

# Pygame setup
pygame.init()
filename = input("Enter the CSV filename to load the maze (including .csv extension) [default: maze.csv]: ") or "maze.csv"
grid = load_maze_from_csv(filename)

height = len(grid)
width = len(grid[0]) if height > 0 else 0
CELL_SIZE = 20
TOP_BAR_HEIGHT = 40
screen = pygame.display.set_mode((width * CELL_SIZE, height * CELL_SIZE + TOP_BAR_HEIGHT))
pygame.display.set_caption("Maze Player")
font = pygame.font.SysFont(None, 20)
clock = pygame.time.Clock()

# Draw the maze
def draw_maze():
    screen.fill(WHITE)
    pygame.draw.rect(screen, DARK_GREY, (0, 0, width * CELL_SIZE, TOP_BAR_HEIGHT))
    filled_count_text = font.render(f"Squares Filled: {len(path)}", True, BLACK)
    screen.blit(filled_count_text, (10, 10))
    restart_text = font.render("Restart", True, BLACK)
    restart_rect = restart_text.get_rect(topleft=(width * CELL_SIZE - 100, 10))
    screen.blit(restart_text, restart_rect)

    for y in range(height):
        for x in range(width):
            # Draw start and end cells
            if y == 0 and x == 0:
                pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE + TOP_BAR_HEIGHT, CELL_SIZE, CELL_SIZE))
            elif y == height - 1 and x == width - 1:
                pygame.draw.rect(screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE + TOP_BAR_HEIGHT, CELL_SIZE, CELL_SIZE))
            elif (x, y) in path:
                pygame.draw.rect(screen, ORANGE, (x * CELL_SIZE, y * CELL_SIZE + TOP_BAR_HEIGHT, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE + TOP_BAR_HEIGHT, CELL_SIZE, CELL_SIZE))
            
            # Draw walls
            if grid[y][x] & N == 0:
                pygame.draw.line(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE + TOP_BAR_HEIGHT), ((x + 1) * CELL_SIZE, y * CELL_SIZE + TOP_BAR_HEIGHT), 2)
            if grid[y][x] & S == 0:
                pygame.draw.line(screen, BLACK, (x * CELL_SIZE, (y + 1) * CELL_SIZE + TOP_BAR_HEIGHT), ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE + TOP_BAR_HEIGHT), 2)
            if grid[y][x] & W == 0:
                pygame.draw.line(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE + TOP_BAR_HEIGHT), (x * CELL_SIZE, (y + 1) * CELL_SIZE + TOP_BAR_HEIGHT), 2)
            if grid[y][x] & E == 0:
                pygame.draw.line(screen, BLACK, ((x + 1) * CELL_SIZE, y * CELL_SIZE + TOP_BAR_HEIGHT), ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE + TOP_BAR_HEIGHT), 2)

    pygame.display.flip()

# Check if the maze is completed
def check_maze_completion():
    # Use BFS to check if there is a valid path from start to finish
    start = (0, 0)
    end = (width - 1, height - 1)
    if start not in path or end not in path:
        return False

    queue = deque([start])
    visited = set([start])

    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            return True

        for direction in [N, S, E, W]:
            if grid[y][x] & direction != 0:  # Check if there is a passage in this direction
                nx, ny = x + DX[direction], y + DY[direction]
                if (nx, ny) in path and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))

    return False

path = set([(0, 0), (width - 1, height - 1)])

# Display the maze
draw_maze()

# Automatically add start and end points to the path
path.add((0, 0))
path.add((width - 1, height - 1))

# Allow user to click and draw path
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if mouse_y < TOP_BAR_HEIGHT:
                # Check if the restart button is clicked
                if width * CELL_SIZE - 100 <= mouse_x <= width * CELL_SIZE - 20:
                    path.clear()
            else:
                grid_x, grid_y = mouse_x // CELL_SIZE, (mouse_y - TOP_BAR_HEIGHT) // CELL_SIZE
                if 0 <= grid_x < width and 0 <= grid_y < height:
                    if (grid_x, grid_y) in path:
                        path.remove((grid_x, grid_y))
                    else:
                        path.add((grid_x, grid_y))

    # Redraw the maze and the path
    draw_maze()

    # Check if the maze is completed
    if check_maze_completion():
        print("Congratulations! You have completed the maze!")
        pygame.quit()
        sys.exit()
