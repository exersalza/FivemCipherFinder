use std::io::Read;
use std::{fs, path::PathBuf};

use crate::utils::{check_regex, CIPHER_REGEX, SIMPLE_URL_REGEX};

pub struct ScannedFile {
    path: PathBuf,
    findings: Vec<(i32, f32)>, // line number, confidence
}

impl ScannedFile {
    /// Creates new ScannedFile object and Scans the file in creation
    pub fn new(path: PathBuf) -> std::io::Result<ScannedFile> {
        let mut ret = Self {
            path,
            findings: vec![],
        };
        ret.scan_file()?; // let the caller handle any errors.

        Ok(ret)
    }

    fn get_file_contents(&self) -> std::io::Result<Vec<String>> {
        println!("{:?}", self.path);
        let mut file = fs::File::open(&self.path)?;
        let mut buf = vec![];

        match file.read_to_end(&mut buf) {
            Err(e) => return Err(e),
            _ => (),
        };

        let cont = String::from_utf8_lossy(&buf);

        Ok(cont.split("\n").map(str::to_string).collect())
    }

    /// Scans file
    fn scan_file(&mut self) -> std::io::Result<()> {
        let contents = self.get_file_contents()?;
        let mut ln = 0;

        for line in contents {
            ln += 1;

            if line.contains("\n") {
                continue;
            }

            let line = line.as_str();

            check_regex(&CIPHER_REGEX, line);
            check_regex(&SIMPLE_URL_REGEX, line);
        }

        Ok(())
    }

    /// Add infected lines to the lister
    fn add_infected(&mut self, ln: i32, confidence: f32) {
        let _ = &self.findings.push((ln, confidence));
    }

    pub fn get_infected(&self) -> Vec<(i32, f32)> {
        self.findings.to_owned()
    }
}
