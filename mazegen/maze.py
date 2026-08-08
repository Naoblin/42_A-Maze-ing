# importy z jinych modulu
from .generate import generate_maze
from .solve import solve_maze
from .grid import Grid
from .display import display_maze
from typing import Any


class MazeGenerator:
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], perfect: bool, seed: Any = None) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self.maze: Grid
        self.solution: str  # tohle jsem tu předpřipravil, ale nechám na tobě
        # jestli to tak necháš, nebo co s tím uděláš. Na první dobrou tipuji,
        # že budeš z solve_maze() vracet string ve formátu "ESEENNWNEES" apod.
        # jak to chce zadání. Případně, jestli si budeš nějak trackovat tu
        # cestu/řešení, třeba pomocí nějaké podobné třídy jako grid, tak se
        # může z solve_maze() vracet ta třída a až pak dodatečně převést na
        # ten formát "ESEENNWNEES"


    # navrhuji, že by se v metodách generate a solve pouze volali funkce
    # importované z jiných modulů, kde si každý budeme psát vlastní kódy
    # nevím ale, jestli je v programátorské praxi takovýto přístup ok
    def generate(self):
        self.maze = generate_maze(self.height, self.width, self.seed)
        # self.maze = Grid(self.width, self.height)

    def solve(self):
        self.solution = solve_maze(self.maze, self.entry, self.exit)

    def display(self):
        # display_maze(self.maze)

        for x in range(self.height):
            if x == 0:
                print("██" * (self.width * 2 + 1))
            for y in range(self.width):
                if y == 0:
                    print("██", end="")
                if self.maze.get_cell(x, y).is_forty_two:
                    print("██", end="")
                else:
                    print("  ", end="")

                if self.maze.cells[x][y].walls["E"]:
                    print("██", end="")
                else:
                    print("  ", end="")
            print()

            for y in range(self.width):
                if y == 0:
                    print("██", end="")

                if self.maze.cells[x][y].walls["S"]:
                    print("██", end="")
                else:
                    print("  ", end="")

                if (self.maze.cells[x][y].walls["S"] or
                    self.maze.cells[x][y].walls["E"] or
                    (self.maze.is_in_range(x, y + 1) and
                     self.maze.cells[x][y + 1].walls["S"]) or
                    (self.maze.is_in_range(x + 1, y) and
                     self.maze.cells[x + 1][y].walls["E"])):
                    print("██", end="")
                else:
                    print("  ", end="")
            print()
