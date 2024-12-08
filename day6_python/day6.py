#!/bin/env python3.12

map_obstacles: set[complex] = set()
map_width = 0
map_height = 0

direction = complex(0, -1)
turn_left = complex(0, 1)
position = complex(0, 0)

with open("test.txt") as f:
    for y, line in enumerate(f):
        map_height = y
        map_width = len(line)
        for x, char in enumerate(line):
            if char == "#":
                map_obstacles.add(complex(x, y))
            if char == "^":
                position = complex(x, y)

def find_path(position: complex, direction: complex, obstacles: set[complex]) -> tuple[set[tuple[complex, complex]], tuple[complex, complex]]:
    positions_visited: set[tuple[complex, complex]] = set()
    positions_visited.add((position,direction))
    while True:
        # We need to turn until we don't face an obstacle
        while position + direction in obstacles:
            direction *= turn_left
        position += direction
        if position.real < 0 or position.real > map_width or position.imag < 0 or position.imag > map_height:
            return positions_visited, (position, direction)
        if (position, direction) in positions_visited:
            #print(f"loop found at {position} {direction} after {len(positions_visited)} steps")
            return positions_visited, (position, direction)
        positions_visited.add((position, direction))

part1,out_point = find_path(position, direction, map_obstacles)

num_options = set()
for position_to_add in set([point[0] for point in part1]):
    if position_to_add == position:
        continue
    path, out_point = find_path(position, direction, map_obstacles|set([position_to_add]))
    if out_point in path:
        num_options.add(position_to_add)
print(f"part1: {len(set([point[0] for point in part1]))}")
print(f"part2: {len(num_options)}")
