from .grid import Grid
from random import seed, randrange, choice


def generate_maze(height: int, width: int, perfect: bool,
                  seed_value: int | None = None) -> "Grid":
    """
    Generate a random maze structure on a new grid using
    the recursive backtracker algorithm.

    Parameters
    ----------
    height : int
        The height (number of rows) of the maze.
    width : int
        The width (number of columns) of the maze.
    perfect : bool
        If True, generates a perfect maze without loops. If False, 
        extra walls at dead-ends are removed to create a playable board.
    seed_value : int | None, optional
        The seed for the random number generator. Default is None.

    Returns
    -------
    Grid
        A new Grid instance representing the fully generated maze.
    """
    maze = Grid(width, height)
    if seed_value:
        seed(seed_value)
    visited_cells: list[tuple[int, int]] = []

    current_cell: tuple[int, int] = (randrange(height), randrange(width))

    while maze.get_cell(*current_cell).is_forty_two:
        current_cell = (randrange(height), randrange(width))
    maze.get_cell(*current_cell).visit()
    visited_cells.append(current_cell)

    while visited_cells:
        current_cell = visited_cells[-1]
        x, y = current_cell
        neighbour_cells: list[tuple[int, int, str]] = []
        direction: str
        for k in [y - 1, y + 1]:
            if maze.is_in_range(x, k) and not maze.get_cell(x, k).is_visited:
                if k < y:
                    direction = "W"
                else:
                    direction = "E"
                neighbour_cells.append((x, k, direction))

        for k in [x - 1, x + 1]:
            if maze.is_in_range(k, y) and not maze.get_cell(k, y).is_visited:
                if k < x:
                    direction = "N"
                else:
                    direction = "S"
                neighbour_cells.append((k, y, direction))

        if not neighbour_cells:
            visited_cells.pop()
            continue
        else:
            x, y, direction = choice(neighbour_cells)
            maze.get_cell(*current_cell).remove_wall(direction)
            maze.get_cell(x, y).remove_wall(direction, opposite=True)
            visited_cells.append((x, y))
            maze.get_cell(x, y).visit()

    if not perfect:
        make_playable(maze)

    return maze


def make_playable(maze: Grid) -> None:
    """
    Remove dead ends to make the maze suitable for Pac-Man.

    Iterates through the maze and randomly removes walls from dead ends 
    to create loops, ensuring no 3x3 open spaces are formed and the 
    '42' pattern remains intact.

    Parameters
    ----------
    maze : Grid
        The grid object representing the maze to be modified.
    """
    for x in range(maze.height):
        for y in range(maze.width):
            if (
                maze.get_cell(x, y).is_dead_end() and
                not maze.get_cell(x, y).is_forty_two
            ):
                walls: list[str] = maze.get_cell(x, y).get_walls()
                while walls:
                    direction: str = walls.pop(randrange(len(walls)))
                    neighbour = maze.get_neighbour(x, y, direction)
                    if (
                        maze.is_in_range(*neighbour) and
                        not maze.get_cell(*neighbour).is_forty_two
                    ):
                        maze.check_3x3_and_remove_wall(x, y, direction)
                        break
