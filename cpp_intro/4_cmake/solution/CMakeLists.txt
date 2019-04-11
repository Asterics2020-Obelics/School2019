cmake_minimum_required(VERSION 3.1...3.14)

if(${CMAKE_VERSION} VERSION_LESS 3.12)
    cmake_policy(VERSION ${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION})
endif()

project(Fibonacci VERSION 0.1
	              DESCRIPTION "Calculate Fibonacci Numbers using C++"
                  LANGUAGES CXX)


add_library(fibonacci SHARED src/fibonacci.cpp include/fibonacci.h)
target_include_directories(fibonacci PUBLIC include)

add_executable(main apps/main.cpp)
target_link_libraries(main PUBLIC fibonacci)
