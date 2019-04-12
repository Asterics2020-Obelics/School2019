#include <iostream>
#include "fibonacci.h"


int main(int argc, char* argv[]) {

	if (argc != 2) {
		std::cerr << "Usage: main <n>" << std::endl;
		return 1;
	}

	if (argv[1] == "-h" || argv[1] == "--help") {
		std::cout << "Print the nth Fibonacci Number" << std::endl << std::endl;
		std::cout << "Usage: main <n>" << std::endl;
		return 0;
	}

	unsigned long n = 0;
	try {
		n = std::stoi(argv[1]);
	} catch(const std::exception& e) {
		std::cerr << "Argument mus be an integer" << std::endl;
		return 2;
	}

	std::cout << fibonacci(n) << std::endl;
     
    return 0;
}
