use std::{collections::HashSet, fs};

#[derive(Debug)]
struct Backpack {
    compartment1: String,
    compartment2: String,
    total: String,
}

impl Backpack {
    fn char_score(c: &char) -> u32 {
        let code = c.clone() as u32;
        return match c {
            'a'..='z' => code - 96,
            'A'..='Z' => code - 38,
            _ => 0,
        };
    }
}

trait Intersection {
    fn intersection(&self, str2: &String) -> Vec<char>;
}
impl Intersection for String {
    fn intersection(&self, str2: &String) -> Vec<char> {
        let set: HashSet<char> = self.chars().collect();
        return str2.chars().filter(|c| set.contains(&c)).collect();
    }
}

fn parse_input(text_input: &str) -> Vec<Backpack> {
    text_input
        .split("\n")
        .map(|line| {
            let compartments = line.split_at(line.len() / 2);
            return Backpack {
                compartment1: compartments.0.to_string(),
                compartment2: compartments.1.to_string(),
                total: line.to_string(),
            };
        })
        .collect()
}

fn main() {
    let txt = fs::read_to_string("./data/3.input").unwrap();
    let backpacks = parse_input(&txt);
    let part1: u32 = backpacks
        .iter()
        .map(|backpack| {
            backpack
                .compartment1
                .intersection(&backpack.compartment2)
                .first()
                .copied()
                .unwrap()
        })
        .map(|c| Backpack::char_score(&c))
        .sum();
    let part2: u32 = backpacks
        .chunks(3)
        .map(|elfs_group| {
            let first_intersection: String = elfs_group[0]
                .total
                .intersection(&elfs_group[1].total)
                .into_iter()
                .collect();
            return first_intersection
                .intersection(&elfs_group[2].total)
                .first()
                .copied()
                .unwrap();
        })
        .map(|c| Backpack::char_score(&c))
        .sum();

    println!("part 1: {}", part1);
    println!("part 2: {}", part2);
}
