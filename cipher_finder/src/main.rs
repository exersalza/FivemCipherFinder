use clap::Parser;

use cipher_finder::{file, os};

// todo:
//  scan modes: // defines how many patterns will be used to scan one file
//   aggressive
//   passive

#[derive(Parser, Debug)]
#[clap(name = "FivemCipherFinder", about = "FivemCipherFinder finds ciphers in your scripts.", long_about = None)]
struct Args {
    #[clap(short = 'm', long = "mode", default_value = "aggressive")]
    /// Scan mode
    mode: String,

    #[clap(short = 'p', long = "path", default_value = ".")]
    /// Paht to the Directory where your server is located
    path: String,

    #[clap(short = 'e', long = "exclude", default_value = "")]
    /// Exclude given Paths from Search
    exclude: String,
}

fn main() -> std::io::Result<()> {
    let opt = Args::parse();

    os::get_all_files(opt.path, None);
    // let infected = file::ScannedFile::new("../cars/server.lua");
    // println!("{:?}", infected?.get_infected());
    Ok(())
}
