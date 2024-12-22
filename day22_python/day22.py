#!/bin/env python3.12
from functools import cache
from typing import Generator,Any

@cache
def mix(secret_number:int, value:int) -> int:
    return secret_number ^ value

@cache
def prune(secret_number:int) -> int:
    return secret_number % 16777216

@cache
def evolve_secret_number(secret_number: int) -> int:
    secret_number = prune(mix(secret_number, secret_number * 64))
    secret_number = prune(mix(secret_number, secret_number // 32))
    secret_number = prune(mix(secret_number, secret_number * 2048))
    return secret_number

def evolve(secret_number: int, iterations: int) -> tuple[int, list[tuple[int,int]]]:
    price_change:list[tuple[int,int]] = []
    for _ in range(iterations):
        previous_number = secret_number % 10
        secret_number = evolve_secret_number(secret_number)
        price_change.append((secret_number % 10, (secret_number % 10 ) - previous_number))
    return secret_number, price_change

def calculate_patterns(price_change: list[tuple[int,int]]) -> Generator[tuple[int, tuple[int,int,int,int]],None, Any]:
    patterns:dict[int, set[tuple[int, int, int,int]]] = {}
    for position,number in enumerate(price_change[3:],start=4):
        if number[0] not in patterns:
            patterns[number[0]] = set()

        pattern:tuple[int,int,int,int] = tuple([change for _,change in price_change[position-4:position]])
        for value,pattern_set in patterns.items():
            if set([pattern]).issubset(pattern_set):
                break
        else:
            yield number[0], pattern
            patterns[number[0]].add(pattern)

sum_of_results = 0
scores:dict[tuple[int,int,int,int], int] = {}
price_patterns:dict[int,dict[int,set[tuple[int,int,int,int]]]] = {}
with open("test2.txt") as file:
    for initial_seed in file:
        secret_number = int(initial_seed.strip())
        evolved = evolve(secret_number, 2000)
        for score,pattern in calculate_patterns(evolved[1]):
            if pattern not in scores:
                scores[pattern] = score
            else:
                scores[pattern] += score
        sum_of_results += evolved[0]

print(f"Part1: {sum_of_results}")
print(f"Part2: {max(scores.values())}")
