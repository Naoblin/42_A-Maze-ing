from typing import Any

KEYS = [WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT]
MIN_SIZE_LIMIT = 2

def load_config() -> dict[str: Any]:
    config_dict: dict[str: str] = {}

    # Extracting KEY and VALUE from every line and adding it to a dictionray
    with open("config.txt") as config_file:
        for line in config_file:
            try:
                key, value = check_key_value(line)
            except ValueError as e:
                print(e)
            else:
                config_dict[key] = value

    return config_dict

def check_key_value(key_value_pair: str) -> tuple(str, Any):

    # get KEY and VALUE separated by '='
    separ_pair: list[str, str] = key_value_pair.split("=")
    if len(separ_pair) != 2:
        raise ValueError("Wrong format, exactly one '=' must be used. Key-Value pair must be written on one line as 'KEY=VALUE'.")

    # strip KEY and VALUE from whitespaces
    key = separ_pair[0].strip()
    value = separ_pair[1].strip()
    if key != key.upper():
        raise ValueError("Wrong format, keys must be written in uppercase!")
    if key not in KEYS:
        raise ValueError(f"Key '{key}' is not an allowed key. Allowed keys are: {KEYS}")

    if (key == "WIDTH" or key == "HEIGHT") and key < MIN_SIZE_LIMIT:
        raise ValueError(f"{key} cannot be less than {MIN_SIZE_LIMIT}")

    elif key == "ENTRY" or key == "EXIT":
        if len(value.split(",")) != 2:
            raise ValueError(f"Wrong format of {key} key, exactly one ',' must be used. (x, y) coordinates of {key} must be written as {key}=x,y.")
        x, y = value.split(",")
        x = int(x)
        y = int(y)
    # zasekl jsem se zde, protoze je potreba zkontrolovat, ze je souradnice x mezi 0 a WIDTH (obdobne pro y)
    # v teto funkci ale nemam pristup do vytvoreneho slovniku a tedy hodnoty WIDTH
    # asi budu muset tuto funki zjednodusit  a tuto kontrolu a ine presunout jinam




if __name__ == "__main__":
    pass