#!/bin/env python3.12
import time

robots = []

area=(101, 103)
with open("day14_input.txt") as f:
    for robot_line in f:
        position,direction = robot_line.strip().split()
        position = position[2:]
        x,y = map(int,position.split(","))

        direction = direction[2:]
        delta_x,delta_y = map(int,direction.split(","))
        robots.append((x,y,delta_x,delta_y))

def check_positions(robots:list[tuple[int, int, int, int]], rounds: int, area: tuple[int, int]) -> list[tuple[int, int]]:
    result = []
    for robot in robots:
        x,y,delta_x,delta_y = robot
        x += delta_x * rounds
        y += delta_y * rounds
        result.append((x% area[0],y % area[1]))
    return result

def calculate_safety_factor(robots: list[tuple[int, int]], area: tuple[int, int]) -> int:
    safety_factor = 1
    midpoint = (area[0]//2, area[1]//2)
    safety_factor *= len([robot for robot in robots if robot[0] < midpoint[0] and robot[1] < midpoint[1]])
    safety_factor *= len([robot for robot in robots if robot[0] > midpoint[0] and robot[1] < midpoint[1]])
    safety_factor *= len([robot for robot in robots if robot[0] > midpoint[0] and robot[1] > midpoint[1]])
    safety_factor *= len([robot for robot in robots if robot[0] < midpoint[0] and robot[1] > midpoint[1]])
    return safety_factor

def check_safety_balance(output: list[tuple[int, int]], area: tuple[int, int],round: int) -> bool:
    offset=2
    robot_points= set(output)
    for robot in robot_points:
        x,y = robot

        robot_filled = True
        for x_point in range(x-offset, x+offset+1):
            for y_point in range(y-offset, y+offset+1):
                if (x_point, y_point) not in robot_points:
                    robot_filled = False
                    break
            if not robot_filled:
                break
        if not robot_filled:
            continue
        draw_area(output, area)
        print(f"Easter egg found in {round=}")
        return True
    return False

def draw_area(robots: list[tuple[int, int]], area: tuple[int, int]) -> None:

    for line in range(area[0]):
        for point in range(area[1]):
            print("X" if (line, point) in robots else ".",end="")
        print("")


output = check_positions(robots, 100, area)
safety_factor = calculate_safety_factor(output, area)
print(f"Part1: {safety_factor}")

for round in range(10000000):
    output = check_positions(robots, round, area)
    if check_safety_balance(output, area, round):
        break

