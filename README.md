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


### Interactive Display Interface
- (Optional) Advanced display options, if you support more than one

### Reusability
- What part of the code is reusable, and how (this is where the "Python module" point from earlier lives)

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
