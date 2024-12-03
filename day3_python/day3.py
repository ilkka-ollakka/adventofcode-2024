import re

corrupted_memory = None
with open('test2.txt') as f:
    corrupted_memory = f.read().strip('\n')


def part1(corrupted_memory):
    match = re.compile(r'mul\((\d+),(\d+)\)')
    result = match.findall(corrupted_memory)
    return sum([int(value[0]) * int(value[1]) for value in result])

def part2(corrupted_memory):
    tokenizer = re.compile(r'(do\(\)|^)(.*?)(don\'t\(\)|$)', flags=re.DOTALL)
    end_result = 0
    for token_value in tokenizer.finditer(corrupted_memory):
        sum_of_value = part1(token_value.groups()[1])
        #print(f"match : {token_value.groups()} {sum_of_value=}")
        end_result += sum_of_value
    return end_result

print(f"part1: {part1(corrupted_memory)}")
print(f"part2: {part2(corrupted_memory)}")
