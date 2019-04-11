#include <iostream>

unsigned long fibonacci(unsigned int n) {
    if (n == 0 || n == 1) {
        return 1;
    }

    return fibonacci(n - 1) + fibonacci(n - 2);
}


int main() {

	for (unsigned int i = 0; i < 10; i++) {
		std::cout << i << ": " << fibonacci(i) << std::endl;
	}
     
    return 0;
}
