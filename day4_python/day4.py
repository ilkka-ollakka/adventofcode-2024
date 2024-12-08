#/bin/env python3.12
from typing import Generator, Any, Callable
from itertools import product

letters = []
#with open("day4_input.txt") as f:
with open("test.txt") as f:
    for line in f:
        letters.append(list(line.strip()))

max_x = len(letters[0])
max_y = len(letters)

def part1(x:int, y:int) -> Generator[list[tuple[int, int, str]], None, Any]:
    WORD_TO_MATCH = "XMAS"
    for x_offset, y_offset in [(1, 1), (1, 0), (0, 1), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
        #print(x_position, y_position)
        list_to_return = []
        for offset, needed_letter in enumerate(WORD_TO_MATCH):
            x_position = x+(x_offset * offset)
            y_position = y+(y_offset * offset)
            if not (0 <= x_position < max_x and 0 <= y_position< max_y):
                break
            list_to_return.append((x_position, y_position, needed_letter))
        else:
            yield list_to_return

def part2(x:int, y:int) -> Generator[list[tuple[int, int, str]], None, Any]:
    teksti="MAS"
    teksti2=teksti[::-1]
    for match1, match2 in product([teksti, teksti2], repeat=2):
        pisteet = [(x+int(index), y+int(index), character) for index,character in enumerate(match1, start=int(len(teksti)/-2))]
        pisteet.extend([(x+-1*int(index), y+int(index), character) for index,character in enumerate(match2, start=int(len(teksti)/-2))])
        if all(0 <= x_point < max_x and 0 <= y_point < max_y for x_point, y_point, _ in pisteet):
            yield pisteet



def find_words(letters: list[list[str]], directions: Callable, letter_to_check: str) -> int:
    words_found = 0
    for y, row in enumerate(letters):
        for x, letter in enumerate(row):
            # Check only letter mentioned to skip points we know can't match
            if letter != letter_to_check:
                continue

            for point_letter in directions(x, y):
                for x_point, y_point, letter in point_letter:
                    if letters[y_point][x_point] != letter:
                        break
                else:
                    words_found += 1
                    #print(f"{x=} {y=}, {max_x=} {max_y=}, {point_letter=}")
    return words_found

print(f"Part 1: {find_words(letters, part1, 'X')}")
print(f"Part 2: {find_words(letters, part2, 'A')}")
