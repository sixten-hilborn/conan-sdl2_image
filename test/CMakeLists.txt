PROJECT(MyHello)
cmake_minimum_required(VERSION 3.0)

include(conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

ADD_EXECUTABLE(example sdl.c)
TARGET_LINK_LIBRARIES(example ${CONAN_LIBS})
