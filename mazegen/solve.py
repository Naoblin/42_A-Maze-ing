# v tomto souboru by byl kód pro hledání řešení
# pripadne muzeme jeste misto solve.py udělat složku solve
# ve které budou všechny soubory s kódem k hledání řešení
from .grid import Grid


def bfs(maze: Grid, entry: tuple, exit: tuple):
    queue: list[tuple[int, int]] = []
    solution: str = ""

    current_cell: tuple[int, int] = entry
    maze.get_cell(*current_cell).visit()
    queue.append(current_cell)

    while queue:
        current_cell = queue.pop(0)
        if current_cell == exit:
            solution += maze.get_cell(*exit).path_direction
            break

        for neighbour, direction in maze.get_opened_neighbours(*current_cell).items():
            if not maze.get_cell(*neighbour).is_visited:
                queue.append(neighbour)
                maze.get_cell(*neighbour).visit()
                maze.get_cell(*neighbour).is_reached_by = current_cell
                maze.get_cell(*neighbour).path_direction = direction

    while current_cell != entry:
        maze.get_cell(*current_cell).is_solution = True
        current_cell = maze.get_cell(*current_cell).is_reached_by
        solution += maze.get_cell(*current_cell).path_direction
    solution = solution[::-1]
    print(solution)

def solve_maze(maze: Grid, entry: tuple[int, int], exit: tuple[int, int]):
    # tělo funkce jsem vyplnil jen pro představu, nechávám na tobě :)
    # solution: str = "ESEENNWNEES"
    # return solution

    # myslím, že nevadí, když znovu použiju is_visited
    # jen si to nejdřív musím resetovat
    # pro jistotu resetuju i is_solution
    for x in range(maze.height):
        for y in range(maze.width):
            maze.get_cell(x, y).is_visited = False
            maze.get_cell(x, y).is_solution = False

    bfs(maze, entry, exit)
    #for x in range(maze.height):
    #    for y in range(maze.width):
    #        print((x,y), ":", maze.get_cell(x, y).path_direction)
