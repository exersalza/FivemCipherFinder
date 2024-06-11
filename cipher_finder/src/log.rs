use std::fmt;
use std::fs;
use std::io;
use std::io::Write;

use crate::utils::get_ext;

#[derive(Debug, PartialEq)]
pub enum Verbosity {
    None,
    Verbose,
    VeryVerbose,
}

pub struct Logging {
    mode: Verbosity,
    log: Vec<String>,
}

impl Logging {
    pub fn new(verbose: bool, very_verbose: bool) -> Self {
        let mode = match (very_verbose, verbose) {
            (true, _) => Verbosity::VeryVerbose,
            (false, true) => Verbosity::Verbose,
            (false, false) => Verbosity::None,
        };

        Self { mode, log: vec![] }
    }

    /// Appends something to the Log
    ///
    /// ## Parameters
    /// msg -> What should be appended to the Log
    pub fn append(&mut self, msg: impl fmt::Display) {
        match self.mode {
            Verbosity::None => (),
            Verbosity::Verbose => {}
            Verbosity::VeryVerbose => {}
        }

        self.log.push(msg.to_string());
    }

    /// Writes the Log to a file
    ///
    /// ## Returns
    /// Returns an Result with the written bytes on success
    pub fn write(&self) -> io::Result<usize> {
        if self.mode.eq(&Verbosity::None) {
            return Ok(0);
        }

        let id = get_last_id();
        let mut written_bytes: usize = 0;

        let mut handle = fs::OpenOptions::new()
            .write(true)
            .create(true)
            .open(format!("./CipherLog-{id}.txt"))?;

        for msg in &self.log {
            if let Ok(v) = handle.write(msg.as_bytes()) {
                written_bytes = written_bytes + v;
            } else {
            }
        }

        Ok(written_bytes)
    }
}

/// Gets the highest CipherLog id that can be found in the current directory
fn get_last_id() -> i32 {
    let mut id = 0;

    for i in fs::read_dir(".").unwrap() {
        if let Ok(j) = i {
            let p = j.path();
            let tp = p.to_str().unwrap_or("whyisliamnothere.txt");

            if !tp.starts_with("./CipherLog-") || !j.path().is_file() {
                continue;
            };

            let f = tp.replace(&(".".to_string() + get_ext(&p).unwrap_or("txt")), "");
            let f = f.replace("./CipherLog-", "");

            match f.parse::<i32>() {
                Ok(g) => {
                    if (g + 1) > id {
                        id = g + 1
                    }
                }
                _ => (),
            }
        }
    }

    id
}
