// C++ uses // to make comments

// here we include the library iostream
// which is included in the standard library 
// and allows us to use the std::cout stream to
// print to the console
#include <iostream>

// we define a `main` function, which is what every
// executable must have, the entry point to the program.
// The function must return an `int`, 0 is the convention
// for success.
int main() {
	// Print "Hello, World!" to the terminal.
	// std::endl is os-indenpent way to create a new line
	// (Windows is different than MacOS/Linux)
    std::cout << "Hello, World!" << std::endl;

	// If we reach this point, we were successful, so return 0.
    return 0;
}
