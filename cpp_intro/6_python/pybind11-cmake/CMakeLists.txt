cmake_minimum_required(VERSION 3.1)

project(Fibonacci VERSION 0.1
                  DESCRIPTION "Calculate Fibonacci numbers using C++, with python binding"
                  LANGUAGES CXX)

add_library(fibonacci SHARED src/fibonacci.cpp include/fibonacci.h)
target_include_directories(fibonacci PUBLIC include)

add_executable(fib_cli apps/fib_cli.cpp)
target_link_libraries(fib_cli PRIVATE fibonacci)

find_package(pybind11 REQUIRED)
pybind11_add_module(fibmod src/fibonacci_wrapper.cpp)
target_link_libraries(fibmod PRIVATE fibonacci)
