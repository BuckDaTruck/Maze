from Gen import generate_maze, save_maze_to_csv
from Solve import dfs_solve, bfs_solve, dijkstra_solve
import os
import time

def generate_and_solve(filename, width, height):
    """Generates a maze, saves it, and solves it with all algorithms."""
    # Create the base directory for storing results
    base_dir = "auto_run_results"
    os.makedirs(base_dir, exist_ok=True)

    # Generate maze
    grid = generate_maze(width, height)

    # Save maze to CSV
    maze_path = os.path.join(base_dir, f"{filename}.csv")
    save_maze_to_csv(grid, maze_path)

    # Run algorithms and save results
    algorithms = [
        ("DFS", dfs_solve),
        ("BFS", bfs_solve),
        ("Dijkstra", dijkstra_solve)
    ]

    results = []
    for algo_name, algo_func in algorithms:
        start_time = time.time()
        path, moves = algo_func(grid, width, height)
        duration = time.time() - start_time
        results.append((algo_name, len(path), moves, duration))

    # Save results to text file
    result_path = os.path.join(base_dir, f"{filename}_results.txt")
    with open(result_path, "w") as f:
        f.write(f"Results for {filename} ({width}x{height}):\n")
        f.write("Algorithm | Path Length | Moves | Time (s)\n")
        f.write("-" * 40 + "\n")
        for algo_name, path_len, moves, duration in results:
            f.write(f"{algo_name:<10} | {path_len:<11} | {moves:<5} | {duration:.3f}\n")

    print(f"Maze and results saved for {filename} ({width}x{height}).")

if __name__ == "__main__":
    # Example usage
    generate_and_solve("example_maze_small", 10, 10)
    generate_and_solve("example_maze_medium", 25, 25)
    generate_and_solve("example_maze_large", 50, 50)
