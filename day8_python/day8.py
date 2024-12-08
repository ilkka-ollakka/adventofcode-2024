#!/bin/env python3.12
from itertools import combinations 
from typing import Generator, Callable

antennas: dict[str, set[complex]] = {}

max_y = 0
max_x = 0
with open("test.txt") as f:
    for y, line in enumerate(f, start=1):
        max_y = y
        max_x = len(line.strip())
        for x, c in enumerate(line.strip(), start=1):
            if c != ".":
                if c not in antennas:
                    antennas[c] = set()
                antennas[c].add(complex(x, y))


def antinodes_part1(first: complex, second: complex) -> Generator[complex, None, None]:
    difference = second - first
    yield first - difference
    yield second + difference

def antinodes_part2(first: complex, second: complex) -> Generator[complex, None, None]:
    difference = second - first
    yield first
    yield second
    position = first - difference
    while antinode_within_bounds(position, max_x, max_y):
        yield position
        position -= difference
    position = second + difference
    while antinode_within_bounds(position, max_x, max_y):
        yield position
        position += difference

def antinode_within_bounds(antinode: complex, max_x: int, max_y: int) -> bool:
    if not (1 <= antinode.real <= max_x):
        return False
    if not (1 <= antinode.imag <= max_y):
        return False
    return True


def map_antinodes(antennas: dict[str, set[complex]], antinodes: Callable, max_x: int, max_y: int) -> int:
    antinode_locations:set[complex] = set()
    for _,positions in antennas.items():
        #print(frequency,positions)
        for pair in combinations(positions,2):
            #print(frequency,pair)
            for antinode in antinodes(*pair):
                if antinode_within_bounds(antinode, max_x, max_y):
                    antinode_locations.add(antinode)
#print(antinode_locations)
    return len(antinode_locations)

print(f"Part1: {map_antinodes(antennas, antinodes_part1, max_x, max_y)}")
print(f"Part2: {map_antinodes(antennas, antinodes_part2, max_x, max_y)}")
