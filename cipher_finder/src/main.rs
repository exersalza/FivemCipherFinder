use clap::Parser;

use cipher_finder::files;

// todo:
//  scan modes:
//   aggressive
//   passive

#[derive(Parser, Debug)]
#[command("0.0.1", "FivemCipherFinder finds ciphers in your scripts.", long_about=None)]
struct Args {
    #[arg("-m", "--mode")]
    mode: String
}


fn main() -> std::io::Result<()> {
    let infected = files::ScannedFile::new("../cars/server.lua");
    println!("{:?}", infected?.get_infected());
    Ok(())
}
