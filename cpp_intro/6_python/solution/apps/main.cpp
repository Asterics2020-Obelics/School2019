#include <iostream>
#include "fibonacci.h"


int main() {

	for (unsigned int i = 0; i < 10; i++) {
		std::cout << i << ": " << fibonacci(i) << std::endl;
	}
     
    return 0;
}
