#!/bin/env python3.12
from functools import cmp_to_key


ordering:dict[int, list[int]] = {}

page_orders: list[list[int]] = []

def sorting_comparator(a: int, other:int ) -> int:
    if a in ordering:
        if other in ordering[a]:
            return -1
    return 0

with open("test.txt") as f:
    parsed_code = False
    for line in f:
        line = line.strip()
        if not line:
            parsed_code = True
            continue
        if parsed_code:
            page_orders.append(list(map(int, line.split(','))))
            continue
        parts = line.split("|")
        parent = int(parts[0])
        if parent not in ordering:
            ordering[parent] = []
        ordering[parent].append(int(parts[1]))

mid_sum = 0
part2_sum = 0
for line in page_orders:
    line_copy = line.copy()
    line_copy.sort(key=cmp_to_key(sorting_comparator))
    print(line, line_copy)
    if line_copy == line:
        mid_sum += line[int(len(line)/2)]
    else:
        part2_sum += line_copy[int(len(line_copy)/2)]
print(f"Part1: {mid_sum=}")
print(f"Part2: {part2_sum=}")
