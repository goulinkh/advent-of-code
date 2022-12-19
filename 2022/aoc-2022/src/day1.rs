use std::fs;

fn parse_input(text_input: &str) -> Vec<Vec<i32>> {
    return text_input
        .split("\n\n")
        .map(|lines| {
            lines.split('\n').fold(vec![], |mut items, line| {
                items.push(line.parse::<i32>().unwrap());
                return items;
            })
        })
        .collect();
}

fn main() {
    let txt = fs::read_to_string("./data/1.input").unwrap();
    let mut elfs = parse_input(&txt)
        .iter()
        .enumerate()
        .map(|(i, items)| (i, items.iter().sum::<i32>()))
        .collect::<Vec<(usize, i32)>>();
    elfs.sort_by_key(|elf| elf.1);
    elfs.reverse();
    println!("part 1: {}", elfs.first().unwrap().1);
    println!("part 2: {}", elfs[..3].iter().map(|e| e.1).sum::<i32>())
}
