use std::fs;

#[derive(Clone, Debug)]
struct Move((usize, usize, usize));

fn parse_input(text_input: &str) -> (Vec<Vec<char>>, Vec<Move>) {
    let (crates_txt, moves_txt) = text_input.split_once("\n\n").unwrap();
    let mut crate_lines: Vec<String> = crates_txt.split('\n').map(|l| l.to_string()).collect();
    crate_lines.pop();
    let number_of_crates = (crate_lines[0].len() + 1) / 4;
    let mut crates = vec![vec![]; number_of_crates];
    crate_lines.iter().for_each(|line| {
        line.chars()
            .collect::<Vec<char>>()
            .chunks(4)
            .enumerate()
            .for_each(|(i, word)| match word.iter().collect::<String>().as_str() {
                "    " | "   " => {}
                _ => crates[i].push(word[1]),
            })
    });

    crates.iter_mut().for_each(|c: &mut Vec<char>| c.reverse());

    let move_lines = moves_txt
        .split('\n')
        .map(|l| l.to_string())
        .collect::<Vec<String>>();
    let mut moves: Vec<Move> = vec![];
    move_lines.iter().for_each(|line| {
        let words = line
            .split_whitespace()
            .filter_map(|word| word.parse::<usize>().ok())
            .collect::<Vec<usize>>();
        moves.push(Move((words[0], words[1], words[2])));
    });
    return (crates, moves);
}

fn move_crates(m: &Move, crates: &mut Vec<Vec<char>>) {
    let (quantity, mut source, mut target) = m.0;
    source -= 1;
    target -= 1;
    for _ in 0..quantity {
        let value = crates[source].pop().unwrap();
        crates[target].push(value);
    }
}

fn reverse_move_crates(m: &Move, crates: &mut Vec<Vec<char>>) {
    let (quantity, mut source, mut target) = m.0;
    source -= 1;
    target -= 1;
    let len = crates[source].len();
    let c = crates[source]
        .splice(len - quantity..len, [])
        .collect::<Vec<char>>();
    crates[target].extend(c);
}

fn main() {
    let txt = fs::read_to_string("./data/5.input").unwrap();
    let mut part1 = parse_input(&txt);
    part1.1.iter().for_each(|m| move_crates(m, &mut part1.0));
    let mut part2 = parse_input(&txt);
    part2
        .1
        .iter()
        .for_each(|m| reverse_move_crates(m, &mut part2.0));
    println!(
        "part 1: {}",
        part1
            .0
            .iter()
            .map(|c| c.last().unwrap())
            .collect::<String>(),
    );
    println!(
        "part 1: {}",
        part2
            .0
            .iter()
            .map(|c| c.last().unwrap())
            .collect::<String>()
    );
}
