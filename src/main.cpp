//
// Created by julian on 10/24/22.
//

#include <iostream>
#include <fstream>
#include <regex>

using namespace std;

int main() {
    string regex = R"((((\x|\u)([a-fA-F0-9]{2})){2}))";

    fstream file;
    string line;
    string foundCipher;
    int count = 0;

    file.open("../src/testFile.lua", ios::in | ios::app);
    if (!file.is_open()) { file.close(); return 1;}

    while (!file.eof()) {
        count++;
        getline(file, line, '\n');
        if (line.empty())
            continue;
    }
    file.close();
    cout << count << endl;


    return 0;
}