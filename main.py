import os
import sys
from world_cup import WorldCup

def main(arguments) -> None:
    if len(arguments) < 3:
        print("not enough parameters, please provide 1. root directory \n \
                2. Excel input bet file name \n \
                3. Name for the results output file")
        return
    source_dir = arguments[1]
    source_file_name = arguments[2]
    results_file_name = arguments[3]

    if not os.path.exists(source_dir):
        print("Root directory not found")
        return

    source_path = os.path.join(source_dir, source_file_name)
    results_path = os.path.join(source_dir, results_file_name)

    if not os.path.exists(source_path):
        print("Not a valid source path")
        return

    world_cup = WorldCup(source_path, results_path)
    world_cup.calculate_results()

if __name__ == '__main__':
    main(sys.argv)