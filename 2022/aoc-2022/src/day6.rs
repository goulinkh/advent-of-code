use std::collections::HashSet;
use std::fs;

fn distinct_packets(message: &String, length: usize) -> usize {
    message
        .chars()
        .collect::<Vec<char>>()
        .windows(length)
        .position(|sequence| sequence.len() == HashSet::<&char>::from_iter(sequence).len())
        .unwrap()
        + length
}

fn main() {
    let txt = fs::read_to_string("./data/6.input").unwrap();
    println!("part 1: {}", distinct_packets(&txt, 4));
    println!("part 2: {}", distinct_packets(&txt, 14));
}
