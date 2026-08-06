from typing import Any
import sys

KEYS = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
MIN_SIZE_LIMIT = 2


def load_config(config_file: str) -> dict[str, Any]:
    config_dict: dict[str, Any] = {}

    # Extracting KEY and VALUE from every line and adding it to a dictionray
    with open(config_file) as config:
        for line in config:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                key, value = check_key_value(line)
            except ValueError as e:
                sys.exit(str(e))  # neplatny config file -> ukoncit program
            else:
                config_dict[key] = value

    try:
        check_mandatory(config_dict, config_file)
        check_entry_exit(config_dict)
    except ValueError as e:
        sys.exit(str(e))  # neplatny config file -> ukoncit program

    return config_dict


def check_mandatory(config: dict[str, Any], config_file: str) -> None:
    # kontrola, ze vsechny mandatory klice byly pouzity v config file
    for key in KEYS:
        if key not in config:
            raise ValueError(f"The mandatory parameter {key} is missing "
                             f"in '{config_file}'.")


def check_entry_exit(config: dict[str, Any]) -> None:
    for gate in ["ENTRY", "EXIT"]:
        x, y = config[gate]
        if not (0 <= x < config["WIDTH"]):
            raise ValueError(f"The 'x' coordinate of {gate} ({x}) is out of "
                             f"range (0, {config['WIDTH']})")
        if not (0 <= y < config["HEIGHT"]):
            raise ValueError(f"The 'y' coordinate of {gate} ({y}) is out of "
                             f"range (0, {config['HEIGHT']})")


def check_key_value(key_value_pair: str) -> tuple[str, Any]:

    # get KEY and VALUE separated by '='
    separ_pair: list[str] = key_value_pair.split("=")
    if len(separ_pair) != 2:
        raise ValueError("Wrong format, exactly one '=' must be used. "
                         "Key-Value pair must be written on one line "
                         "as 'KEY=VALUE'.")

    # strip KEY and VALUE from whitespaces
    key: str = separ_pair[0].strip()
    value: Any = separ_pair[1].strip()
    if key != key.upper():
        raise ValueError("Wrong format, keys must be written in uppercase!")
    if key not in KEYS:
        raise ValueError(f"'{key}' is not an allowed key. "
                         f"Allowed keys are: {KEYS}")

    if key == "WIDTH" or key == "HEIGHT":
        value = int(value)
        if value < MIN_SIZE_LIMIT:
            raise ValueError(f"{key} cannot be less than {MIN_SIZE_LIMIT}")

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
            raise ValueError(f"Value {value} is not allowed for key {key}. "
                             "Allowed values are 'True' od 'False'")

    return key, value


if __name__ == "__main__":
    print(load_config(sys.argv[1]))
