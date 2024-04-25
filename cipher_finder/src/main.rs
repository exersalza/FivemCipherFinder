use clap::Parser;

pub mod de_obfs;
pub mod file;
pub mod os;
pub mod utils;

// todo:
//  scan modes: // defines how many patterns will be used to scan one file
//   aggressive // all
//   passive // main patterns, hex detection

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

    os::get_all_files(opt.path, Some(vec!["target".to_string()]));
    // let infected = file::ScannedFile::new("../cars/server.lua");
    // println!("{:?}", infected?.get_infected());
    Ok(())
}
