#include <iostream>
#include <vector>

std::vector<unsigned long> fibonacci(unsigned int n) {
	std::vector<unsigned long> result;
	
	for (unsigned int i = 0; i < n; i++) {
		
		if (i <= 1) {
			result.push_back(1);
		} else {
			result.push_back(result.at(i - 1) + result.at(i - 2));
		}
	
	}

    return result;
}


int main() {
	
	std::vector<unsigned long> numbers = fibonacci(10);

	for (unsigned long fib: numbers) {
		std::cout << fib << std::endl;
	}
     
    return 0;
}
