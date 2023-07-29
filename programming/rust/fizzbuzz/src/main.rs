use std::env;
use std::process;

fn fizzbuzz(i: i64) -> String
{
    let mut result: String = String::new();

    if i <= 0 {
        return result;
    }
    if i % 3 == 0 {
        result += "fizz";
    }
    if i % 5 == 0 {
        result += "buzz";
    }
    // same as `return result;` -- WATTTTTT?
    result
}

fn usage()
{
    let exe = env::current_exe().expect("could not resolve exe path");
    let progname = exe.file_name().expect("could not resolve exe filename.");

    println!("usage: {} <value>", progname.to_string_lossy());

    process::exit(1);
}

fn main()
{
    let args: Vec<String> = env::args().collect();
    let fb_result: String;

    if args.len() != 2 {
        usage();
    }

    let arg: String = args.get(1).expect("arg 0 not specified").to_string();
    let arg_i: i64 = arg.parse().unwrap();

    if arg_i <= 0 {
        println!("error: argument must be a positive integral value!\n");
        usage();
    }
    fb_result = fizzbuzz(arg_i);

    println!("{}", fb_result);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fizzbuzz() {
        let test_tuples = [
            (3, "fizz"),
            (5, "buzz"),
            (15, "fizzbuzz"),
            (-15, ""),
        ];
        for test_tuple in test_tuples.iter() {
            assert_eq!(fizzbuzz(test_tuple.0), test_tuple.1.to_string());
        }
    }
}
