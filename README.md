*This project has been created as part of the 42 curriculum by lnovakov, lnovotny.*

# Description
A-Maze-ing is a 42 project focused on creating a maze generator python tool. The program generates mazes from a configuration file. It can produce perfect mazes (exactly one path between entrance and exit) and saves the result to a file using a hex-based wall representation. It also renders a visual version of the maze so you can see what was generated.

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
| `SEED` | Seed value to reproduce the same maze on demand    | `SEED=gdgsagdrgd`   |

**Example config file:**

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=gdgsagdrgd
```
#### Config Validation

Each line is parsed into a `KEY=VALUE` pair, validated, and converted to the correct type (integers, coordinate tuples, booleans). The program checks for missing mandatory keys, invalid values, and valid `ENTRY`/`EXIT` coordinates, exiting with an error message if the config file is invalid.

### `MazeGenerator` Class
`MazeGenerator` is the main interface for working with mazes. It takes the maze dimensions, entry/exit points, and optional settings (`perfect`, `seed`) on initialization, then exposes four core methods: `generate()` to build the maze, `solve()` to find the shortest path, `display()` to print it, and `make_output_file()` to export the hex layout and solution to a file.

### Maze Generation Algorithm
TODO: Lukas
- The algorithm you chose
- Why you chose it
- (Optional) Advanced features — multiple algorithms, alternate generation modes

### Maze Solving Algorithm
After researching various solving algorithms, we decided to go with Breadth-First Search (BFS). It's relatively simple to implement and it guarantees the shortest path between the entry and exit. Starting from the entry cell, the algorithm explores all reachable neighbours level by level, keeping track of how each cell was reached until it finds the exit. Once the exit is found, the path is reconstructed backwards to the entry and returned as a string of directions (e.g. `NESW`). If no path exists, an error is raised.

### Interactive Display Interface
Entering interactive mode generates the maze, solves it, and saves it to the output file, then drops into a terminal menu where the maze is redrawn after every action. From there, you can regenerate a new maze, toggle the solution path on or off, and cycle through wall and '42' pattern colors. Choosing exit ends the session.

Note that this interactive loop is specific to the CLI program and is not part of the reusable module. Only the underlying `display()` method is exposed for reuse elsewhere.

### Reusability

The core maze logic (generation, solving, and display) is implemented as a self-contained Python module (`mazegen`), independent of the config file parsing and the interactive CLI. This means it can be imported and used directly in other Python projects, without needing a config file or the terminal interface at all.

```python
from mazegen import MazeGenerator

maze = MazeGenerator(width=20, height=15, entry=(0, 0), exit=(19, 14), perfect=True)
maze.generate()
maze.solve()
maze.display()
maze.make_output_file()
```

Only the interactive menu loop (`display_interactive`) and config validation are specific to the standalone program and are not part of the reusable module.

## Team & Project Management
- Roles of each team member
- Anticipated planning and how it evolved
- What worked well and what could be improved
- Tools used (and why)

# Instructions
TODO: Lukas

# Resources
- [Jamis Buck: "Algorithm" is Not a Four-Letter Word](https://www.jamisbuck.org/presentations/rubyconf2011/index.html) - RubyConf 2011 talk (Jamis Buck) with interactive demos of major maze-generation algorithms
- [Red Blob Games: Introduction to the A* Algorithm](https://www.redblobgames.com/pathfinding/a-star/introduction.html) - interactive introduction to A and related graph search algorithms, with hands-on animated visualizations
- [Python Docstrings - GeeksforGeeks](https://www.geeksforgeeks.org/python/python-docstrings/) - reference on writing and formatting Python docstrings, including different documentation styles (Google, Numpydoc)
- [Claude AI](https://claude.ai/) - AI assistant for debugging, understanding concepts and drafting docs

TODO: do not forget things from the list below!!!!!
# Additional Requirements

Any required additions will be explicitly listed below. 
• The complete structure and format of your config file. 
• The maze generation algorithm you chose. 
• Why you chose this algorithm. 
• What part of your code is reusable, and how. 
• Your team and project management with: 
    ◦ The roles of each team member. 
    ◦ Your anticipated planning and how it evolved until the end 
    ◦ What worked well and what could be improved 
    ◦ Have you used any specific tools? Which ones? This is the way If you implement advanced features (multiple algorithms, display options), describe them in this README.md file.
