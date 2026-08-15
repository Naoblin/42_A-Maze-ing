
## Instructions

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
maze = MazeGenerator(width=20, height=15, entry=(0,0), exit=(19,14), perfect=False, seed=42)
```
*The `perfect` (whether the maze will have no loops, defaults to False) and `seed` (for reproducibility) parameters are optional.*

**Basic Sequence of Methods:**
The methods should be called in this logical order:

1.  **`maze.generate()`**: Generates the maze structure and sets the entry and exit points.
2.  **`maze.solve()`**: Finds the shortest path (if you want to solve the maze).
3.  **`maze.make_output_file()`**: (Optional) Exports the hex-based maze layout, coordinates, and solution to a file named `output_maze.txt`.
4.  **`maze.display(show_solution=True, color_walls=0, color_42=1)`**: (Optional) Renders the maze in the terminal. You can set the solution visibility and colors (ANSI codes 0-6).
