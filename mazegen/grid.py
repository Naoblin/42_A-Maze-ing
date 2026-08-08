# Zde jsou dvě třídy, které dlouží k vytvoření datové struktury bludiště

class Cell:
    # slouží k uchování informací o dané buňce a k implementaci metod, které
    # tyto informace upravují
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.walls: dict[str, bool] = {"N": True, "E": True, "S": True, "W": True}
        self.is_visited: bool = False
        self.is_forty_two: bool = False
        self.is_solution: bool = False
        self.is_reached_by: tuple[int, int] = None


    def visit(self) -> None:
        self.is_visited = True


    def add_to_forty_two(self) -> None:
        self.is_forty_two = True


    def remove_wall(self, direction: str, opposite: bool = False) -> None:
        if direction in self.walls:
            if opposite:
                opposite_walls: dict[str, str] = {
                    "N": "S",
                    "S": "N",
                    "E": "W",
                    "W": "E"
                }
                direction = opposite_walls[direction]
            self.walls[direction] = False
        else:
            raise ValueError(f"Unknown direction '{direction}'. "
                             f"Allowed directions are {self.walls.keys()}.")


class Grid:
    # slouží k evidování celé mřížky z buněk
    # při vytvoření objektu se vytvoří maze se všemi stěnami
    # při generování bludiště dojde následně k odstraňování
    # těchto stěn (v generate.py)
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells = [[Cell(x, y) for y in range(width)] for x in range(height)]
        self.create_forty_two()


    def is_in_range(self, x: int, y: int) -> bool:
        return 0 <= y < self.width and 0 <= x < self.height


    def get_cell(self, x: int, y: int) -> "Cell":
        return self.cells[x][y]

    def get_opened_neighbours(self, x: int, y: int) -> list[tuple[int, int]]:
        neighbours: list[tuple[int, int]] = []
        if self.get_cell(x, y).walls["N"] is False:
            neighbours.append((x - 1, y))
        if self.get_cell(x, y).walls["E"] is False:
            neighbours.append((x, y + 1))
        if self.get_cell(x, y).walls["S"] is False:
            neighbours.append((x + 1, y))
        if self.get_cell(x, y).walls["W"] is False:
            neighbours.append((x, y - 1))
        return neighbours

    def connect_cells(self, start: tuple[int, int], path: str):
        x, y = start
        self.get_cell(x, y).visit()
        self.get_cell(x, y).add_to_forty_two()
        for direction in path:
            if direction == "N":
                x -= 1
            elif direction == "S":
                x += 1
            elif direction == "E":
                y += 1
            elif direction == "W":
                y -= 1
            else:
                raise ValueError("CHYBA V CONNECT_CELLS")  # toto jeste doresit
            self.get_cell(x, y).visit()
            self.get_cell(x, y).add_to_forty_two()


    def create_forty_two(self):
        four: str = "SSEESS"
        two: str = "EESSWWSSEE"
        
        start: tuple[int, int] = (round((self.height - 6) / 2),
                                  round((self.width - 8) / 2))
        self.connect_cells(start, four)

        start = start[0], start[1] + 4
        self.connect_cells(start, two)

