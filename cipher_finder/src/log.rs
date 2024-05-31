pub enum Verbosity {
    None,
    Verbose,
    VeryVerbose,
}

pub struct Logging {
    mode: Verbosity,
}

impl Logging {
    pub fn new(verbose: bool, very_verbose: bool) -> Self {
        let mode = match (very_verbose, verbose) {
            (true, _) => Verbosity::VeryVerbose,
            (false, true) => Verbosity::Verbose,
            (false, false) => Verbosity::None,
        };

        Self { mode }
    }
}
