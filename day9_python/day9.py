#!/bin/env python3.12

disk_layout = []

file_layout = {}
free_layout = {}
file_id=0
with open("test2.txt") as f:
    for line in f:
        input = line.strip()
        file=True
        for sector in input:
            sector_amount = int(sector)
            position = len(disk_layout)
            for _ in range(sector_amount):
                disk_layout.append(str(file_id) if file else '.')
            if sector_amount > 0:
                if file:
                    file_layout[file_id] = {'size':sector_amount, 'position':position}
                else:
                    free_layout[position] = {'size':sector_amount}
            file = not file
            if file:
                file_id += 1


def part1(disk_layout: list[str])->int:
    while "." in disk_layout:
        position = disk_layout.index(".")
        number = disk_layout.pop()
        while number == ".":
            number = disk_layout.pop()
        if len(disk_layout) <= position:
            disk_layout.append(number)
        else:
            disk_layout[position]=number
    return calculate_checksum(disk_layout)

def part2(file_layout: dict[int, dict[str, int]], free_layout: dict[int, dict[str, int]]) -> int:
    moved_files: set[int] = set()
    for file_info in sorted(file_layout.keys(), reverse=True):
        print(f"file_id {file_info=}")
        size_to_find = None
        file_position = file_layout[file_info]['position']
        for key,free_position in sorted(free_layout.items()):
            #print(key,free_position, file_layout[file_info])
            if key > file_position:
                break
            if free_position['size'] < file_layout[file_info]['size']:
                continue
            size_to_find = free_layout[key]['size']
            #print(f"found free space {size_to_find=}")
            break
        else:
            #print(f"no free space for {file_info=} from {free_layout=}")
            continue
        if size_to_find is None:
            #print(f"no free space left of item for {file_layout[file_info]=} from {free_layout=}")
            continue
        file_size = file_layout[file_info]['size']
        new_size = size_to_find - file_size
        new_position = key+file_size
        if new_size > 0:
            free_layout[new_position] = {'size':new_size}
        del free_layout[key]
        changed_position = file_layout[file_info]['position']
        free_layout[changed_position] = {'size':file_size}
        file_layout[file_info]['position'] = key
        moved_files.add(file_info)

    #print(f"file_layout {file_layout=}")
    #print(f"moved_files {moved_files=}")
    return calculate_checksum_from_file_layout(file_layout)

def calculate_checksum_from_file_layout(file_layout: dict[int, dict[str, int]])->int:
    disk_checksum = 0
    for file_id,file_info in file_layout.items():
        for position in range(file_info['size']):
            disk_checksum += file_id*(position+file_info['position'])
    return disk_checksum

def calculate_checksum(disk_layout: list[str])->int:
    disk_checksum = 0
    for position, number in enumerate(disk_layout):
        disk_checksum += int(number)*position
    return disk_checksum

print(f"Part 1: {part1(disk_layout)}")
print(f"Part 2: {part2(file_layout, free_layout)}")
