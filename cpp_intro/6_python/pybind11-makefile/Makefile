all: libfibonacci.so fibmod fib_cli

fib_cli: apps/fib_cli.cpp libfibonacci.so
	# compile fib_cli.cpp using the c++ compiler
	# save to `fib_cli`
	# link against the library `fibonacci`
	# include the current directory in the directories searched for libraries
	# include the current directory in the directories searched for headers
	# compile the path where the library is to find into the binary
	$(CXX) apps/fib_cli.cpp \
		-o fib_cli \
		-lfibonacci \
		-L. \
		-Iinclude \
		-Wl,-rpath .

libfibonacci.so: include/fibonacci.h src/fibonacci.cpp
	# compile fibonacci.cpp into a shared library 
	# into libfibonacci.so
	$(CXX) src/fibonacci.cpp \
		-I include \
		-o libfibonacci.so \
		-Wl,-rpath . \
		--shared

fibmod: libfibonacci.so src/fibonacci_wrapper.cpp
	# compile a python wrapper using pybind 11
	$(CXX) -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup \
		-Iinclude -L. -lfibonacci \
		`python3 -m pybind11 --includes` \
		src/fibonacci_wrapper.cpp \
		-o fibmod`python3-config --extension-suffix`

clean:
	rm -f fib_cli libfibonacci.so fibmod.cpython* fib_cli
