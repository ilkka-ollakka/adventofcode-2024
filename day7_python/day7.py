#!/usr/bin env python3.12

# Recursion makes faster traveling of the tree of possibilities
# as we can rule out more branches at once that we don't need to travel
# if we end up in state that we are over the result
def check_result(current_result:int, target_value:int, values:list[int], valid_operators: list[str], operation: str) -> bool:
    if not values:
        return current_result == target_value

    if current_result > target_value:
        return False

    match operation:
        case '+':
            new_result = current_result + values[0]
        case '*':
            new_result = current_result * values[0]
        case '||':
            new_result = int(str(current_result) + str(values[0]))
        case _:
            return False

    for operator in valid_operators:
        if check_result(new_result, result_to_aim, values[1:], valid_operators, operator):
            return True

    return False

    

part1 = 0
part2 = 0
with open("day7_input.txt") as file:
    for line in file:
        result, values = line.split(":", maxsplit=1)
        result_to_aim = int(result.strip())
        values = [int(value) for value in values.strip().split()]

        valid_operators_part1 = ["*", "+"]
        valid_operators_part2 = ["*", "+", "||"]
        for operator in valid_operators_part2:
            if check_result(values[0], result_to_aim, values[1:], valid_operators_part2, operator):
                part2 += result_to_aim
                break
        for operator in valid_operators_part1:
            if check_result(values[0], result_to_aim, values[1:], valid_operators_part1, operator):
                part1 += result_to_aim
                break


print(f"{part1=} {part2=}")

