from mazegen import MazeGenerator
import os


def display_interactive(maze: MazeGenerator) -> None:
    """
    Run the interactive terminal interface for the maze.

    Generates, solves, and saves the maze, then enters a loop allowing
    the user to regenerate the maze, toggle the solution visibility,
    change the colors of walls and the '42' pattern, or exit.

    Parameters
    ----------
    maze : MazeGenerator
        The maze generator instance to be displayed and manipulated.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    
    maze.generate()
    maze.solve()
    maze.make_output_file()
    show_solution: bool = True
    color_walls: int = 0
    color_42: int = 1
    while True:
        maze.display(show_solution, color_walls, color_42)
        menu = ("\n" +
                "=== A-Maze-Ing ===\n" +
                "Regenerate new maze     [1]\n" +
                "Show/Hide solution      [2]\n" +
                "Change wall colors      [3]\n" +
                "Change 42 colors        [4]\n" +
                "Exit                    [5]\n" +
                "What's your choice? ")
        decision = input(menu)

        while decision not in ("1", "2", "3", "4", "5"):
            decision = input("Not a valid option, try again: ")

        os.system('cls' if os.name == 'nt' else 'clear')

        if decision == "1":
            maze.generate()
            maze.solve()
            maze.make_output_file()
        elif decision == "2":
            show_solution = not show_solution
        elif decision == "3":
            color_walls = (color_walls + 1) % 7
            if color_walls == color_42:
                color_walls = (color_walls + 1) % 7
        elif decision == "4":
            color_42 = (color_42 + 1) % 7
            if color_42 == color_walls:
                color_42 = (color_42 + 1) % 7
        elif decision == "5":
            break
