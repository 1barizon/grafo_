cmake_minimum_required(VERSION 3.10)

# Set the project name
project(grafos)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
# Add the include directory
include_directories(${PROJECT_SOURCE_DIR}/include)

# Add the executable
add_executable(grafos src/main.cpp src/graph.cpp)

