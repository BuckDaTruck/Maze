import pygame
import csv
import sys
from collections import deque
import heapq
import time

# Constants for colors
RED = (255, 0, 0)  # Start
GREEN = (0, 255, 0)  # End
DARK_GREY = (64, 64, 64)  # Top bar
BLACK = (0, 0, 0)  # Wall
WHITE = (255, 255, 255)  # Background
BLUE = (0, 0, 255)  # DFS Path
YELLOW = (255, 255, 0)  # BFS Path
CYAN = (0, 255, 255)  # Dijkstra Path
MAGENTA = (255, 0, 255)  # Final Path
ORANGE = (255, 165, 0)  # Current Point
PURPLE = (128, 0, 128)  # Backtracked Points

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
pygame.display.set_caption("Maze Auto Solver")
font = pygame.font.SysFont(None, 20)
clock = pygame.time.Clock()

# Draw the maze
def draw_maze(path=None, color=BLUE, algorithm_name="", final_path=None, current=None, backtracked=None, visited=None):
    screen.fill(WHITE)
    pygame.draw.rect(screen, DARK_GREY, (0, 0, width * CELL_SIZE, TOP_BAR_HEIGHT))
    algorithm_text = font.render(f"Algorithm: {algorithm_name}", True, BLACK)
    screen.blit(algorithm_text, (10, 10))

    for y in range(height):
        for x in range(width):
            # Draw start and end cells
            if y == 0 and x == 0:
                pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE + TOP_BAR_HEIGHT, CELL_SIZE, CELL_SIZE))
            elif y == height - 1 and x == width - 1:
                pygame.draw.rect(screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE + TOP_BAR_HEIGHT, CELL_SIZE, CELL_SIZE))
            elif final_path and (x, y) in final_path:
                pygame.draw.rect(screen, MAGENTA, (x * CELL_SIZE, y * CELL_SIZE + TOP_BAR_HEIGHT, CELL_SIZE, CELL_SIZE))
            elif visited and (x, y) in visited:
                pygame.draw.rect(screen, CYAN, (x * CELL_SIZE, y * CELL_SIZE + TOP_BAR_HEIGHT, CELL_SIZE, CELL_SIZE))
            elif current == (x, y):
                pygame.draw.rect(screen, ORANGE, (x * CELL_SIZE, y * CELL_SIZE + TOP_BAR_HEIGHT, CELL_SIZE, CELL_SIZE))
            elif backtracked and (x, y) in backtracked:
                pygame.draw.rect(screen, PURPLE, (x * CELL_SIZE, y * CELL_SIZE + TOP_BAR_HEIGHT, CELL_SIZE, CELL_SIZE))
            elif path and (x, y) in path:
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE + TOP_BAR_HEIGHT, CELL_SIZE, CELL_SIZE))
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
    pygame.image.save(screen, f"{algorithm_name}_overlay_solve.png")
    pygame.event.pump()

# DFS Algorithm
def dfs_solve():
    stack = [(0, 0)]
    visited = set()
    parent = {}  # To trace the path back
    moves = 0

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return None, float('inf')

        x, y = stack.pop()
        moves += 1
        if (x, y) in visited:
            continue
        visited.add((x, y))
        draw_maze(path=list(visited), color=BLUE, algorithm_name="Depth-First Search", current=(x, y), visited=visited)
        time.sleep(0.01)

        if (x, y) == (width - 1, height - 1):  # Reached the goal
            path = []
            while (x, y) is not None:
                path.append((x, y))
                if (x, y) in parent:  # Ensure we only try to unpack existing parent nodes
                    x, y = parent[(x, y)]
                else:
                    break
            path.reverse()
            draw_maze(path=path, color=MAGENTA, algorithm_name="Depth-First Search", final_path=path, visited=visited)
            pygame.image.save(screen, "DFS_solve.png")
            return path, moves

        for direction in [N, S, E, W]:
            if grid[y][x] & direction != 0:
                nx, ny = x + DX[direction], y + DY[direction]
                if (nx, ny) not in visited:
                    stack.append((nx, ny))
                    parent[(nx, ny)] = (x, y)

    return [], moves

# BFS Algorithm
def bfs_solve():
    queue = deque([(0, 0)])
    visited = set([(0, 0)])
    parent = {(0, 0): None}
    moves = 0
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return None, float('inf')

        x, y = queue.popleft()
        moves += 1
        draw_maze(list(visited), YELLOW, "Breadth-First Search", current=(x, y), visited=visited)
        if (x, y) == (width - 1, height - 1):
            path = []
            while (x, y) is not None:
                path.append((x, y))
                if parent[(x, y)] is not None:
                    x, y = parent[(x, y)]
                else:
                    break
            path.reverse()
            draw_maze(path, MAGENTA, "Breadth-First Search", final_path=path, visited=visited)
            pygame.image.save(screen, "BFS_solve.png")
            return path, moves
        for direction in [N, S, E, W]:
            if grid[y][x] & direction != 0:
                nx, ny = x + DX[direction], y + DY[direction]
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))
                    draw_maze(list(visited), YELLOW, "Breadth-First Search", current=(nx, ny))
                    pygame.display.update()
                    time.sleep(0.05)
    return [], moves

# Dijkstra's Algorithm
def dijkstra_solve():
    pq = [(0, (0, 0))]
    distances = {(0, 0): 0}
    parent = {(0, 0): None}
    visited = set()
    moves = 0
    while pq:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return None, float('inf')

        current_distance, (x, y) = heapq.heappop(pq)
        moves += 1
        draw_maze(list(visited), CYAN, "Dijkstra's Algorithm", current=(x, y), visited=visited)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if (x, y) == (width - 1, height - 1):
            path = []
            while (x, y) is not None:
                path.append((x, y))
                if (x, y) in parent and parent[(x, y)] is not None:
                    x, y = parent[(x, y)]
                else:
                    break
            path.reverse()
            draw_maze(path, MAGENTA, "Dijkstra's Algorithm", final_path=path, visited=visited)
            pygame.image.save(screen, "Dijkstra_solve.png")
            return path, moves
        for direction in [N, S, E, W]:
            if grid[y][x] & direction != 0:
                nx, ny = x + DX[direction], y + DY[direction]
                new_distance = current_distance + 1
                if (nx, ny) not in distances or new_distance < distances[(nx, ny)]:
                    distances[(nx, ny)] = new_distance
                    parent[(nx, ny)] = (x, y)
                    heapq.heappush(pq, (new_distance, (nx, ny)))
                    draw_maze(list(visited), CYAN, "Dijkstra's Algorithm", current=(nx, ny))
                    pygame.display.update()
                    time.sleep(0.05)
    return [], moves

# Left-Wall Following Algorithm
def left_wall_follow():
    x, y = 0, 0
    visited = []
    direction = E  # Start facing East
    moves = 0

    while (x, y) != (width - 1, height - 1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return None, float('inf')

        visited.append((x, y))
        draw_maze(path=visited, color=CYAN, algorithm_name="Left-Wall Follow", current=(x, y))
        time.sleep(0.05)

        # Check the wall to the left of the current direction
        left_direction = {E: N, N: W, W: S, S: E}[direction]
        if grid[y][x] & left_direction != 0:  # Can move left
            direction = left_direction
        elif grid[y][x] & direction == 0:  # Can't move forward
            direction = {E: S, S: W, W: N, N: E}[direction]  # Turn right
        # Move forward
        x, y = x + DX[direction], y + DY[direction]
        moves += 1

    visited.append((x, y))  # Add the last cell
    draw_maze(path=visited, color=MAGENTA, algorithm_name="Left-Wall Follow", final_path=visited)
    pygame.image.save(screen, "LeftWallFollow_solve.png")
    return visited, moves

# Right-Wall Following Algorithm
def right_wall_follow():
    x, y = 0, 0
    visited = []
    direction = E  # Start facing East
    moves = 0

    while (x, y) != (width - 1, height - 1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return None, float('inf')

        visited.append((x, y))
        draw_maze(path=visited, color=CYAN, algorithm_name="Right-Wall Follow", current=(x, y))
        time.sleep(0.05)

        # Check the wall to the right of the current direction
        right_direction = {E: S, S: W, W: N, N: E}[direction]
        if grid[y][x] & right_direction != 0:  # Can move right
            direction = right_direction
        elif grid[y][x] & direction == 0:  # Can't move forward
            direction = {E: N, N: W, W: S, S: E}[direction]  # Turn left
        # Move forward
        x, y = x + DX[direction], y + DY[direction]
        moves += 1

    visited.append((x, y))  # Add the last cell
    draw_maze(path=visited, color=MAGENTA, algorithm_name="Right-Wall Follow", final_path=visited)
    pygame.image.save(screen, "RightWallFollow_solve.png")
    return visited, moves

# Run the algorithms and generate a report
def run_solvers():
    results = []

    # Run DFS
    start_time = time.time()
    dfs_path, dfs_moves = dfs_solve()
    dfs_time = time.time() - start_time
    if dfs_path is None:
        results.append(("Depth-First Search", "DNF", float('inf'), float('inf')))
    else:
        results.append(("Depth-First Search", len(dfs_path), dfs_time, dfs_moves))

    time.sleep(1)

    # Run BFS
    start_time = time.time()
    bfs_path, bfs_moves = bfs_solve()
    bfs_time = time.time() - start_time
    if bfs_path is None:
        results.append(("Breadth-First Search", "DNF", float('inf'), float('inf')))
    else:
        results.append(("Breadth-First Search", len(bfs_path), bfs_time, bfs_moves))

    time.sleep(1)

    # Run Dijkstra
    start_time = time.time()
    dijkstra_path, dijkstra_moves = dijkstra_solve()
    dijkstra_time = time.time() - start_time
    if dijkstra_path is None:
        results.append(("Dijkstra's Algorithm", "DNF", float('inf'), float('inf')))
    else:
        results.append(("Dijkstra's Algorithm", len(dijkstra_path), dijkstra_time, dijkstra_moves))

    time.sleep(1)

    # Run Left-Wall Follow
    start_time = time.time()
    lwf_path, lwf_moves = left_wall_follow()
    lwf_time = time.time() - start_time
    if lwf_path is None:
        results.append(("Left-Wall Follow", "DNF", float('inf'), float('inf')))
    else:
        results.append(("Left-Wall Follow", len(lwf_path), lwf_time, lwf_moves))

    time.sleep(1)

    # Run Right-Wall Follow
    start_time = time.time()
    rwf_path, rwf_moves = right_wall_follow()
    rwf_time = time.time() - start_time
    if rwf_path is None:
        results.append(("Right-Wall Follow", "DNF", float('inf'), float('inf')))
    else:
        results.append(("Right-Wall Follow", len(rwf_path), rwf_time, rwf_moves))

    # Print report
    print("\nMaze Solving Report:")
    for name, length, duration, moves in results:
        print(f"{name}: Path Length = {length}, Time Taken = {duration:.2f} seconds, Moves Considered = {moves}")

# Display the maze and run solvers
run_solvers()

# Keep the window open
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
