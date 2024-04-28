use std::{path, vec};

use lazy_static::lazy_static;
use regex::Regex;

lazy_static! {
    pub static ref CIPHER_REGEX: Regex = Regex::new(r"(((\\[xu])([a-fA-F0-9]{2}))+)").unwrap();
    pub static ref SIMPLE_URL_REGEX: Regex = Regex::new(r"https?://(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)").unwrap();
}

/// increases or decreases the confidence if the regex finds something or not.
pub fn check_regex(regex: &Regex, haystack: &str) -> bool {
    for found in regex.captures_iter(haystack) {
        println!("{found:?}")
    }
    false
}

/// just a shortcut to split a string for further usage
pub fn format_dir_str(s: String) -> Vec<String> {
    if s.is_empty() {
        // handle default
        return vec![];
    }
    let ret = vec![];

    for i in s.split(",").into_iter() {}

    ret
}

/// Filter the walk_dir list for viable files like .lua etc.
pub fn filter_viables(haystack: Vec<path::PathBuf>) -> Vec<path::PathBuf> {
    haystack
        .into_iter()
        .filter(|i| i.extension().unwrap_or_default() == "lua")
        .collect::<Vec<path::PathBuf>>()
}

/// find all .gitignore files in location system
pub fn find_gitignores(haystack: Vec<path::PathBuf>) -> Vec<path::PathBuf> {
    haystack
        .into_iter()
        .filter(|i| i.file_name().unwrap_or_default() == ".gitignore")
        .collect::<Vec<path::PathBuf>>()
}

pub fn load_gitignores(stack: Vec<path::PathBuf>) {}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_format_dir_str() {
        let tests = vec![
            (
                String::from("some,cool,string"),
                vec!["some".to_string(), "cool".to_string(), "string".to_string()],
            ),
            (String::from("some"), vec!["some".to_string()]),
            (String::from(""), vec![]),
        ];

        for (s, t) in tests {
            assert!(format_dir_str(s) == t);
        }
    }
}
