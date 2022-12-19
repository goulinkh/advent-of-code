use std::{
    fmt::{self, Debug},
    fs,
    str::FromStr,
};

use anyhow::{bail, Result};

#[derive(Debug, Clone, Copy)]
enum Move {
    Rock = 1,
    Paper = 2,
    Scissor = 3,
}
#[derive(Debug, Clone, Copy)]
enum Outcome {
    Win = 6,
    Draw = 3,
    Lose = 0,
}

impl Move {
    fn outcome(&self, e2: &Self) -> Outcome {
        match (self, e2) {
            (Move::Rock, Move::Rock) => Outcome::Draw,
            (Move::Rock, Move::Paper) => Outcome::Lose,
            (Move::Rock, Move::Scissor) => Outcome::Win,
            (Move::Paper, Move::Rock) => Outcome::Win,
            (Move::Paper, Move::Paper) => Outcome::Draw,
            (Move::Paper, Move::Scissor) => Outcome::Lose,
            (Move::Scissor, Move::Rock) => Outcome::Lose,
            (Move::Scissor, Move::Paper) => Outcome::Win,
            (Move::Scissor, Move::Scissor) => Outcome::Draw,
        }
    }
    fn score(&self, opponent: &Self) -> i32 {
        *self as i32 + self.outcome(opponent) as i32
    }
    fn to_play(&self, expected_outcome: &Outcome) -> Move {
        match (self, expected_outcome) {
            (Move::Rock, Outcome::Win) => Move::Paper,
            (Move::Rock, Outcome::Draw) => Move::Rock,
            (Move::Rock, Outcome::Lose) => Move::Scissor,
            (Move::Paper, Outcome::Win) => Move::Scissor,
            (Move::Paper, Outcome::Draw) => Move::Paper,
            (Move::Paper, Outcome::Lose) => Move::Rock,
            (Move::Scissor, Outcome::Win) => Move::Rock,
            (Move::Scissor, Outcome::Draw) => Move::Scissor,
            (Move::Scissor, Outcome::Lose) => Move::Paper,
        }
    }
}

impl FromStr for Move {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self> {
        match s {
            "A" => Ok(Move::Rock),
            "X" => Ok(Move::Rock),
            "B" => Ok(Move::Paper),
            "Y" => Ok(Move::Paper),
            "C" => Ok(Move::Scissor),
            "Z" => Ok(Move::Scissor),
            _ => bail!("Invalid move"),
        }
    }
}

impl FromStr for Outcome {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self> {
        match s {
            "X" => Ok(Outcome::Lose),
            "Y" => Ok(Outcome::Draw),
            "Z" => Ok(Outcome::Win),
            _ => bail!("Invalid outcome"),
        }
    }
}

fn parse_input<T, U>(text_input: &str) -> Vec<(T, U)>
where
    T: std::str::FromStr,
    <T as FromStr>::Err: fmt::Debug,
    U: std::str::FromStr,
    <U as FromStr>::Err: fmt::Debug,
{
    text_input
        .split('\n')
        .map(|line| {
            let (c1, c2) = line.split_once(' ').unwrap();
            return (c1.parse::<T>().unwrap(), c2.parse::<U>().unwrap());
        })
        .collect()
}

fn main() {
    let txt = fs::read_to_string("./data/2.input").unwrap();
    let part1 = parse_input::<Move, Move>(&txt);
    println!(
        "part 1: {}",
        part1
            .iter()
            .map(|round| round.1.score(&round.0))
            .sum::<i32>()
    );
    let part2 = parse_input::<Move, Outcome>(&txt);
    println!(
        "part 2: {}",
        part2
            .iter()
            .map(|round| {
                let played_move = round.0.to_play(&round.1);
                return played_move.score(&round.0);
            })
            .sum::<i32>()
    )
}
