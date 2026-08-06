# Zde jsou dvě třídy, které dlouží k vytvoření datové struktury bludiště


class Cell:
    # slouží k uchování informací o dané buňce a k implementaci metod, které
    # tyto informace upravují
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.walls: dict[str, bool] = {"North": True, "East": True, "South": True, "West": True}
        self.is_visited: bool = False


    def visit(self) -> None:
        self.is_visited = True


    def remove_wall(self, direction: str) -> None:
        if direction in self.walls:
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
        self.cells = [[Cell(x, y) for x in range(width)] for y in range(height)]


    def is_in_range(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
