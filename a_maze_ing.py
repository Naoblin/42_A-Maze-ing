from mazegen import MazeGenerator
from process_config import load_config
import sys
from typing import Any

def main() -> None:
    # dopsat asi dodatečné kontroly, že je správný počet parametrů při zavolání funkce
    # že soubor existuje atd. - to asi zkontrolovat v processing_config() jeste
    
    param: dict[str, Any] = load_config(sys.argv[1])

    if "SEED" in param:
        maze = MazeGenerator(width=param["WIDTH"], height=param["HEIGHT"],
                            entry=param["ENTRY"], exit=param["EXIT"],
                            perfect=param["PERFECT"], seed=param["SEED"])
    else:
        maze = MazeGenerator(width=param["WIDTH"], height=param["HEIGHT"],
                            entry=param["ENTRY"], exit=param["EXIT"],
                            perfect=param["PERFECT"])

    # pro generování bludiště zavoláme
    maze.generate()
    maze.display()

    # pro hledání řešení bludiště zavoláme
    print()
    maze.solve()
    maze.display()
    maze.make_output_file()

if __name__ == "__main__":
    main()
