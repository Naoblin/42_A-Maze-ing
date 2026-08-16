from mazegen import MazeGenerator
from process_config import load_config
from interactive_mode import display_interactive
import sys
from typing import Any


def main() -> None:
    """
    Execute the main application flow.

    This function serves as the entry point of the script. It parses
    command-line arguments, loads the configuration file, instantiates
    the MazeGenerator, and starts the interactive display mode.

    Raises
    ------
    SystemExit
        If the number of provided command-line arguments is not exactly one.
    """
    if len(sys.argv) > 2:
        sys.exit("One argument is expected. More than one were provided.")
    elif len(sys.argv) < 2:
        sys.exit("One argument is expected. None was provided.")

    param: dict[str, Any] = load_config(sys.argv[1])

    try:
        if "SEED" in param:
            maze = MazeGenerator(width=param["WIDTH"], height=param["HEIGHT"],
                                 entry=param["ENTRY"], exit=param["EXIT"],
                                 output_file=param["OUTPUT_FILE"],
                                 perfect=param["PERFECT"], seed=param["SEED"])
        else:
            maze = MazeGenerator(width=param["WIDTH"], height=param["HEIGHT"],
                                 entry=param["ENTRY"], exit=param["EXIT"],
                                 output_file=param["OUTPUT_FILE"],
                                 perfect=param["PERFECT"])
        display_interactive(maze)
    except ValueError as e:
        sys.exit(str(e))
    except RuntimeError as e:
        sys.exit(str(e))
    except OSError as e:
        sys.exit("An error occured while writing to the output file: "
                 f"{str(e)}")


if __name__ == "__main__":
    main()
