from mazegen import MazeGenerator
import os

def display_interactive(maze: MazeGenerator):
    maze.generate()
    maze.solve()
    maze.make_output_file()
    show_solution: bool = True
    color_walls: int = 0
    color_42: int = 1
    while True:
        os.system("clear")
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

        if decision == "1":
            maze.generate()
            maze.solve()
            maze.make_output_file()
        elif decision == "2":
            show_solution = not show_solution
        elif decision == "3":
            color_walls = (color_walls + 1) % 6
            if color_walls == color_42:
                color_walls = (color_walls + 1) % 6
        elif decision == "4":
            color_42 = (color_42 + 1) % 6
            if color_42 == color_walls:
                color_42 = (color_42 + 1) % 6
        elif decision == "5":
            break
