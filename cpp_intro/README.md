# Basic Introduction to C++

A small introduction to the basics of C++.

## Compiler

C++ is a compiled language, that means,
that running code is a two-step procedure.

A compiler converts source file(s) into binary
executables or libraries, that can be run or
used.

MacOS users should use `clang++`, Linux users `g++`.
If you are using the conda environment of the school,
use `$CXX` on Linux, which points to the compiler
that comes with Anaconda.


## Hello World

Create a file called `hello.cpp` with the 
following content:

```c++
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
```

Before we can run it, we need to compile it.

Linux users need to run:
```
$ g++ hello.cpp -o hello
```
Use `$CXX` instead of `g++` if you use the conda school environment.

MacOS users need to run

```
$ clang++ hello.cpp -o hello
```

This will create an executable program called `hello`, because we used `-o hello`, which you can run using

```
$ ./hello
```

## Examples and Exercises

* `1_hello` the hello world example
* `2_fibonacci` simple program calculating fibonacci numbers
* `3_fibonacci_lib` Make a library calculating fibonacci numbers
* `4_cmake` Compile the library using cmake
* `5_python` Call the library from python


### References

* Large C++ Tutorial: https://www.learncpp.com/cpp-tutorial/
* Modern CMAKE: https://cliutils.gitlab.io/modern-cmake/
* pybind11
* cython
