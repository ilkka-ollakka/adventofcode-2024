#!/bin/env python3.12

from functools import cache
from collections import Counter


@cache
def blink(number: int)-> list[int]:
    if number == 0:
        return [1]
    elif len(str(number)) % 2 == 0:
        number_to_split=str(number)
        point_of_split = len(number_to_split)//2
        number1, number2 = number_to_split[:point_of_split], number_to_split[point_of_split:]
        return [int(number1), int(number2)]
    return [number * 2024]

# We don't need to keep track of seed order, only amount of numbers and what numbers there is
# so we use Counter, so we don't need to check numbers multiple time and cache better
def do_rounds(seed: Counter, rounds: int) -> int:
    for _ in range(rounds):
        new_seed = Counter()
        for number, amount in seed.items():
            for result in blink(number):
                # Counter update so we don't duplicate list blink returns
                new_seed.update(Counter({result: amount}))
        seed = new_seed
    return seed.total()

seed = Counter()
with open("test.txt") as f:
    for line in f:
        seed.update(map(int, line.strip().split()))

print(seed)

print(f"part1: length: {do_rounds(seed, 25)}")
print(f"part2: length: {do_rounds(seed, 75)}")

