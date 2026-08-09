# v tomto souboru by byl kód pro generování bludiště
# pripadne muzeme jeste misto generate.py udělat složku generate ve které budou všechny soubory s kódem
# ke generování bludiště
from .grid import Grid
from random import seed, randrange, choice

# zde bude kód pro vytvoření bludiště z grid (tj. bludiště se všemi stěnami)
def generate_maze(height: int, width: int, perfect: bool, seed_value: int = None):
    maze = Grid(width, height)
    if seed_value:
        seed(seed_value)
    visited_cells: list[tuple[int, int]] = []

    # nahodne zvolit zacatek generovani bludiste
    current_cell: tuple[int, int] = (randrange(height), randrange(width))
    # obcas se stalo, ze chybela stena u 42. To nastalo, když se začýtek generování
    # bludiště vybral právě do 42 a při generování bludiště došlo k probourání stěny
    # teď už by to mělo být ok, protože vybíráme start generování tak dlouho, dokud není
    # mimo 42
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


def make_playable(maze: Grid):
    for x in maze.height:
        for y in maze.width:
            if maze.get_cell(x, y).is_dead_end():
                # vybrat nahodnou postavenou stenu ze seznamu sten
                walls: list[] = maze.get_cell(x, y).get_walls()
                wall = walls.pop()
                # zkontrolovat, že to není stěna s okrajem, nebo s 42, jinak vybrat jinou
                # zkontrolovat, že po odstranění stěny nevznikne prostor 3x3 a větší
                # odstranit danou stěnu (pokud nějaká zbyla)


