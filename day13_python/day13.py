#!/bin/env python3.12

def resolve_with_cramer(button_a:tuple[int,int], button_b:tuple[int,int], goal:tuple[int,int], offset:int=0) -> tuple[int,int]|None:
    a=button_a[0]
    b=button_b[0]
    c=button_a[1]
    d=button_b[1]
    goal = (goal[0]+offset, goal[1]+offset)
    e=goal[0]
    f=goal[1]
    denominator = (a*d - b*c)
    if denominator  == 0:
        return None
    steps_a=((e*d)-(b*f)) // denominator
    steps_b=((a*f)-(e*c)) // denominator

    x_result = (button_a[0] * steps_a) + (button_b[0] * steps_b)
    y_result = (button_a[1] * steps_a) + (button_b[1] * steps_b)
    if x_result != goal[0] or y_result != goal[1]:
        return None
    return (steps_a, steps_b)


tokens_part1 = 0
tokens_part2 = 0
with open("test.txt") as f:
    button_a = (0,0)
    button_b = (0,0)
    goal = (0,0)
    for line in f:
        match line.partition(":"):
            case "Button A",_,value:
                coordinates = value.split(",")
                x = int(coordinates[0][2:])
                y = int(coordinates[1][2:])
                button_a = (x, y)
            case "Button B",_,value:
                coordinates = value.split(",")
                x = int(coordinates[0][2:])
                y = int(coordinates[1][2:])
                button_b = (x, y)
            case "Prize",_,value:
                coordinates = value.split(",")
                x = int(coordinates[0].strip()[2:])
                y = int(coordinates[1].strip()[2:])
                goal = (x, y)
                if (part1 := resolve_with_cramer(button_a, button_b,goal, 0)) is not None:
                    tokens_part1 += (part1[0]*3 + part1[1])
                if (part2 := resolve_with_cramer(button_a, button_b,goal, 10000000000000)) is not None:
                    tokens_part2 += (part2[0]*3 + part2[1])

print(f"{tokens_part1=} {tokens_part2=}")
