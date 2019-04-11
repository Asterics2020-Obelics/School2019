all: main

main: main.cpp libfibonacci.so
	# compile main.cpp using the c++ compiler
	# save to `main`
	# link against the library `fibonacci`
	# include the current directory in the directories searched for libraries
	# include the current directory in the directories searched for headers
	# compile the path where the library is to find into the binary
	$(CXX) main.cpp \
		-o main \
		-lfibonacci \
		-L. \
		-I. \
		-Wl,-rpath .

libfibonacci.so: fibonacci.h fibonacci.cpp
	# compile fibonacci.cpp into a shared library 
	# into libfibonacci.so
	$(CXX) fibonacci.cpp \
		-o libfibonacci.so \
		--shared

clean:
	rm -f main libfibonacci.so 
