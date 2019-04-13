#include <pybind11/pybind11.h>
#include "fibonacci.h"

PYBIND11_MODULE(fibmod, m) {
    m.doc() = "pybind11 example plugin for fibonacci";

    m.def("fibonacci", &fibonacci, "Fibonacci function using C++");
}
