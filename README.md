*This project has been created as part of the 42 curriculum by lnovakov, lnovotny.*

# Description
A-Maze-ing is a 42 project focused on creating a maze generator python tool. The program generates mazes from a configuration file. It can produce perfect mazes (exactly one path between entrance and exit) or playable mazes (many loops, almost none dead-ends, ideal for pac-man like games) and saves the result to a file using a hex-based wall representation. It also renders a visual version of the maze so you can see what was generated.

The maze generation logic is designed to be reusable as a standalone Python module, so it can easily be integrated into other projects.

## Design

### Configuration File

The configuration file uses a simple `KEY=VALUE` format, one pair per line. Lines starting with `#` are treated as comments and ignored.

**Mandatory keys:**

| Key           | Description                  | Example              |
|---------------|-------------------------------|-----------------------|
| `WIDTH`       | Maze width (number of cells)  | `WIDTH=20`            |
| `HEIGHT`      | Maze height (number of cells) | `HEIGHT=15`           |
| `ENTRY`       | Entry coordinates (x,y)       | `ENTRY=0,0`           |
| `EXIT`        | Exit coordinates (x,y)        | `EXIT=19,14`          |
| `OUTPUT_FILE` | Output filename               | `OUTPUT_FILE=maze.txt`|
| `PERFECT`     | Whether the maze is perfect   | `PERFECT=True`        |

**Optional keys:**

| Key    | Description                                      | Example     |
|--------|---------------------------------------------------|-------------|
| `SEED` | Seed value to reproduce the same maze on demand    | `SEED=42`   |

**Example config file:**

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```
#### Config Validation

Each line is parsed into a `KEY=VALUE` pair, validated, and converted to the correct type (integers, coordinate tuples, booleans). The program checks for missing mandatory keys, invalid values, and valid `ENTRY`/`EXIT` coordinates, exiting with an error message if the config file is invalid.

### MazeGenerator Class
`MazeGenerator` is the main interface for working with mazes. It takes the maze dimensions, entry/exit points, and optional settings perfect (default is False) and seed on initialization, then exposes four core methods: `generate()` to build the maze, `solve()` to find the shortest path, `display()` to print it, and `make_output_file()` to export the hex layout, entry and exit points and solution to a file.

### Maze Generation Algorithm
The maze generation algorithm utilizes the **Recursive Backtracker** (Randomized depth-first search) method.

This algorithm works by choosing a random starting cell (that is not part of the pre-defined '42' pattern), marking it as visited, and adding it to a stack. Then, in a loop:
1. It looks at the cell on top of the stack.
2. It checks if the cell has any unvisited neighbors.
3. If it does, it randomly selects one, removes the wall between the current and the selected cell, marks the neighbor as visited, and pushes it onto the stack.
4. If there are no unvisited neighbors (a dead end), the algorithm removes the current cell from the stack (backtracks) and repeats the process.
This continues until the stack is empty, meaning all accessible cells have been visited and the maze is generated.

When `PERFECT=FALSE`, this step runs after the initial perfect maze is generated. It converts the maze into a playable one by identifying all dead ends, randomly removing one wall per dead end, and ensuring no 3x3 open areas are created.

We chose this algorithm because it offers a very good balance between implementation simplicity and the quality of the generated maze. It generates visually interesting mazes with long, winding corridors and fewer short dead ends, which is ideal for our purposes.

> If the specified maze dimensions are smaller than 9x7 (width x height), an error message is printed and the maze is generated without the mandatory '42' pattern in the center.

### Maze Solving Algorithm
After researching various solving algorithms, we decided to go with **Breadth-First Search** (BFS). It's relatively simple to implement and it guarantees the shortest path between the entry and exit. Starting from the entry cell, the algorithm explores all reachable neighbours level by level, keeping track of how each cell was reached until it finds the exit. Once the exit is found, the path is reconstructed backwards to the entry and returned as a string of directions (e.g. `NESW`). If no path exists, an error is raised.

### Output File

Once a maze is generated and solved, it can be exported using `make_output_file()`. The file contains three parts, separated by blank lines:

1. **The maze layout** — one line per row, where each character is a hexadecimal digit (0-F) encoding the walls standing around that cell.
2. **The entry and exit coordinates** — one `x, y` pair per line.
3. **The solution path** — a string of directions (`N`, `E`, `S`, `W`) from entry to exit.

Each hex digit is a sum of bit values for the walls present on that cell: `N = 1`, `E = 2`, `S = 4`, `W = 8`. For example, a cell with only the North and West walls standing would be `1 + 8 = 9`.

**Example:**

```
95139553953
83C2C154696
AAFA96FFFC3
AAFC4157F92
86FFFAFFFAA
C393FAFD52A
946AFAFFFAA
853C50393C2
C54556C6C56

0, 0
10, 8
EEESSSEESSSSESENESEE
```

### Interactive Display Interface
Entering interactive mode generates the maze, solves it, and saves it to the output file, then drops into a terminal menu where the maze is redrawn after every action. From there, you can regenerate a new maze, toggle the solution path on or off, and cycle through wall and '42' pattern colors. Choosing exit ends the session.

Note that this interactive loop is specific to the CLI program and is not part of the reusable module. Only the underlying `display()` method is exposed for reuse elsewhere.

### Reusability
The reusable part of the code is the MazeGenerator class from the mazegen module with its methods described in the **MazeGenerator Class** chapter. The **Instructions** section describes how to use this module.

The core maze logic (generation, solving, and display) is implemented as a self-contained Python module (`mazegen`), independent of the config file parsing and the interactive CLI. This means it can be imported and used directly in other Python projects, without needing a config file or the terminal interface at all.

```python
from mazegen import MazeGenerator

maze = MazeGenerator(width=20, height=15, entry=(0, 0), exit=(19, 14), output_file="maze.txt", perfect=True)
maze.generate()
maze.solve()
maze.display()
maze.make_output_file()
```

Only the interactive menu loop (`display_interactive`) and config validation are specific to the standalone program and are not part of the reusable module.

> The `mazegen` package, along with its license, is distributed as a standalone `.whl`/`.tar.gz` file at the root of this repository. See [`LICENSE.md`](./LICENSE.md) for reuse terms.

## Team & Project Management

### Roles of each team member

**Lucie Nováková:**
- Maze solving algorithm (BFS)
- Interactive terminal interface

**Lukáš Novotný:**
- Maze generation algorithm (Recursive Backtracker)
- Configuration parsing and validation

**Both:**
- Terminal maze rendering / display logic
- Project documentation (README)

### Anticipated planning and how it evolved

At the beginning, we agreed that Lucka would implement the maze-solving logic while Lukáš would handle maze generation, leaving the remaining tasks to be assigned dynamically based on progress. We maintained active communication throughout development; whenever one of us finished a part of the project, we discussed the next steps before moving forward.

For version control, we used a main branch alongside a personal branch for each team member. Development was carried out on individual branches and then submitted to main via pull requests. Every pull request was reviewed by the other team member prior to merging. We kept the same personal branches from the start to the end of the project.

### Tools used (and why)

Our primary tool was GitHub, which we used to keep our shared codebase in sync during development. Setting it up this way let both of us work on the project separately while making it easy to review and discuss each other's changes using pull requests.

### What worked well and what could be improved

 - **What worked well:** Communication and teamwork went smoothly throughout the entire project, allowing us to align on tasks and solve problems efficiently.
 - **What could be improved:** Next time, we would improve our Git workflow. Instead of using a single long-lived personal branch for the entire project, adopting dedicated feature branches for individual tasks would provide better isolation and a cleaner commit history. Additionally, we would implement unit tests from the beginning of development to avoid repetitive manual testing after every major change.

# Instructions

### Installing the `mazegen` Module

To use the maze generator as a module, you need to install it first. It is highly recommended to perform the installation within an isolated virtual environment.

1.  Create and activate a virtual environment:

    You can use these commands to use the virtual environment:

    create
    ```
    python3 -m venv <venv_name>
    ```
    activate
    ```
    source <venv_name>/bin/activate
    ```
    deactivate
    ```
    deactivate
    ```

2.  Install the package using `pip` (e.g., from the provided `.whl` file):
    ```bash
    pip install mazegen-1.0.0-py3-none-any.whl
    ```
    *Note: The project also includes a `make install` command that performs this installation.*

### Building Installation Packages (.tar.gz and .whl)

If you need to build the installation packages from the source code (which requires the `pyproject.toml` file included in this project), follow these steps:

1.  Ensure you have the `build` tool installed:
    ```bash
    pip install build
    ```
2.  Run the build command in the root directory of the project (where `pyproject.toml` is located):
    ```bash
    python3 -m build
    ```
3.  The resulting archives (`.tar.gz` and `.whl`) will be found in the generated `dist/` directory.

### Using the `mazegen` Module

To use the module in your own code, you need to create an instance of the `MazeGenerator` class and call its methods.

**Initialization:**
Create an instance of the class with the desired parameters:
```python
from mazegen import MazeGenerator

# Creating a 20x15 maze, entry at [0,0], exit at [19,14]
maze = MazeGenerator(width=20, height=15, entry=(0,0), exit=(19,14), output_file="maze.txt", perfect=False, seed=42)
```
*The `perfect` (whether the maze will have no loops, defaults to False) and `seed` (for reproducibility) parameters are optional.*

**Custom Parameters:**
The parameters correspond to the grid as follows:

* **Width:** The number of columns.
* **Height:** The number of rows.
* **Entry and Exit:** Tuples in the format `(x, y)`, where `x` represents the column and `y` represents the row.

Besides the mandatory `width`, `height`, `entry`, `exit` and `output_file`, two optional parameters are available:

- `perfect` (`bool`, default `False`) — if `True`, generates a perfect maze (exactly one path between entry and exit).
- `seed` (default `None`) — sets the random seed, so the same parameters always produce the same maze.

**Basic Sequence of Methods:**
The methods should be called in this logical order:

1.  **`maze.generate()`**: Generates the maze structure and sets the entry and exit points.
2.  **`maze.solve()`**: Finds the shortest path (if you want to solve the maze).
3.  **`maze.make_output_file()`**: (Optional) Exports the hex-based maze layout, coordinates, and solution to a file named `output_maze.txt`.
4.  **`maze.display(show_solution=True, color_walls=0, color_42=1)`**: (Optional) Renders the maze in the terminal. You can set the solution visibility and colors (ANSI codes 0-6).

### How to Use PDB (Python Debugger)

PDB is a built-in Python tool for interactive debugging directly from the command line. It allows you to pause the execution of a program, step through the code, and inspect the state of variables.

The easiest way to run PDB with your script is to call it directly as a module:

```bash
python3 -m pdb script.py [arguments]
```
*Note: In this project, the `make debug` command is prepared to run the script with PDB.*

Once executed, the program stops at the first line and opens an interactive `(Pdb)` console. You can control the code using the following commands:

*   **`l`** (list): Displays 11 lines of code around the current execution point.
*   **`n`** (next): Executes the current line and stops at the next one. It does not step into called functions.
*   **`s`** (step): Executes a single step. If there is a function call on the line, it steps inside the function so you can debug it.
*   **`c`** (continue): Resumes the program's execution until it finishes or hits a breakpoint.
*   **`p <variable>`** (print): Prints the current value of the specified variable (e.g., `p x`).
*   **`b <line_or_function>`** (break): Sets a breakpoint at the specified line or at the beginning of a function.
*   **`q`** (quit): Immediately terminates the debugger and the running program.

*Tip: If you simply press `Enter`, the last entered command is repeated (useful for quick stepping with `n`).*

From Python 3.7 onwards, you can also directly insert the `breakpoint()` function into your code. If you then run the script normally (without `-m pdb`), the program will run at full speed and stop (opening the Pdb console) exactly where you placed the `breakpoint()`.

# Resources
- [Jamis Buck: "Algorithm" is Not a Four-Letter Word](https://www.jamisbuck.org/presentations/rubyconf2011/index.html) - RubyConf 2011 talk (Jamis Buck) with interactive demos of major maze-generation algorithms
- [Red Blob Games: Introduction to the A* Algorithm](https://www.redblobgames.com/pathfinding/a-star/introduction.html) - interactive introduction to A and related graph search algorithms, with hands-on animated visualizations
- [Python Docstrings - GeeksforGeeks](https://www.geeksforgeeks.org/python/python-docstrings/) - reference on writing and formatting Python docstrings, including different documentation styles (Google, Numpydoc)
- [MIT License - Wikipedia](https://en.wikipedia.org/wiki/MIT_License) - information about the MIT License used in this project
- [Claude AI](https://claude.ai/) - AI assistant for debugging, understanding concepts and drafting docs
- [Google Gemini](gemini.google.com) - AI assistant for debugging, understanding concepts, drafting docs and creating docstrings
