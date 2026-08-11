# importy z jinych modulu
from .generate import generate_maze
from .solve import solve_maze
from .grid import Grid
from .display import display_maze
from typing import Any
import sys


class MazeGenerator:
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], perfect: bool = False, seed: Any = None) -> None:
        self.width = width
        self.height = height
        self.entry = entry[1], entry[0]
        self.exit = exit[1], exit[0]
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
        self.maze = generate_maze(self.height, self.width, self.perfect, self.seed)
        try:
            self.maze.get_cell(*self.entry).add_entry()
            self.maze.get_cell(*self.exit).add_exit()
        except ValueError as e:
            sys.exit(str(e))

    def solve(self):
        self.solution = solve_maze(self.maze, self.entry, self.exit)

    def display(self):
        display_maze(self.maze, self.height, self.width)

    def make_output_file(self):
        with open("output_maze.txt", "w") as file:
            for x in range(self.height):
                line: str = ""
                for y in range(self.width):
                    line += str(self.maze.get_cell(x, y).get_hexadec())
                file.write(line + "\n")

            file.write("\n")
            file.write(f"{self.entry[1]}, {self.entry[0]}\n")
            file.write(f"{self.exit[1]}, {self.exit[0]}\n")
            file.write(f"{self.solution}\n")
