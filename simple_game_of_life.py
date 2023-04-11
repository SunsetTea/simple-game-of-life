# -*- coding: utf-8 -*-
# A "." is used to represent the cells that are dead, while "*" represents those that are alive.

import os
import time
import copy
from colorama import Fore
from colorama import Style

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def generate_dotted_matrix(lines, columns):
    matrix = []
    for line in range(lines):
        matrix.append([])
        for column in range(columns):
            matrix[line].append(".")

    return matrix


def modify_matrix(matrix, positions_to_set):
    for position in positions_to_set:
        matrix[position[0]][position[1]] = "*"


def generate_pattern(pattern_key, pattern_dict):
    pattern_entry = pattern_dict[pattern_key]
    original_state = generate_dotted_matrix(
        pattern_entry[0][0], pattern_entry[0][1])
    new_state = generate_dotted_matrix(
        pattern_entry[0][0], pattern_entry[0][1])

    modify_matrix(original_state, pattern_entry[1])

    return original_state, new_state


def print_matrix(matrix, current_gen, refresh_rate):
    time.sleep(refresh_rate)
    clear_console()

    population = 0
    for line in matrix:
        print()
        for column in line:
            if (column == "*"):
                print(f"{Fore.GREEN}{column}{Style.RESET_ALL}", end=" ")
                population += 1
            else:
                print(column, end=" ")
    print()

    print(f"Population: {population}")
    print(f"Generation: {current_gen}")


def check_neighbours(matrix, line, column):
    alive_neighbours = 0
    if (line-1 >= 0):
        for i in range(column-1, column+2):
            if (i >= 0 and i < len(matrix[line])):
                if (matrix[line-1][i] == "*"): alive_neighbours += 1
    
    for j in range(column-1, column+2):
        if (j >= 0 and j < len(matrix[line]) and j != column):
            if(matrix[line][j] == "*"): alive_neighbours += 1
    
    if (line+1 < len(matrix)):
        for k in range(column-1, column+2):
            if (k >= 0 and k < len(matrix[line])):
                if(matrix[line+1][k] == "*"): alive_neighbours += 1
    
    return alive_neighbours


def main():
    patterns = {1: ((4, 4), ((1, 1), (1, 2), (2, 1), (2, 2))),
                2: ((5, 6), ((1, 2), (1, 3), (2, 1), (2, 4), (3, 2), (3, 3))),
                3: ((5, 5), ((1, 2), (2, 1), (2, 3), (3, 2))),
                4: ((8, 8), ((2, 3), (2, 4), (3, 2), (4, 5), (5, 3), (5, 4))),
                5: ((17, 17), ((2, 4), (2, 5), (2, 6), (2, 10), (2, 11), (2, 12), (4, 2), (4, 7), (4, 9), (4, 14), (5, 2), (5, 7),
                            (5, 9), (5, 14), (6, 2), (6, 7), (6, 9), (6, 14), (7, 4), (7, 5), (7, 6), (7, 10), (7, 11), (7, 12),
                            (9, 4), (9, 5), (9, 6), (9, 10), (9, 11), (9, 12), (14, 4), (14, 5), (14, 6), (14, 10), (14, 11), (14, 12),
                            (10, 2), (10, 7), (10, 9), (10, 14), (11, 2), (11, 7), (11, 9), (11, 14), (12, 2), (12, 7), (12, 9), (12, 14))),
                6: ((11, 18), ((4, 6), (4, 11), (5, 4), (5, 5), (5, 7), (5, 8), (5, 9), (5, 10), (5, 12), (5, 13), (6, 6), (6, 11))),
                7: ((25, 25), ((1, 3), (2, 4), (3, 2), (3, 3), (3, 4)))}


    while True:

        print("\n" + " MENU ".center(30, "-"))
        print("\n" + " STILL LIFES ".center(25, "*"))
        print("1. Block")
        print("2. Bee-hive")
        print("3. Tub")
        print("\n" + " OSCILLATORS ".center(25, "*"))
        print("4. Toad")
        print("5. Pulsar")
        print("6. Penta-decathlon")
        print("\n" + " SPACESHIPS ".center(25, "*"))
        print("7. Glider")

        print("8. EXIT" + "\n")

        while True:
            try:
                chosen_pattern = int(
                    input("Choose a pattern to visualize: ").strip())
            except ValueError:
                print("Please enter a valid input.")
            else:
                if chosen_pattern in range(1, 9): break
                print("Please enter a valid range.")

        if chosen_pattern == 8: break

        original_matrix, new_matrix = generate_pattern(chosen_pattern, patterns)
        
        match chosen_pattern:
            case 1 | 2 | 3 :
                generations = 15
                refresh = 0.75
            case 4 | 5 | 6:
                generations = 40
                refresh = 0.75
            case 7:
                generations = 90
                refresh = 0.3

        for gen in range(generations):

            print_matrix(original_matrix, gen+1, refresh)

            for current_line in range(len(original_matrix)):
                for current_column in range(len(original_matrix[current_line])):

                    alive_neighbours = check_neighbours(original_matrix, current_line, current_column)

                    if (alive_neighbours == 2 and original_matrix[current_line][current_column] == "*") or alive_neighbours == 3:
                        # All live cells with 2 or 3 live neighbours survive.
                        # Dead cells with 3 live neighbours become alive.
                        new_matrix[current_line][current_column] = "*"
                    else:
                        # Live cells with less than 2 live neighbours die.
                        # Dead cells with less than 3 live neighbours stay dead.
                        # Live cells with more than 3 live neighbours die.
                        # Dead cells with more than 3 live neighbours stay dead.
                        new_matrix[current_line][current_column] = "."

            original_matrix = copy.deepcopy(new_matrix)


if __name__ == "__main__":
    main()
