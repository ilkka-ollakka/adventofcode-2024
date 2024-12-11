#!/bin/env python3.12
from typing import Generator

topology_map:list[list[int]] = []
max_x=0
max_y=0

with open("test.txt") as file:
    topology_map = [list(map(int, list(line.strip()))) for line in file]

starting_points: set[tuple[int, int]] = set()

for y, row in enumerate(topology_map):
    max_y=y
    max_x=len(row)
    for x, value in enumerate(row):
        if value == 0:
            starting_points.add((x, y))

def get_valid_moves(topology_map: list[list[int]], point: tuple[int, int]) -> Generator[tuple[int, int], None, None]:
    current_x, current_y = point
    current_value = topology_map[current_y][current_x]
    for offsets in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_x = current_x + offsets[0]
        new_y = current_y + offsets[1]
        if 0 <= new_x < max_x and 0 <= new_y <= max_y:
            new_value = topology_map[new_y][new_x]
            if new_value-current_value == 1:
                yield (new_x, new_y)


def find_trails(topology_map: list[list[int]], starting_points: set[tuple[int, int]], skip_visited_points:bool) -> int:
    trailling_heads = 0
    for point in starting_points:
        visited_points: set[tuple[int, int]] = set()
        points_to_check = list(get_valid_moves(topology_map, point))
        while points_to_check:
            current_point = points_to_check.pop(0)
            if skip_visited_points and current_point in visited_points:
                continue
            visited_points.add(current_point)
            if topology_map[current_point[1]][current_point[0]] == 9:
                trailling_heads += 1
                #print(f"Found a trail fron {point} to {current_point}")
                continue
            points_to_check.extend(list(get_valid_moves(topology_map, current_point)))
        #print(f"Visited {len(visited_points)} points, found {trailling_heads-current_trails} trails from starting point {point}")
    return trailling_heads

print(f"Part1: {find_trails(topology_map, starting_points, True)}")
print(f"Part2: {find_trails(topology_map, starting_points, False)}")
