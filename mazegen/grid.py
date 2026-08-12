import sys


class Cell:
    """
    Represent a single cell in the maze grid.

    Parameters
    ----------
    x : int
        The row coordinate of the cell.
    y : int
        The column coordinate of the cell.

    Attributes
    ----------
    walls : dict[str, bool]
        A dictionary indicating whether the walls (N, E, S, W) are standing.
    is_visited : bool
        Flag indicating if the cell has been visited during generation/solving.
    is_forty_two : bool
        Flag indicating if the cell is part of the mandatory '42' pattern.
    is_solution : bool
        Flag indicating if the cell is part of the final solution path.
    is_reached_by : tuple[int, int]
        The coordinates of the previous cell in the shortest path.
    is_entry : bool
        Flag indicating if the cell is the maze entry.
    is_exit : bool
        Flag indicating if the cell is the maze exit.
    path_direction : str
        The direction taken to reach this cell during solving.

    Methods
    -------
    visit()
        Mark the cell as visited.
    add_to_forty_two()
        Mark the cell as part of the '42' pattern.
    add_entry()
        Mark the cell as the entry point of the maze.
    add_exit()
        Mark the cell as the exit point of the maze.
    count_walls()
        Count the number of standing walls around the cell.
    get_walls()
        Get a list of directions where the walls are currently standing.
    is_dead_end()
        Determine if the cell is a dead end.
    remove_wall(direction, opposite=False, inverse=False)
        Remove or restore a wall in the specified direction.
    get_hexadec()
        Calculate the hexadecimal representation of the cell's walls.
    """

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.walls: dict[str, bool] = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }
        self.is_visited: bool = False
        self.is_forty_two: bool = False
        self.is_solution: bool = False
        # nevim, jestli je nekde v kodu nutne, aby zde byl None, doresime spolu
        # bud dat pryc None, nebo upravit type hint na "tuple[int, int] | None"
        # ale pak se to bude muset upravit i dal v kodu
        self.is_reached_by: tuple[int, int] = None
        self.is_entry: bool = False
        self.is_exit: bool = False
        self.path_direction = ""

    def visit(self) -> None:
        """Mark the cell as visited."""
        self.is_visited = True

    def add_to_forty_two(self) -> None:
        """Mark the cell as part of the '42' pattern."""
        self.is_forty_two = True

    def add_entry(self) -> None:
        """
        Mark the cell as the entry point of the maze.

        Raises
        ------
        ValueError
            If the cell is already designated as part of the '42' pattern.
        """
        if self.is_forty_two:
            raise ValueError("Entry cannot be located in the 42 logo")
        self.is_entry = True

    def add_exit(self) -> None:
        """
        Mark the cell as the exit point of the maze.

        Raises
        ------
        ValueError
            If the cell is already designated as part of the '42' pattern.
        """
        if self.is_forty_two:
            raise ValueError("Exit cannot be located in the 42 logo")
        self.is_exit = True

    def count_walls(self) -> int:
        """
        Count the number of standing walls around the cell.

        Returns
        -------
        int
            The number of closed walls (0-4).
        """
        count: int = 0
        for wall in self.walls:
            if self.walls[wall]:
                count += 1
        return count

    def get_walls(self) -> list[str]:
        """
        Get a list of directions where the walls are currently standing.

        Returns
        -------
        list[str]
            A list of strings representing standing walls (e.g., ['N', 'E']).
        """
        walls: list[str] = []
        for wall in self.walls:
            if self.walls[wall]:
                walls.append(wall)
        return walls

    def is_dead_end(self) -> int:
        """
        Determine if the cell is a dead end (3 or more standing walls).

        Returns
        -------
        int
            Evaluates to True (1) if it's a dead end, False (0) otherwise.
        """
        return self.count_walls() > 2

    def remove_wall(self, direction: str, opposite: bool = False,
                    inverse: bool = False) -> None:
        """
        Remove or restore a wall in the specified direction.

        Parameters
        ----------
        direction : str
            The direction of the wall to modify ('N', 'E', 'S', 'W').
        opposite : bool, optional
            If True, modifies the wall on the opposite side of the given direction.
            Default is False.
        inverse : bool, optional
            If True, restores the wall instead of removing it. Default is False.

        Raises
        ------
        ValueError
            If the provided direction is not one of 'N', 'E', 'S', 'W'.
        """
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

    def get_hexadec(self) -> str:
        """
        Calculate the hexadecimal representation of the cell's walls.

        Returns
        -------
        str
            A single hexadecimal character (0-F) encoding the standing walls.
        """
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
    """
    Represent the entire maze grid composed of Cell objects.
    Initialize the Grid instance with fully walled cells and the '42' pattern.

    Parameters
    ----------
    width : int
        The number of columns in the grid.
    height : int
        The number of rows in the grid.

    Attributes
    ----------
    cells : list[list[Cell]]
        A 2D list containing the Cell instances of the maze.

    Methods
    -------
    is_in_range(x, y)
        Check if the given coordinates are within the grid boundaries.
    get_cell(x, y)
        Retrieve the Cell object at the specified coordinates.
    get_neighbour(x, y, site)
        Get the coordinates of the neighboring cell in a specific direction.
    get_opened_neighbours(x, y)
        Find all accessible neighboring cells (where the shared wall is open).
    connect_cells(start, path)
        Carve a specific path of cells and mark them as the '42' pattern.
    create_forty_two()
        Generate the '42' pattern in the center of the grid.
    check_3x3_and_remove_wall(x, y, direction)
        Attempt to remove a wall, reverting if it creates an open 3x3 space.
    is_3x3(x, y)
        Check if the specified cell is the center of a fully open 3x3 area.
    """

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells = [[Cell(x, y) for y in range(width)
                       ] for x in range(height)]
        try:
            self.create_forty_two()
        except ValueError as e:
            print(str(e), file=sys.stderr)

    def is_in_range(self, x: int, y: int) -> bool:
        """
        Check if the given coordinates are within the grid boundaries.

        Parameters
        ----------
        x : int
            The row coordinate to check.
        y : int
            The column coordinate to check.

        Returns
        -------
        bool
            True if the coordinates are within the grid limits, False otherwise.
        """
        return 0 <= y < self.width and 0 <= x < self.height

    def get_cell(self, x: int, y: int) -> "Cell":
        """
        Retrieve the Cell object at the specified coordinates.

        Parameters
        ----------
        x : int
            The row coordinate of the cell.
        y : int
            The column coordinate of the cell.

        Returns
        -------
        Cell
            The Cell instance at (x, y).
        """
        return self.cells[x][y]

    def get_neighbour(self, x: int, y: int, site: str) -> tuple[int, int]:
        """
        Get the coordinates of the neighboring cell in a specific direction.

        Parameters
        ----------
        x : int
            The current row coordinate.
        y : int
            The current column coordinate.
        site : str
            The direction to look for the neighbor ('N', 'E', 'S', 'W').

        Returns
        -------
        tuple[int, int]
            The (row, column) coordinates of the neighboring cell.
        """
        if site == "N":
            x -= 1
        elif site == "S":
            x += 1
        elif site == "E":
            y += 1
        elif site == "W":
            y -= 1
        return x, y

    def get_opened_neighbours(self, x: int, y: int
                              ) -> dict[tuple[int, int], str]:
        """
        Find all accessible neighboring cells (where the shared wall is open).

        Parameters
        ----------
        x : int
            The row coordinate of the current cell.
        y : int
            The column coordinate of the current cell.

        Returns
        -------
        dict[tuple[int, int], str]
            A dictionary mapping the (row, col) coordinates of accessible 
            neighbors to the direction taken to reach them.
        """
        neighbours: dict[tuple[int, int], str] = {}
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
        """
        Carve a specific path of cells and mark them as the '42' pattern.

        Parameters
        ----------
        start : tuple[int, int]
            The (row, col) starting coordinates.
        path : str
            A string of directions (e.g., 'SSEESS') to carve out.

        Raises
        ------
        ValueError
            If an invalid direction character is encountered in the path.
        """
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
                raise ValueError("Grid.connect_cells() - invalid argument 'path' "
                                 f"with direction '{direction}'")
            self.get_cell(x, y).visit()
            self.get_cell(x, y).add_to_forty_two()

    def create_forty_two(self) -> None:
        """
        Generate the '42' pattern in the center of the grid.

        Raises
        ------
        ValueError
            If the grid dimensions are smaller than 9x7.
        """
        four: str = "SSEESS"
        two: str = "EESSWWSSEE"

        if self.width < 9 or self.height < 7:
            raise ValueError("The maze is too small. "
                             "It is generated without the '42' pattern")
        start: tuple[int, int] = (((self.height - 4) // 2),
                                  ((self.width - 6) // 2))
        self.connect_cells(start, four)

        start = start[0], start[1] + 4
        self.connect_cells(start, two)

    def check_3x3_and_remove_wall(self, x: int, y: int, direction: str
                                  ) -> bool:
        """
        Attempt to remove a wall, reverting if it creates an open 3x3 space.

        Parameters
        ----------
        x : int
            The row coordinate of the cell.
        y : int
            The column coordinate of the cell.
        direction : str
            The direction of the wall to remove.

        Returns
        -------
        bool
            True if the wall was successfully removed without creating a 3x3
            open space, False if the removal was reverted.
        """
        self.get_cell(x, y).remove_wall(direction)
        neighbour = self.get_neighbour(x, y, direction)
        self.get_cell(*neighbour).remove_wall(direction, opposite=True)
        for m in [x - 1, x, x + 1]:
            for n in [y - 1, y, y + 1]:
                if self.is_3x3(m, n):
                    self.get_cell(x, y).remove_wall(direction, inverse=True)
                    self.get_cell(*neighbour).remove_wall(
                        direction, opposite=True, inverse=True
                    )
                    return False
        return True

    def is_3x3(self, x: int, y: int) -> bool:
        """
        Check if the specified cell is the center of a fully open 3x3 area.

        Parameters
        ----------
        x : int
            The row coordinate of the potential center.
        y : int
            The column coordinate of the potential center.

        Returns
        -------
        bool
            True if the 3x3 area around (x, y) has no internal standing walls, 
            False otherwise.
        """
        for m in [x - 1, x, x + 1]:
            for n in [y - 1, y, y + 1]:
                if (
                    not self.is_in_range(m, n) or
                    self.get_cell(m, n).is_forty_two
                ):
                    return False
        if self.get_cell(x, y).count_walls() > 0:
            return False
        for side in "EW":
            if (
                self.get_cell(x + 1, y).walls[side] or
                self.get_cell(x - 1, y).walls[side]
            ):
                return False
        for side in "NS":
            if (
                self.get_cell(x, y + 1).walls[side] or
                self.get_cell(x, y - 1).walls[side]
            ):
                return False
        return True
