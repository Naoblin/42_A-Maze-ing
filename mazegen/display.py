from .grid import Grid


def display_maze(maze: Grid, height: int, width: int,
                 show_solution: bool = True, color_walls: int = 0,
                 color_42: int = 0) -> None:
    colors = [37, 36, 35, 34, 32, 31]
    wall = f"\x1b[{colors[color_walls]}m██\x1b[0m"
    path = "  "
    solution = "\x1b[31m◀▶\x1b[0m"
    forty_two = f"\x1b[{colors[color_42]}m██\x1b[0m"
    entry = "🟢"
    exit = "🏁"

    for x in range(height):
        if x == 0:
            print(wall * (width * 2 + 1))
        for y in range(width):
            if y == 0:
                print(wall, end="")
            if maze.get_cell(x, y).is_forty_two:
                print(forty_two, end="")
            elif maze.get_cell(x, y).is_entry:
                print(entry, end="")
            elif maze.get_cell(x, y).is_exit:
                print(exit, end="")
            elif show_solution and maze.get_cell(x, y).is_solution:
                print(solution, end="")
            else:
                print(path, end="")

            if maze.get_cell(x, y).walls["E"]:
                print(wall, end="")
            else:
                print(path, end="")
        print()

        for y in range(width):
            if y == 0:
                print(wall, end="")

            if maze.get_cell(x, y).walls["S"]:
                print(wall, end="")
            else:
                print(path, end="")

            if (maze.get_cell(x, y).walls["S"] or
                maze.get_cell(x, y).walls["E"] or
                (maze.is_in_range(x, y + 1) and
                    maze.get_cell(x, y + 1).walls["S"]) or
                (maze.is_in_range(x + 1, y) and
                    maze.get_cell(x + 1, y).walls["E"])):
                print(wall, end="")
            else:
                print(path, end="")
        print()
