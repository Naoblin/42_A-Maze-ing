from typing import Any
import sys

KEYS = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
KEYS_OPTIONAL = ["SEED"]
MIN_SIZE_LIMIT = 2


def load_config(config_file: str) -> dict[str, Any]:
    """
    Load and parse the maze configuration from a file.

    Reads the specified file line by line, extracts key-value pairs,
    and validates them. It also performs mandatory key checks and
    coordinate boundary validation.

    Parameters
    ----------
    config_file : str
        The path to the configuration text file.

    Returns
    -------
    dict[str, Any]
        A dictionary containing the parsed configuration parameters.

    Raises
    ------
    SystemExit
        If the file cannot be opened or if any validation error occurs.
    """
    config_dict: dict[str, Any] = {}

    try:
        with open(config_file) as config:
            for line in config:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                try:
                    key, value = check_key_value(line)
                except ValueError as e:
                    sys.exit(str(e))
                else:
                    config_dict[key] = value
    except OSError as e:
        sys.exit(f"An error occured while opening the config file: {str(e)}")

    try:
        check_mandatory(config_dict, config_file)
    except ValueError as e:
        sys.exit(str(e))

    return config_dict


def check_mandatory(config: dict[str, Any], config_file: str) -> None:
    """Ensure all mandatory configuration keys are present.

    Parameters
    ----------
    config : dict[str, Any]
        The dictionary of parsed configuration parameters.
    config_file : str
        The name of the configuration file, used for error reporting.

    Raises
    ------
    ValueError
        If any key from the mandatory KEYS list is missing.
    """
    for key in KEYS:
        if key not in config:
            raise ValueError(f"The mandatory parameter {key} is missing "
                             f"in '{config_file}'.")


def check_key_value(key_value_pair: str) -> tuple[str, Any]:
    """
    Parse and validate a single configuration line.

    Splits a 'KEY=VALUE' string, checks if the key is allowed, and
    converts the value to its appropriate data type (integer, tuple,
    or boolean).

    Parameters
    ----------
    key_value_pair : str
        A single line from the configuration file.

    Returns
    -------
    tuple[str, Any]
        A tuple containing the parsed key and its typed value.

    Raises
    ------
    ValueError
        If the format is incorrect, the key is unknown, or the value
        is invalid for the given key.
    """
    separ_pair: list[str] = key_value_pair.split("=")
    if len(separ_pair) != 2:
        raise ValueError("Wrong format, exactly one '=' must be used. "
                         "Key-Value pair must be written on one line "
                         "as 'KEY=VALUE'.")

    key: str = separ_pair[0].strip()
    value: Any = separ_pair[1].strip()
    if key != key.upper():
        raise ValueError("Wrong format, keys must be written in uppercase!")
    if key not in KEYS and key not in KEYS_OPTIONAL:
        raise ValueError(f"'{key}' is not an allowed key. "
                         f"Allowed keys are: {KEYS}")

    if key == "WIDTH" or key == "HEIGHT":
        value = int(value)

    elif key == "ENTRY" or key == "EXIT":
        if len(value.split(",")) != 2:
            raise ValueError(f"Wrong format of key {key}, exactly one ',' "
                             f"must be used. (x, y) coordinates of {key} "
                             f"must be written as {key}=x,y.")
        x, y = value.split(",")
        value = (int(x), int(y))

    elif key == "PERFECT":
        if value == "True":
            value = True
        elif value == "False":
            value = False
        else:
            raise ValueError(f"Value '{value}' is not allowed for key {key}. "
                             "Allowed values are 'True' or 'False'")

    return key, value


if __name__ == "__main__":
    print(load_config(sys.argv[1]))
