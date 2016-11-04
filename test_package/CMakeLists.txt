PROJECT(MyHello)
cmake_minimum_required(VERSION 3.0)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

ADD_EXECUTABLE(example sdl.c)
MESSAGE(${CONAN_LIBS})
TARGET_LINK_LIBRARIES(example ${CONAN_LIBS})
# TARGET_LINK_LIBRARIES(example SDL2_image jpeg turbojpeg png16 m z SDL2 SDL2main dl rt pthread)

