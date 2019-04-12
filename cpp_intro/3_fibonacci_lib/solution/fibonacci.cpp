#include "fibonacci.h"

unsigned long fibonacci(unsigned int n) {
	unsigned long n0 = 1;
	unsigned long n1 = 1;
	unsigned long tmp = 1;

	for (unsigned int i = 0; i < n; i++) {
		tmp = n1;
		n1 = n0 + n1;
		n0 = tmp;
	}
	return n0;
}
