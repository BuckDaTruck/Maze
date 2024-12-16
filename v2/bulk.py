import pygame
import random
import sys
import csv
import os
import time
from collections import deque
import heapq

# Constants for directions
N, S, E, W = 1, 2, 4, 8
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}
OPPOSITE = {E: W, W: E, N: S, S: N}

# Maze generation function
def generate_maze(width, height):
    grid = [[0 for _ in range(width)] for _ in range(height)]

    def walk(x, y):
        directions = [N, S, E, W]
        random.shuffle(directions)
        for direction in directions:
            nx, ny = x + DX[direction], y + DY[direction]
            if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 0:
                grid[y][x] |= direction
                grid[ny][nx] |= OPPOSITE[direction]
                walk(nx, ny)

    walk(random.randint(0, width - 1), random.randint(0, height - 1))
    return grid

# Save maze to CSV file
def save_maze_to_csv(grid, folder, filename):
    filepath = os.path.join(folder, filename)
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(grid)

# Load maze from CSV file
def load_maze_from_csv(filepath):
    with open(filepath, mode='r') as file:
        reader = csv.reader(file)
        return [list(map(int, row)) for row in reader]

# Solver algorithms
def dfs_solve(grid):
    height, width = len(grid), len(grid[0])
    stack = [(0, 0)]
    visited = set()
    parent = {}

    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if (x, y) == (width - 1, height - 1):
            path = []
            while (x, y) is not None:
                path.append((x, y))
                x, y = parent.get((x, y), None)
            return path[::-1]

        for direction in [N, S, E, W]:
            if grid[y][x] & direction:
                nx, ny = x + DX[direction], y + DY[direction]
                if (nx, ny) not in visited:
                    stack.append((nx, ny))
                    parent[(nx, ny)] = (x, y)

    return []

def bfs_solve(grid):
    height, width = len(grid), len(grid[0])
    queue = deque([(0, 0)])
    visited = set([(0, 0)])
    parent = {(0, 0): None}

    while queue:
        x, y = queue.popleft()

        if (x, y) == (width - 1, height - 1):
            path = []
            while (x, y) is not None:
                path.append((x, y))
                x, y = parent.get((x, y), None)
            return path[::-1]

        for direction in [N, S, E, W]:
            if grid[y][x] & direction:
                nx, ny = x + DX[direction], y + DY[direction]
                if (nx, ny) not in visited:
                    queue.append((nx, ny))
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)

    return []

def dijkstra_solve(grid):
    height, width = len(grid), len(grid[0])
    pq = [(0, (0, 0))]
    distances = {(0, 0): 0}
    parent = {(0, 0): None}

    while pq:
        current_distance, (x, y) = heapq.heappop(pq)

        if (x, y) == (width - 1, height - 1):
            path = []
            while (x, y) is not None:
                path.append((x, y))
                x, y = parent.get((x, y), None)
            return path[::-1]

        for direction in [N, S, E, W]:
            if grid[y][x] & direction:
                nx, ny = x + DX[direction], y + DY[direction]
                new_distance = current_distance + 1
                if (nx, ny) not in distances or new_distance < distances[(nx, ny)]:
                    distances[(nx, ny)] = new_distance
                    parent[(nx, ny)] = (x, y)
                    heapq.heappush(pq, (new_distance, (nx, ny)))

    return []

# Run bulk tests
def run_bulk_tests():
    folder_name = input("Enter a folder name to save results: ")
    os.makedirs(folder_name, exist_ok=True)

    results_filepath = os.path.join(folder_name, "results.txt")
    results = []

    for size in range(10, 100, 10):
        width, height = size, size
        filename = f"maze_{size}x{size}.csv"

        # Generate and save maze
        grid = generate_maze(width, height)
        save_maze_to_csv(grid, folder_name, filename)

        # Load maze and solve
        filepath = os.path.join(folder_name, filename)
        grid = load_maze_from_csv(filepath)

        # Solve with DFS
        start_time = time.time()
        dfs_path = dfs_solve(grid)
        dfs_duration = time.time() - start_time

        # Solve with BFS
        start_time = time.time()
        bfs_path = bfs_solve(grid)
        bfs_duration = time.time() - start_time

        # Solve with Dijkstra
        start_time = time.time()
        dijkstra_path = dijkstra_solve(grid)
        dijkstra_duration = time.time() - start_time

        results.append((size, len(dfs_path), dfs_duration, len(bfs_path), bfs_duration, len(dijkstra_path), dijkstra_duration))

    # Save and display results
    with open(results_filepath, mode='w') as results_file:
        results_file.write("Maze Solving Results:\n")
        results_file.write("Size | DFS Path Length | DFS Time | BFS Path Length | BFS Time | Dijkstra Path Length | Dijkstra Time\n")
        for size, dfs_len, dfs_time, bfs_len, bfs_time, dijkstra_len, dijkstra_time in results:
            result_line = f"{size}x{size} | {dfs_len} | {dfs_time:.4f} | {bfs_len} | {bfs_time:.4f} | {dijkstra_len} | {dijkstra_time:.4f}\n"
            results_file.write(result_line)
            print(result_line)

if __name__ == "__main__":
    run_bulk_tests()
