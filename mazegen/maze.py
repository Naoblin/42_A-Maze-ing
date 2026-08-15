from .generate import generate_maze
from .solve import solve_maze
from .grid import Grid
from .display import display_maze
from typing import Any
import sys


class MazeGenerator:
    """
    A unified interface for generating, solving, displaying, and exporting mazes.

    Parameters
    ----------
    width : int
        The width (number of columns) of the maze.
    height : int
        The height (number of rows) of the maze.
    entry : tuple[int, int]
        The (x, y) coordinates for the maze entry.
    exit : tuple[int, int]
        The (x, y) coordinates for the maze exit.
    perfect : bool, optional
        If True, generates a perfect maze. Default is False.
    seed : Any, optional
        The seed for the random number generator. Default is None.

    Attributes
    ----------
    maze : Grid
        The internal grid structure. Populated by `generate()`.
    solution : str
        The string path from entry to exit. Populated by `solve()`.

    Methods
    -------
    generate()
        Generates the maze structure and sets the entry and exit points.
    solve()
        Finds the shortest path between the entry and exit.
    display()
        Prints a visual representation of the maze to the standard output.
    make_output_file()
        Exports the hexadecimal maze layout, coordinates, and solution 
        into 'output_maze.txt'.
    """

    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], perfect: bool = False, seed: Any = None
                 ) -> None:
        """
        Initialize the MazeGenerator instance.

        Coordinates for entry and exit are automatically converted from
        (x, y) input format to (row, column) internal layout.
        """
        self.width = width
        self.height = height
        self.entry = entry[1], entry[0]
        self.exit = exit[1], exit[0]
        self.perfect = perfect
        self.seed = seed
        self.maze: Grid
        self.solution: str | None = None

    def generate(self) -> None:
        """
        Generate the maze grid and apply the entry and exit points.

        This method populates the `maze` attribute by delegating the core
        logic to the `generate_maze` function. It then sets the specified
        entry and exit cells. 

        Raises
        ------
        SystemExit
            If the entry or exit cannot be placed (e.g., they overlap 
            with the forbidden '42' pattern), the program exits.
        """
        self.maze = generate_maze(self.height, self.width, self.perfect,
                                  self.seed)
        try:
            self.maze.get_cell(*self.entry).add_entry()
            self.maze.get_cell(*self.exit).add_exit()
        except ValueError as e:
            sys.exit(str(e))

    def solve(self) -> None:
        """
        Find the shortest path from the entry to the exit.

        This method populates the `solution` attribute with a string
        representing the sequence of directions required to navigate 
        the maze.
        """
        try:
            self.solution = solve_maze(self.maze, self.entry, self.exit)
        except AttributeError as e:
            sys.exit(f"AttributeError: {e}")

    def display(self, show_solution: bool = True, color_walls: int = 0,
                color_42: int = 1) -> None:
        """
        Print a visual representation of the maze to the standard output.

        Parameters
        ----------
        show_solution : bool, optional
            Whether to display the solved path in the output. Default is True.
        color_walls : int, optional
            ANSI color code (0-6) to use for the walls. Default is 0 (white).
            0 = white, 1 = cyan, 2 = magenta, 3 = blue, 4 = yellow,
            5 = green, 6 = red.
        color_42 : int, optional
            ANSI color code (0-6) to use for the mandatory '42' pattern.
            Default is 1 (cyan).
            0 = white, 1 = cyan, 2 = magenta, 3 = blue, 4 = yellow,
            5 = green, 6 = red.
        """
        if show_solution and not self.solution:
            print("No solution found yet. Displaying the maze without a path.",
                  "Run solve() first to include the solution.")
        try:
            display_maze(self.maze, self.height, self.width, show_solution,
                     color_walls, color_42)
        except ValueError as e:
            print(f"Display maze error: {e}")
        except AttributeError as e:
            sys.exit(f"AttributeError: {e}")

    def make_output_file(self) -> None:
        """
        Export the maze layout and metadata to a text file.

        The file is created as 'output_maze.txt' in the current working
        directory. It contains the hexadecimal representation of the walls 
        for each cell, followed by the entry coordinates, exit coordinates, 
        and the solution path string.

        Raises
        ------
        SystemExit
            If an OSError occurs during the file writing process.
        """
        try:
            with open("output_maze.txt", "w") as file:
                for x in range(self.height):
                    line: str = ""
                    for y in range(self.width):
                        line += str(self.maze.get_cell(x, y).get_hexadec())
                    file.write(line + "\n")

                file.write("\n")
                file.write(f"{self.entry[1]}, {self.entry[0]}\n")
                file.write(f"{self.exit[1]}, {self.exit[0]}\n")
                file.write(f"{self.solution}\n")
        except OSError as e:
            sys.exit(f"An error occured while writing to the output file: {str(e)}")
        except AttributeError as e:
            sys.exit(f"AttributeError: {e}")
        if not self.solution:
            print("No solution found yet. The 'output_maze.txt' shows 'None'",
                  "instead. Run solve() first to include the solution.")
