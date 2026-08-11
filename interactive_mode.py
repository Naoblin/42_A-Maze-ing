from mazegen import MazeGenerator
import os

def display_interactive(maze: MazeGenerator):
    maze.generate()
    maze.solve()
    maze.make_output_file()
    while True:
        os.system("clear")
        maze.display()
        menu = ("\n" +
                "=== A-Maze-Ing ===\n" +
                "Regenerate new maze     [1]\n" +
                "Show/Hide solution      [2]\n" +
                "Change wall colors      [3]\n" +
                "Change 42 colors        [4]\n" +
                "Exit                    [5]\n")
        decision = input(menu)

        if decision == "1":
            maze.generate()
            maze.solve()
            maze.make_output_file()
        if decision == "2":
            pass
        if decision == "3":
            pass
        if decision == "4":
            pass
        if decision == "5":
            break
