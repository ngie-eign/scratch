fn main() {
    let mut i = -1;

    // A "loop" loop.
    loop {
        i += 1;
        match i {
            0 => { println!("They tried to make me go to rehab... but I said..."); },
            1..=3 => { println!("\"No..\"."); },
            _ => { break; }
        }
    }

    // A "while" loop.
    i = 0;

    while i <= 3 {
        println!("🎵I'll be... here a while... ain't goin' nowhere!🎵");
        i += 1;
    }

    // A exclusive range for loop.
    for _j in 0..1 {
        println!("For-loop and seven instructions ago!");
    }

    // A inclusive for loop.
    for _j in 0..=0 {
        println!("One more time!");
    }
    println!("🎉🎉🎉 We're gonna celebrate 🎉🎉🎉!");

    let hbfs_lyrics = [
        "WORK--IT",
        "MAKE--IT",
        "DO--IT",
        "MAKES--US",
    ];

    for line in &hbfs_lyrics {
        println!("{}", line);
    }

    for _ in 1..=8 {
        println!("dun... DUN");
    }

    let hbfs_lyrics = [
        "HARDER",
        "BETTER",
        "FASTER",
        "STRONGER"
    ];

    for line in hbfs_lyrics.iter() {
        println!("{}", line);
    }
}
