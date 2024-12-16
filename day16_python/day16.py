#!/bin/env python3.12
from typing import Generator, Any
from heapq import heappop, heappush

direction = complex(1,0)
position = complex(0,0)
walls:set[complex]=set()
goal=complex(0,0)

with open("test2.txt") as f:
    for row_number,row in enumerate(f):
        for column_number,cell in enumerate(row):
            match cell:
                case "#":
                    walls.add(complex(column_number,row_number))
                case "E":
                    goal=complex(column_number, row_number)
                case "S":
                    position=complex(column_number, row_number)


def turn_count(direction: complex, end_direction:complex, clockwise:bool)->int:
    if direction == end_direction:
        return 0
    turn = complex(0,1) if clockwise else complex(0,-1)
    count = 0
    while direction != end_direction:
        count += 1
        direction *= turn
    return count

def directions(position:complex, direction:complex)->Generator[tuple[tuple[int,int],tuple[int,int],int], None, Any]:
    for next_step in [complex(1,0), complex(-1,0), complex(0,1), complex(0,-1)]:
        score=1
        if position+next_step in walls:
            continue
        if next_step != direction:
            clock_wise = turn_count(direction, next_step, True)
            counter_clock_wise = turn_count(direction, next_step, False)
            turn_amount = min([clock_wise, counter_clock_wise])
            score += (1000*turn_amount)
        next_position = position+next_step
        yield ((int(next_position.real), int(next_position.imag)), (int(next_step.real),int(next_step.imag)), score)

positions_visited:set[tuple[int,int]] = set()
lowest_score_visited:dict[tuple[tuple[int,int],tuple[int,int]],int]={}
possibilities=[(int(0),(int(position.real),int(position.imag)),(int(direction.real),int(direction.imag)),positions_visited)]

final_points=set()
while possibilities:
    score, position,direction,positions_visited = heappop(possibilities)
    previous_score = lowest_score_visited.get((position,direction),None)
    if previous_score is not None and previous_score < score:
        continue
    lowest_score_visited[(position,direction)]=score
    if complex(*position) == goal:
        print(f"Part1 min score {score}, steps: {len(positions_visited)}")
        final_points.update(positions_visited)
        while complex(*position)==goal:
            netx_score, position,direction,positions_visited = heappop(possibilities)
            if netx_score > score:
                print(f"Part2: points: {len(final_points)+1}")
                break
            final_points.update(positions_visited)
        break
    for next_position, next_direction, next_score in directions(complex(*position), complex(*direction)):
        if next_position in positions_visited:
            continue
        heappush(possibilities, (score+next_score, next_position, next_direction, positions_visited|set([position])))
