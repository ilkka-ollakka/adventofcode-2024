#!/bin/env python3.12
from typing import Any,Generator,Literal
import time

walls: set[complex] = set()
barrel_data = tuple[complex,Literal["[","]"]]
barrels: set[barrel_data] = set()
directions: list[complex] = []
position: complex = complex(0,0)

max_x=0
max_y=0
with open("test3.txt") as f:
    for rownumber,row in enumerate(f):
        match row[0]:
            case "#":
                for columnnumber,column in enumerate(row.strip()):
                    max_y=rownumber
                    max_x=columnnumber*2+1
                    match column:
                        case "#":
                            walls.add(complex(columnnumber*2,rownumber))
                            walls.add(complex(columnnumber*2+1,rownumber))
                        case "O":
                            barrels.add((complex(columnnumber*2,rownumber),"["))
                            barrels.add((complex(columnnumber*2+1,rownumber),"]"))
                        case "@":
                            position = complex(columnnumber*2, rownumber)
            case "^"|"<"|">"|"v":
                for directionsignal in row.strip():
                    match directionsignal:
                        case "^":
                            directions.append(complex(0,-1))
                        case "v":
                            directions.append(complex(0,1))
                        case "<":
                            directions.append(complex(-1,0))
                        case ">":
                            directions.append(complex(1,0))
                        case _:
                            print(f"unknown mark '{directionsignal}'")
            case _:
                continue

def check_barrels(position: complex, barrels:set[barrel_data]) -> Generator[barrel_data, None, Any]:
    if (position,"[") in barrels:
        yield (position,"[")
    if (position,"]") in barrels:
        yield (position+complex(-1,0),"[")

def check_barrel_move(position:complex, direction: complex, barrels:set[barrel_data], walls:set[complex])->bool:
    if position+direction in walls:
        return False

    for barrel in check_barrels(position+direction, barrels):
        if check_barrel_move(barrel[0], direction, barrels, walls) is False:
            return False
    return True

def move_to(position:complex, direction:complex, walls: set[complex], barrels:set[barrel_data])->complex:
    if position + direction in walls:
        return position

    old_barres = barrels.copy()
    for barrel in check_barrels(position+direction,barrels):
        barrel_start = barrel
        barrel_end = (barrel[0]+complex(1,0),"]")
        barrels.remove(barrel_start)
        barrels.remove(barrel_end)
        new_barrel_start_position = move_to(barrel_start[0], direction, walls, barrels)
        if new_barrel_start_position == barrel_start[0]:
            barrels.clear()
            barrels.update(old_barres)
            return position
        new_barrel_end_position = move_to(barrel_end[0], direction, walls, barrels)
        if new_barrel_end_position == barrel_end[0]:
            barrels.clear()
            barrels.update(old_barres)
            return position
        if new_barrel_start_position.imag == new_barrel_end_position.imag:
            barrels.add((new_barrel_start_position,"["))
            barrels.add((new_barrel_end_position,"]"))
        else:
            barrels.clear()
            barrels.update(old_barres)
            return position

    return position + direction

def calculate_barrel_score(barrels: set[barrel_data])->int:
    score = 0
    for barrel in barrels:
        if barrel[1] == "[":
            score += int(barrel[0].real) + int(barrel[0].imag)*100
    return score

def draw_map(walls: set[complex], barrels: set[barrel_data], position: complex):
    print("\033[2J")
    print("\033[H")
    for y in range(max_y+1):
        for x in range(max_x+1):
            if complex(x,y) in walls:
                print("#",end="")
            elif (complex(x,y),"[") in barrels:
                print("[",end="")
            elif (complex(x,y),"]") in barrels:
                print("]",end="")
            elif complex(x,y) == position:
                print("@",end="")
            else:
                print(".",end="")
        print()

draw_map(walls, barrels, position)
print(f"Starting moving, barrel_amount={len(barrels)}, move count={len(directions)}")

for direction in directions:
    time.sleep(.01)
    new_position = move_to(position, direction, walls, barrels)
    position = new_position
    draw_map(walls, barrels, position)

print(f"final GPS score: {calculate_barrel_score(barrels)} barrel_amount={len(barrels)}, moves={len(directions)}")



