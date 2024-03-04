use std::fs;
use std::io::Read;

use crate::utils::{CIPHER_REGEX, SIMPLE_URL_REGEX, update_confidence};

pub struct ScannedFile {
    path: String,
    findings: Vec<(i32, f32)>,  // line number, confidence
}


impl ScannedFile {
    /// Creates new ScannedFile object and Scans the file in creation
    pub fn new(path: &str) -> std::io::Result<ScannedFile> {
        let mut ret = Self { path: path.to_string(), findings: vec![] };
        ret.scan_file()?; // let the caller handle any errors.

        Ok(ret)
    }

    fn get_file_contents(&self) -> std::io::Result<Vec<String>> {
        let mut cont = String::new();
        let mut file = fs::File::open(&self.path)?;

        file.read_to_string(&mut cont)?;

        Ok(cont.split("\n").map(str::to_string).collect())
    }

    /// Scans file
    fn scan_file(&mut self) -> std::io::Result<()> {
        let contents = self.get_file_contents()?;
        let mut i = 0;

        for line in contents {
            i += 1;

            if line == "\n" || line == "\r\n" {
                continue;
            }

            let line = line.as_str();
            let mut confidence: f32 = 0.0;

            update_confidence(&CIPHER_REGEX, line, &mut confidence);
            update_confidence(&SIMPLE_URL_REGEX, line, &mut confidence);

            if confidence != 0.0 {
                self.add_infected(i, confidence);
            }
        }

        Ok(())
    }

    /// Add infected lines to the lister
    fn add_infected(&mut self, ln: i32, confidence: f32) {
        &self.findings.push((ln, confidence));
    }

    pub fn get_infected(&self) -> Vec<(i32, f32)> {
        self.findings.to_owned()
    }
}

