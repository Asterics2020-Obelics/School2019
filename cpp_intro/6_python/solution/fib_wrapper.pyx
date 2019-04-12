# cython: language_level = 3
# distutils: language = c++

cdef extern from "fibonacci.h":
    cpdef unsigned long fibonacci(unsigned int n)
