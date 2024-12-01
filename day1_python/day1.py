#!/bin/env python3.12
from collections import Counter

numbers: list[list[int]] = [[],[]]

def part1(numbers: list[list[int]]) -> int:
    #print(numbers)
    total_distance = 0
    for pair in zip(numbers[0], numbers[1]):
        #print(pair[0], pair[1], abs(pair[0] - pair[1]))
        total_distance += abs(pair[0] - pair[1])
    return total_distance

def part2(numbers: list[list[int]]) -> int:
    toka_lista_esiintyvyys = Counter(numbers[1])
    #print(toka_lista_esiintyvyys)
    total_similarity = 0
    for value_to_check in numbers[0]:
        total_similarity += (toka_lista_esiintyvyys.get(value_to_check,0) * value_to_check)
    return total_similarity

with open('test.txt') as file_input:
    for line in file_input:
        eka, toka, *_ = line.split()
        numbers[0].append(int(eka))
        numbers[1].append(int(toka))
numbers[0].sort()
numbers[1].sort()
print(f"part1: {part1(numbers)}")
print(f"part2: {part2(numbers)}")
