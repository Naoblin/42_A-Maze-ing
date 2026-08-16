# `mazegen` — Usage Guide

`MazeGenerator` is the main class for generating, solving, and exporting mazes.

## Basic Example

```python
from mazegen import MazeGenerator

maze = MazeGenerator(width=20, height=15, entry=(0, 0), exit=(19, 14),output_file="maze.txt")
maze.generate()
maze.solve()
maze.display()
maze.make_output_file()
```

## Custom Parameters
The parameters correspond to the grid as follows:

* **Width:** The number of columns.
* **Height:** The number of rows.
* **Entry and Exit:** Tuples in the format `(x, y)`, where `x` represents the column and `y` represents the row.

Besides the mandatory `width`, `height`, `entry`, `exit` and `output_file`, two optional parameters are available:

- `perfect` (`bool`, default `False`) — if `True`, generates a perfect maze (exactly one path between entry and exit).
- `seed` (default `None`) — sets the random seed, so the same parameters always produce the same maze.

```python
maze = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    output_file="maze.txt",
    perfect=True,
    seed=42
)
```

## Accessing the Generated Structure

After calling `generate()`, the maze's internal grid is available through the `maze.maze` attribute (a `Grid` object):

```python
maze.generate()
grid = maze.maze
```

## Accessing the Solution

After calling `solve()`, the shortest path from entry to exit is available through the `maze.solution` attribute, as a string of directions (`N`, `E`, `S`, `W`):

```python
maze.solve()
print(maze.solution)  # e.g. 'EEESSSEESSSSESENESEE'
```

## Methods

- `generate()` — generates the maze structure and sets the entry and exit points.
- `solve()` — finds the shortest path between the entry and exit.
- `display(show_solution=True, color_walls=0, color_42=1)` — prints a visual representation of the maze to the terminal.
- `make_output_file()` — exports the hex-based maze layout, coordinates, and solution to a file.

Every method includes a detailed docstring with parameters and return values. You can view them directly in Python:

```python
help(MazeGenerator)
```