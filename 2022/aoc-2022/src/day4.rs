use std::fs;

struct Group(u32, u32);

fn parse_input(text_input: &str) -> Vec<(Group, Group)> {
    return text_input
        .split('\n')
        .map(|line| {
            let (group1, group2) = line.split_once(',').unwrap();
            let (g1_left, g1_right) = group1.split_once('-').unwrap();
            let (g2_left, g2_right) = group2.split_once('-').unwrap();
            let g1 = Group(
                g1_left.parse::<u32>().unwrap(),
                g1_right.parse::<u32>().unwrap(),
            );
            let g2 = Group(
                g2_left.parse::<u32>().unwrap(),
                g2_right.parse::<u32>().unwrap(),
            );
            return (g1, g2);
        })
        .collect::<Vec<(Group, Group)>>();
}

fn includes(group1: &Group, group2: &Group) -> bool {
    return (group1.0 <= group2.0 && group1.1 >= group2.1)
        || (group2.0 <= group1.0 && group2.1 >= group1.1);
}
fn overlap(group1: &Group, group2: &Group) -> bool {
    return (group1.0 <= group2.1 && group1.0 >= group2.0)
        || (group2.0 <= group1.1 && group2.0 >= group1.0);
}

fn main() {
    let txt = fs::read_to_string("./data/4.input").unwrap();
    let part1 = parse_input(&txt)
        .iter()
        .filter(|(g1, g2)| includes(g1, g2))
        .collect::<Vec<&(Group, Group)>>()
        .len();
    let part2 = parse_input(&txt)
        .iter()
        .filter(|(g1, g2)| overlap(g1, g2))
        .collect::<Vec<&(Group, Group)>>()
        .len();
    println!("part 1: {}", part1);
    println!("part 2: {}", part2);
}
