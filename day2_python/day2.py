#!/usr/bin/env python3.12
from typing import Any, Generator
import itertools

def check_delta_value(value: int, ascending: bool) -> bool:
    max_step = 3
    min_step = 1
    if not (min_step <= abs(value) <= max_step):
        return False
    if ascending is (value < 0):
        return False
    return True

def check_line(numbers: list[int]) -> bool:
    delta_line = list(map(lambda x, y: x - y, numbers[1:], numbers[:-1]))
    return all(check_delta_value(delta_value, numbers[0] < numbers[1]) == True for delta_value in delta_line)

def part1(input_lines: Generator[list[int], Any, None]) -> int:
    return sum([ 1 if check_line(line) else 0 for line in input_lines ])

def part2(input_lines: Generator[list[int], Any, None]) -> int:
    result = 0
    for line in input_lines:
        if check_line(line):
            result += 1
            continue
        # take n-1 combinations to try if dropping one value makes the set valid
        for new_values in itertools.combinations(line, len(line) - 1):
            if check_line(list(new_values)):
                result += 1
                break


    return result

def input_generator():
    with open('test.txt') as f:
        for line in f:
            input_numbers = list(map(int, line.split()))
            yield input_numbers

print(f"Part 1: {part1(input_generator())}")
print(f"Part 2: {part2(input_generator())}")

