use lazy_static::lazy_static;
use regex::Regex;

lazy_static! {
    static ref VAR_NAMES: Vec<&'static str> = vec![
        "gg", "rizz", "taco", "bell", "uber", "deez", "nuts", "jugz", "hell", "gyros", "fries",
        "towlie", "things",
    ];
    static ref TABLE_REGEX: Regex = Regex::new(r"(\{([^{}]+)\})").unwrap();
    static ref VAR_REGEX: Regex = Regex::new(r"(((local(\s+)?)?(=\w?)(\w+)))").unwrap();
    static ref FUNC_REGEX: Regex = Regex::new(r"(function\s*\(((\w+(,(\s?))?)*)\))").unwrap();
}

pub fn de_obfuscate_char() -> Vec<char> {
    todo!()
}

pub fn de_obfuscate(
    infected: Vec<(usize, String, Vec<String>)>,
) -> Vec<(usize, String, Vec<String>)> {
    for (ln, line, trigger) in infected.iter() {
        println!("{ln}");
    }

    infected
}
