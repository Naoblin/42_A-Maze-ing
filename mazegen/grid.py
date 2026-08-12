# Zde jsou dvě třídy, které dlouží k vytvoření datové struktury bludiště

import sys

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
        self.is_reached_by: tuple[int, int]
        self.is_entry: bool = False
        self.is_exit: bool = False
        self.path_direction = ""


    def visit(self) -> None:
        self.is_visited = True


    def add_to_forty_two(self) -> None:
        self.is_forty_two = True


    def add_entry(self) -> None:
        if self.is_forty_two:
            raise ValueError("Entry cannot be located in the 42 logo")
        self.is_entry = True


    def add_exit(self) -> None:
        if self.is_forty_two:
            raise ValueError("Exit cannot be located in the 42 logo")
        self.is_exit = True

    def count_walls(self) -> int:
        count: int = 0
        for wall in self.walls:
            if self.walls[wall]:
                count += 1
        return count

    def get_walls(self) -> list[str]:
        walls: list[str] = []
        for wall in self.walls:
            if self.walls[wall]:
                walls.append(wall)
        return walls

    def is_dead_end(self) -> int:
        return self.count_walls() > 2

    def remove_wall(self, direction: str, opposite: bool = False, inverse: bool = False) -> None:
        if direction in self.walls:
            if opposite:
                opposite_walls: dict[str, str] = {
                    "N": "S",
                    "S": "N",
                    "E": "W",
                    "W": "E"
                }
                direction = opposite_walls[direction]
            self.walls[direction] = inverse
        else:
            raise ValueError(f"Unknown direction '{direction}'. "
                             f"Allowed directions are {self.walls.keys()}.")

    def get_hexadec(self) -> int:
        total_walls: int = 0
        if self.walls["N"]:
            total_walls += 1
        if self.walls["E"]:
            total_walls += 2
        if self.walls["S"]:
            total_walls += 4
        if self.walls["W"]:
            total_walls += 8
        return f"{total_walls:X}"


class Grid:
    # slouží k evidování celé mřížky z buněk
    # při vytvoření objektu se vytvoří maze se všemi stěnami
    # při generování bludiště dojde následně k odstraňování
    # těchto stěn (v generate.py)
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells = [[Cell(x, y) for y in range(width)] for x in range(height)]
        try:
            self.create_forty_two()
        except ValueError as e:
            print(str(e), file=sys.stderr)


    def is_in_range(self, x: int, y: int) -> bool:
        return 0 <= y < self.width and 0 <= x < self.height


    def get_cell(self, x: int, y: int) -> "Cell":
        return self.cells[x][y]

    def get_neighbour(self, x: int, y: int, site: str) -> tuple[int, int]:
        if site == "N":
            x -= 1
        elif site == "S":
            x += 1
        elif site == "E":
            y += 1
        elif site == "W":
            y -= 1
        return x, y


    def get_opened_neighbours(self, x: int, y: int) -> dict[tuple[int, int]: str]:
        neighbours: dict[tuple[int, int]: str] = {}
        if not self.get_cell(x, y).walls["N"]:
            neighbours[x - 1, y] = "N"
        if not self.get_cell(x, y).walls["E"]:
            neighbours[x, y + 1] = "E"
        if not self.get_cell(x, y).walls["S"]:
            neighbours[x + 1, y] = "S"
        if not self.get_cell(x, y).walls["W"]:
            neighbours[x, y - 1] = "W"
        return neighbours

    def connect_cells(self, start: tuple[int, int], path: str) -> None:
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


    def create_forty_two(self) -> None:
        four: str = "SSEESS"
        two: str = "EESSWWSSEE"

        if self.width < 8 or self.height < 6:
            raise ValueError("The maze is too small. It is generated without the '42' pattern")
        start: tuple[int, int] = (round((self.height - 6) / 2),
                                  round((self.width - 8) / 2))
        self.connect_cells(start, four)

        start = start[0], start[1] + 4
        self.connect_cells(start, two)

    def check_3x3_and_remove_wall(self, x, y, direction) -> bool:
        self.get_cell(x, y).remove_wall(direction)
        neighbour = self.get_neighbour(x, y, direction)
        self.get_cell(*neighbour).remove_wall(direction, opposite=True)
        for k in [x - 1, x, x + 1]:
            for l in [y - 1, y, y + 1]:
                if self.is_3x3(k, l):
                    self.get_cell(x, y).remove_wall(direction, inverse=True)
                    self.get_cell(*neighbour).remove_wall(direction, opposite=True, inverse=True)
                    return False
        return True

    def is_3x3(self, x: int, y: int) -> bool:
        for k in [x - 1, x, x + 1]:
            for l in [y - 1, y, y + 1]:
                if not self.is_in_range(k, l) or self.get_cell(k, l).is_forty_two:
                    return False
        if self.get_cell(x, y).count_walls() > 0:
            return False
        for side in "EW":
            if (self.get_cell(x + 1, y).walls[side] or
                self.get_cell(x - 1, y).walls[side]):
                return False
        for side in "NS":
            if (self.get_cell(x, y + 1).walls[side] or
                self.get_cell(x, y - 1).walls[side]):
                return False
        return True
