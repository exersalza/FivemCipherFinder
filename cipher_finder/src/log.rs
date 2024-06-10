use std::fmt;
use std::fs;
use std::io;

use crate::utils::get_ext;

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
        let mut id = 0;

        for i in fs::read_dir(".").unwrap() {
            if let Ok(j) = i {
                let p = j.path();
                let tp = p.to_str().unwrap_or("whyisliamnothere.txt");

                if !tp.starts_with("CipherLog-") || !j.path().is_file() {
                    continue;
                };

                let f = tp.replace(get_ext(&p).unwrap_or(".txt"), "");
                let f = f.replace("./CipherLog-", "");

                println!("{f}");

                id = if let Ok(g) = f.parse::<i32>() {
                    println!("ok");
                    g + 1
                } else {
                    println!("not ok");
                    0
                }
            }
        }

        let _handle = fs::OpenOptions::new()
            .write(true)
            .create(true)
            .open(format!("./CipherLog-{id}.txt"));

        Ok(0)
    }
}
