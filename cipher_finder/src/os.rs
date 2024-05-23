use core::panic;
use std::{
    collections::HashSet,
    fs,
    path::{self, PathBuf},
    str::FromStr,
};

use regex::Regex;

/// Gets all files in subdirectories
pub fn get_all_files(path: String, exclude: Option<HashSet<String>>) -> Vec<PathBuf> {
    let mut ret = Vec::new();

    walk_dir(path, &mut |e| ret.push(e));

    println!("{:?} ex", exclude);
    // Filters
    if exclude.is_some() && !exclude.as_ref().unwrap().is_empty() {
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

/********************************************************************************
 *   FILE UTILS, DON'T HAVE TO BE PUBLIC, SO WE PUT THEM HERE AND NOT IN UTILS  *
 ********************************************************************************/

/// Filters a Vector with an Regex
fn filter_vec(haystack: Vec<PathBuf>, needles: Regex) -> Vec<PathBuf> {
    haystack
        .into_iter()
        .filter(|buf| !needles.is_match(buf.to_str().unwrap()))
        .collect::<Vec<PathBuf>>()
}

/// Walks through the given directory
fn walk_dir(path: String, cb: &mut impl FnMut(path::PathBuf)) {
    let f = match fs::read_dir(&path) {
        Err(e) => {
            println!("Can't open {} {}", path, e.kind());
            return;
        }
        Ok(v) => {
            println!("{v:?}");
            v
        }
    };

    for i in f {
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
