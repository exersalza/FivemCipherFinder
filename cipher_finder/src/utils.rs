use std::{collections::HashSet, fs::OpenOptions, io::Read, path, sync::Mutex, usize, vec};

use lazy_static::lazy_static;
use regex::Regex;

lazy_static! {
    pub static ref CIPHER_REGEX: Regex = Regex::new(r"(((\\[xu])([a-fA-F0-9]{2}))+)").unwrap();
    pub static ref SIMPLE_URL_REGEX: Regex = Regex::new(r"https?://(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)").unwrap();
    static ref TRANSLATE_LIST: Vec<(String, String)> = Vec::from_iter([
        (".".to_string(), "\\.".to_string()),
        ("[".to_string(), "\\[".to_string()),
        ("]".to_string(), "\\]".to_string()),
        ("(".to_string(), "\\(".to_string()),
        (")".to_string(), "\\)".to_string()),
        ("*".to_string(), ".*".to_string()),
    ]);
    pub static ref SCAN_LEVEL: Mutex<ScanLevel> = Mutex::new(ScanLevel::Standard);
}

/// Defines the Scanlevel
/// Standard -> Uses the default regexes -> URL, HexCode
/// Aggressive -> Uses more regexes, but yields more false positives -> Lua IO Operations
#[derive(clap::ValueEnum, Debug, Clone)]
pub enum ScanLevel {
    /// Standard scan
    Standard,
    Aggressive,
}

/// checks a regex
pub fn check_regex(regex: &Regex, haystack: &str) -> Vec<String> {
    regex
        .captures_iter(haystack)
        .filter_map(|found| found.get(0).map(|j| j.as_str().to_string()))
        .collect()
}

/// just a shortcut to split a string for further usage
pub fn format_dir_str(s: String) -> HashSet<String> {
    if s.is_empty() {
        // handle default
        return HashSet::new();
    }

    s.split(',')
        .into_iter()
        .map(|i| prepare_for_regex(i.to_string()))
        .collect()
}

/// Filter the walk_dir list for viable files like "lua" etc.
///
/// Scans the PathBuf vector for the needle, the needle doesn't have to have a [dot] infront of it.
pub fn filter_viables(haystack: Vec<path::PathBuf>, needle: &str) -> Vec<path::PathBuf> {
    haystack
        .into_iter()
        .filter(|i| {
            // rust things
            let f = i
                .file_name()
                .unwrap_or_default()
                .to_str()
                .unwrap_or_default();
            f.split('.').last().unwrap_or_default() == needle
        })
        .collect()
}

/// Get the contents of gitignore files based on the input vector
pub fn parse_gitignores(stack: Vec<path::PathBuf>) -> HashSet<String> {
    let mut ret = vec![];

    for path in stack {
        let mut file = match OpenOptions::new().read(true).open(path) {
            Ok(f) => f,
            Err(e) => panic!(
                "Panicked while trying to open gitignore file with error: {}",
                e
            ),
        };

        let mut buf = vec![];
        let _ = file.read_to_end(&mut buf);

        let conts = String::from_utf8_lossy(&buf).into_owned().replace('\r', "");

        for l in conts.split('\n') {
            remove_comments(l, &mut ret);
        }
    }

    HashSet::from_iter(ret)
}

/// filters comments from a .gitignore line, also prepares the line
/// for use in regex
fn remove_comments(line: &str, target: &mut Vec<String>) {
    let comment_ind = match line.find('#') {
        Some(v) => v,
        None => usize::max_value(),
    };
    let mut t = line;

    // check if found index has no \ before it
    if comment_ind != usize::max_value()
        && !(comment_ind > 0 && line.chars().nth(comment_ind - 1).unwrap() == '\\')
    {
        t = &line[..comment_ind];
    }

    // empty lines wont be used in filter
    if t.is_empty() {
        return;
    }

    target.push(prepare_for_regex(t.trim().to_string()));
}

/// Prepares a string to be used in regex
/// we want to replace stuff like "." with "\\." because in regex terms the dot is a wildcard
/// for every character, that can break search results
fn prepare_for_regex(s: String) -> String {
    let mut s = s;
    // translate list to parse characters for regex
    for (k, v) in TRANSLATE_LIST.iter() {
        s = s.replace(k, v);
    }

    s
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_format_dir_str() {
        let tests = vec![
            (
                String::from("some,cool,string"),
                HashSet::from_iter(vec![
                    "some".to_string(),
                    "cool".to_string(),
                    "string".to_string(),
                ]),
            ),
            (
                String::from("some"),
                HashSet::from_iter(vec!["some".to_string()]),
            ),
            (String::from(""), HashSet::new()),
        ];

        for (s, t) in tests {
            assert!(format_dir_str(s) == t);
        }
    }

    #[test]
    fn test_prepare_for_regex() {
        assert!(prepare_for_regex(String::from("Testing.")) == String::from("Testing\\."));
        assert!(prepare_for_regex(String::from("Testing.*")) == String::from("Testing\\..*"));
        assert!(prepare_for_regex(String::from("*Testing.*")) == String::from(".*Testing\\..*"));
        assert!(
            prepare_for_regex(String::from("*[Testing].*")) == String::from(".*\\[Testing\\]\\..*")
        );
        assert!(
            prepare_for_regex(String::from("*(Testing).*")) == String::from(".*\\(Testing\\)\\..*")
        );
    }

    #[test]
    fn test_load_gitignores() {
        let input = vec![
            "# test",
            "",
            r"\#remove_me",
            "some_dir/ # this directy has stuff in it",
        ];
        let should = vec!["\\#remove_me", "some_dir/"];
        let mut target = vec![];

        for i in input {
            remove_comments(i, &mut target);
        }

        for (i, v) in target.iter().enumerate() {
            assert!(should[i] == v)
        }
    }
}
