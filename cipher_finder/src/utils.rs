use lazy_static::lazy_static;
use regex::Regex;

lazy_static! {
    pub static ref CIPHER_REGEX: Regex = Regex::new(r"(((\\[xu])([a-fA-F0-9]{2}))+)").unwrap();
    pub static ref SIMPLE_URL_REGEX: Regex = Regex::new(r"https?://(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)").unwrap();
}

/// increases or decreases the confidence if the regex finds something or not.
pub fn update_confidence(regex: &Regex, haystack: &str, confidence: &mut f32) -> Option<bool> {
    for found in regex.captures_iter(haystack) {
        let mut yeet = 0;
        println!("{found:?}");

        if haystack.contains("\\x") { // do something different if not cleartext stuff. yes
            // yeet = 1;
        }
        println!("\n--------\n")
    }

    Some(true)
}
