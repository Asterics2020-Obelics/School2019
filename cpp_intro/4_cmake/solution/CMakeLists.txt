cmake_minimum_required(VERSION 3.1)


project(Fibonacci VERSION 0.1
	              DESCRIPTION "Calculate Fibonacci Numbers using C++"
                  LANGUAGES CXX)

# set correct runpath for installed libraries
# and executables
SET(CMAKE_SKIP_BUILD_RPATH  FALSE)
SET(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)
set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")
SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)


add_library(fibonacci SHARED src/fibonacci.cpp include/fibonacci.h)
target_include_directories(fibonacci PUBLIC include)
set_target_properties(fibonacci PROPERTIES PUBLIC_HEADER include/fibonacci.h)

add_executable(fib apps/main.cpp)
target_link_libraries(fib PUBLIC fibonacci)

# enable installing
install(TARGETS fibonacci fib
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib
        RUNTIME DESTINATION bin
        INCLUDES DESTINATION include
		PUBLIC_HEADER DESTINATION include)
