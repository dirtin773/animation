#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <thread>
#include <chrono>

std::string getFileContent(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: unable to open file " << filename << std::endl;
        return {};
    }
    return std::string(
        (std::istreambuf_iterator<char>(file)),
        std::istreambuf_iterator<char>());
}

std::vector<std::string> split(const std::string& content, const std::string& delimiter) {
    std::vector<std::string> parts;
    size_t start = 0;
    size_t end = content.find(delimiter, start);
    while (end != std::string::npos) {
        parts.push_back(content.substr(start, end - start));
        start = end + delimiter.length();
        end = content.find(delimiter, start);
    }
    parts.push_back(content.substr(start));
    return parts;
}

void clearScreen() {
    for (int i = 0; i < 50; ++i) {
        std::cout << '\n';
    }
}

void runAnimation(const std::string& filename) {
    std::string content = getFileContent(filename);
    if (content.empty()) {
        std::cerr << "Failed to load animation from " << filename << std::endl;
        return;
    }
    std::vector<std::string> frames = split(content, "FRAME");

    std::cout << "Press Enter to stop the animation...\n";
    std::thread animThread([&frames]() {
        while (true) {
            for (const std::string& frame : frames) {
                clearScreen();
                std::cout << frame << std::endl;
                std::this_thread::sleep_for(std::chrono::milliseconds(33));
            }
        }
        });

    std::cin.ignore();
    animThread.detach();
}

int main() {
    setlocale(LC_ALL, "Russian");
    while (true) {
        clearScreen();
        std::cout << "Главное меню:\n";
        std::cout << "1. Запустить анимацию 1\n";
        std::cout << "2. Запустить анимацию 2\n";
        std::cout << "3. Выйти из программы\n";
        std::cout << "Выберите опцию (1-3): ";

        int choice = 0;
        std::cin >> choice;
        std::cin.ignore();

        if (choice == 1) {
            runAnimation("animation1.txt");
        }
        else if (choice == 2) {
            runAnimation("animation2.txt");
        }
        else if (choice == 3) {
            std::cout << "Выход из программы.\n";
            break;
        }
        else {
            std::cout << "Неверный выбор, попробуйте снова.\n";
            std::this_thread::sleep_for(std::chrono::seconds(2));
        }
    }

    return 0;
}