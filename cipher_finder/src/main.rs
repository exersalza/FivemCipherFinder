use clap::Parser;

use cipher_finder::files;

// todo:
//  scan modes:
//   aggressive
//   passive

#[derive(Parser, Debug)]
#[clap(name = "FivemCipherFinder", about = "FivemCipherFinder finds ciphers in your scripts.", long_about = None)]
struct Args {
    #[clap(short = 'm', long = "mode")]
    mode: String,
}

fn main() -> std::io::Result<()> {
    let infected = files::ScannedFile::new("../cars/server.lua");
    println!("{:?}", infected?.get_infected());
    Ok(())
}
