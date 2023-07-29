fn main() {
    let mut i = 0;

    // A "loop" loop.
    loop {
        if i == 0 {
            println!("They tried to make me go to rehab... but I said...");
            i += 1;
            continue;
        } else if i <= 3 {
            println!("\"No..\".");
        } else {
            break;
        }
        i += 1;
    }

    // A "while" loop.
    i = 0;

    while i <= 3 {
        println!("311: 🎵I'll be... here a while... ain't goin' nowhere!🎵");
        i += 1;
    }

    // A "for" loop.
    for _j in 0..1 {
        println!("For-loop and seven instructions ago!");
    }
}
