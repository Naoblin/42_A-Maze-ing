# importy z jinych modulu
from .generate import generate_maze
from .solve import solve_maze
from .grid import Grid


class MazeGenerator:
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], perfect: bool):
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
