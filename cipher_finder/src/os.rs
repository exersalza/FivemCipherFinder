use std::{fs, io};

pub fn get_all_files(path: String, exclude: Option<Vec<String>>) -> Vec<String> {
    let mut ret = vec![];

    println!("{path}");
    let g = fs::read_dir(path)
        .unwrap()
        .map(|dir| dir.map(|f| f.path()))
        .collect::<Result<Vec<_>, io::Error>>();

    println!("{g:?}");

    ret
}

fn read_recursive_dir(d: String) -> Vec<String> {
    todo!()
}
