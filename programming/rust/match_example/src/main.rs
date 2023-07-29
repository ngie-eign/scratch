fn pick_needle(haystack: &String, needle_num: usize) -> String {
    let needle_in_haystack = haystack.chars().nth(needle_num);

    return match needle_in_haystack {
        Some(needle) => format!("Needle #{} found in haystack: '{}'", needle_num, needle),
        None => format!("Needle #{} not in the haystack!", needle_num)
    };
}

fn main() {
    let haystack: String = String::from("This is a haystack");

    let last_needle_in_haystack_s = pick_needle(&haystack, haystack.len() - 1);
    let needle_not_in_haystack_s = pick_needle(&haystack, haystack.len());

    println!("Haystack contents: \"{}\".", haystack);
    println!("{}", last_needle_in_haystack_s);
    println!("{}", needle_not_in_haystack_s);
}
