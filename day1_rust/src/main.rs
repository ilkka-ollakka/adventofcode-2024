use std::collections::HashMap;
use std::fs::File;
use std::io;
use std::io::BufRead;
use std::io::BufReader;

fn read_input(filename: &str) -> Result<Vec<Vec<i32>>, io::Error> {
    let file = BufReader::new(File::open(filename).expect("Cannot open file"));
    let mut first_numbers: Vec<i32> = Vec::new();
    let mut second_numbers: Vec<i32> = Vec::new();

    file.lines().map_while(Result::ok).for_each(|string| {
        string
            .split_whitespace()
            .map(|number| number.parse::<i32>().unwrap())
            .collect::<Vec<i32>>()
            .chunks(2)
            .for_each(|pair| {
                first_numbers.push(pair[0]);
                second_numbers.push(pair[1]);
            });
    });
    first_numbers.sort();
    second_numbers.sort();
    Ok([first_numbers, second_numbers].to_vec())
}

fn day1_part1(number_pairs: &[Vec<i32>]) -> u32 {
    let sum = number_pairs[0]
        .iter()
        .zip(number_pairs[1].iter())
        .map(|pair| (pair.0 - pair.1).unsigned_abs())
        .sum();
    sum
}

fn day1_part2(numbers: &[Vec<i32>]) -> i32 {
    /* We build hashmap of second list numbers, so we don't need to search it constantly
    and run-time is O(n) instead of O(n^2) */
    let mut score_map: HashMap<i32, i32> = HashMap::new();
    numbers[1].iter().for_each(|number| {
        *score_map.entry(*number).or_insert(0) += 1;
    });

    let impact_score: i32 = numbers[0]
        .iter()
        .map(|number| *score_map.get(number).unwrap_or(&0) * number)
        .sum();

    impact_score
}

fn main() {
    let filename = "test.txt";
    let number_pairs = read_input(filename).unwrap();
    let part1_result = day1_part1(&number_pairs);
    let part2_result = day1_part2(&number_pairs);
    println!("Part 1: {}", part1_result);
    println!("Part 2: {}", part2_result);
}
