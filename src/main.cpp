//
// Created by julian on 10/24/22.
//

#include <regex>
#include <fstream>
#include <iostream>
#include <filesystem>

using rdi = std::filesystem::recursive_directory_iterator;

int main(int argc, char **argv) {
    std::string regex = R"((((\x|\u)([a-fA-F0-9]{2})){2}))";

    std::fstream file;
    std::string line;

    std::string search = "magic";
    auto res = std::find_if(argv + 1, argv + argc, [&](char const * const arg){return arg == search;});

    for (const auto& entry : rdi(search)) {
        /*std::cout << direntry << '\n';*/
    }

    file.open("src/testFile.lua", std::ios::in);
    if (!file.is_open()) { file.close(); printf("Can't open file: %s", "ff");}


    file.close();


    return 0;
}