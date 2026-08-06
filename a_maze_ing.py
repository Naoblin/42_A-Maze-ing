from mazegen import MazeGenerator
from process_config import load_config
import sys
from typing import Any

def main() -> None:
    # dopsat asi dodatečné kontroly, že je správný počet parametrů při zavolání funkce
    # že soubor existuje atd. - to asi zkontrolovat v processing_config() jeste
    
    param: dict[str, Any] = load_config(sys.argv[1])
    maze = MazeGenerator(width=param["WIDTH"], height=param["HEIGHT"],
                         entry=param["ENTRY"], exit=param["EXIT"],
                         perfect=param["PERFECT"])

    print(param)
    print("test")
    # pro generování bludiště zavoláme
    maze.generate()

    # pro hledání řešení bludiště zavoláme
    maze.solve()


if __name__ == "__main__":
    main()
