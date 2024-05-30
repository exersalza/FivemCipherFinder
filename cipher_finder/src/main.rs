//!
#[warn(missing_debug_implementations, missing_docs)]
use clap::Parser;
use utils::ScanLevel;

use crate::file_op::ScannedFile;

pub mod de_obfs;
pub mod file_op;
pub mod os;
pub mod utils;

// todo:
//  scan modes: // defines how many patterns will be used to scan one file
//   aggressive // all
//   passive // main patterns, hex detection
#[derive(Parser, Debug)]
#[clap(name = "FivemCipherFinder", about = "FivemCipherFinder finds ciphers in your scripts.", long_about = None)]
struct Args {
    #[clap(short = 'm', long = "mode", default_value = "standard")]
    /// Scan mode
    mode: ScanLevel,

    #[clap(short = 'p', long = "path", default_value = ".")]
    /// Paht to the Directory where your server is located
    path: String,

    #[clap(short = 'x', long = "exclude", default_value = "")]
    /// Exclude given Paths from Search. Syntax: foo,bar,foobar
    exclude: String,

    #[clap(long = "include-git", default_value = "false")]
    /// includes content of .gitignore files. Maybe increases the time it needs to filter out files
    include_git: bool,

    /// Prevents logs from being created
    #[clap(short = 'n', long = "no-log", default_value = "false")]
    no_log: bool,

    /// Prints some information
    #[clap(short = 'v', default_value = "false")]
    simple_verbose: bool,

    /// Prints even more information
    #[clap(long = "verbose", default_value = "false")]
    verbose: bool,
}

fn main() -> std::io::Result<()> {
    // i kissed a girl and i liked it https://images.app.goo.gl/ynuCJ85rmxJFVNBs5
    let opt = Args::parse();

    match utils::SCAN_LEVEL.try_lock() {
        Ok(mut l) => *l = opt.mode,
        Err(f) => panic!("Couldn't get SCAN_LEVEL lock -> {f:?}"),
    };

    let exludes = utils::format_dir_str(opt.exclude);
    let mut all_paths = os::get_all_files(opt.path.clone(), Some(exludes.clone()));

    if opt.include_git {
        let git_ignores = utils::filter_viables(all_paths.clone(), "gitignore");

        // do the readout part and add to exlude thingi
        let mut ignored = utils::parse_gitignores(git_ignores);
        ignored.extend(exludes);
        all_paths = os::get_all_files(opt.path, Some(ignored));
    }

    let paths = utils::filter_viables(all_paths, "lua");

    for i in paths {
        let infected = ScannedFile::new(i);
        println!("{:?}", infected?.get_infected());
    }

    Ok(())
}
