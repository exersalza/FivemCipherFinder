use std::io::Read;
use std::{fs, path::PathBuf};

use crate::utils::{self, check_regex, ScanLevel, CIPHER_REGEX, SIMPLE_URL_REGEX};

#[derive(Debug)]
pub struct ScannedFile {
    path: PathBuf,
    findings: Vec<(usize, String, Vec<String>)>, // line number, confidence
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

    /// gets the file contents, converts it to an utf8 but lossy
    fn get_file_contents(&self) -> std::io::Result<Vec<String>> {
        let mut file = fs::File::open(&self.path)?;
        let mut buf = vec![];

        file.read_to_end(&mut buf)?;

        let cont = String::from_utf8_lossy(&buf);

        Ok(cont.split('\n').map(str::to_string).collect())
    }

    /// Scans file
    fn scan_file(&mut self) -> std::io::Result<()> {
        let contents = self.get_file_contents()?;
        let scan_mode = match utils::SCAN_LEVEL.try_lock() {
            Ok(v) => v.clone(),
            Err(_) => ScanLevel::Standard,
        };

        for (ln, line) in contents.into_iter().enumerate() {
            if line.contains('\n') {
                continue;
            }

            let line = line.as_str();
            //todo implement modes here somehow
            if scan_mode.eq(&ScanLevel::Aggressive) {
                println!("aggressive mode active");
            }
            self.add_infected(ln, line, check_regex(&CIPHER_REGEX, line));
            self.add_infected(ln, line, check_regex(&SIMPLE_URL_REGEX, line));
        }

        Ok(())
    }

    /// add infected lines to the lister
    fn add_infected(&mut self, ln: usize, line: &str, trigger: Vec<String>) {
        if trigger.is_empty() {
            return;
        }

        let _ = self.findings.push((ln, line.to_string(), trigger));
    }

    /// getter for the vec of infected lines
    pub fn get_infected(&self) -> &Vec<(usize, String, Vec<String>)> {
        self.findings.as_ref()
    }
}
