# importy z jinych modulu
from .generate import generate_maze
from .solve import solve_maze
from .grid import Grid
from .display import display_maze


class MazeGenerator:
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], perfect: bool) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
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
        self.maze = generate_maze(self.width, self.height)


    def solve(self):
        self.solution = solve_maze(self.maze)


    def display(self):
        display_maze(self.maze)

        for x in range(self.height):
            if x == 0:
                print("██" * (self.width * 2 + 1))
            for y in range(self.width):
                if y == 0:
                    print("██", end="")
                print("  ", end="")

                if self.maze.cells[x][y].walls["East"]:
                    print("██", end="")
                else:
                    print("  ", end="")

                if y == self.width - 1:
                    # print("██")
                    print()

            for y in range(self.width):
                if y == 0:
                    print("██", end="")

                if self.maze.cells[x][y].walls["South"]:
                    print("██", end="")
                else:
                    print("  ", end="")

                if (self.maze.cells[x][y].walls["South"] or
                    self.maze.cells[x][y].walls["East"] or
                    (self.maze.is_in_range(x, y + 1) and
                     self.maze.cells[x, y + 1].walls["South"]) or
                    (self.maze.is_in_range(x + 1, y) and
                     self.maze.cells[x, y + 1].walls["East"])):
                    print("██", end="")
                else:
                    print("  ", end="")

                if y == self.width - 1:
                    # print("██")
                    print()
        
        # print("██" * (self.width * 2 + 1))


