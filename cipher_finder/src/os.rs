use std::{
    fs::{self},
    path::{self, PathBuf},
    str::FromStr,
};

use regex::Regex;

/// Gets all files in subdirectories
pub fn get_all_files(path: String, exclude: Option<Vec<String>>) -> Vec<PathBuf> {
    let mut ret = Vec::new();

    walk_dir(path, &mut |e| ret.push(e));

    if exclude.is_some() {
        let s = exclude
            .unwrap()
            .iter()
            .map(|s| "(".to_owned() + s.as_str() + ")")
            .collect::<Vec<String>>()
            .join("|");

        let needle: Regex = match Regex::from_str(&s) {
            Ok(r) => r,
            Err(_) => panic!("BuFu"),
        };

        ret = filter_vec(ret, needle);
    }

    ret
}

/// Filters a Vector with an Regex
fn filter_vec(haystack: Vec<PathBuf>, needles: Regex) -> Vec<PathBuf> {
    haystack
        .into_iter()
        .filter(|buf| !needles.is_match(&buf.to_str().unwrap().to_string()))
        .collect::<Vec<PathBuf>>()
}

/// Walks through the given directory
fn walk_dir(path: String, cb: &mut impl FnMut(path::PathBuf)) {
    for i in fs::read_dir(path).unwrap() {
        match i {
            Ok(dir) => {
                // we dont want to return here, also dont remove the else ples
                if dir.path().is_dir() {
                    walk_dir(dir.path().to_str().unwrap().to_string(), cb);
                } else {
                    cb(dir.path());
                }
            }
            Err(e) => panic!("{e}"),
        }
    }
}
