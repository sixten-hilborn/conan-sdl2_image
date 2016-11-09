cmake_minimum_required(VERSION 2.8.12)

# Project Name and start working in project scope (some things just work until now, some just work after this command)
project(SDL2_image C)

# Add conan dependencies
include(../conanbuildinfo.cmake) # TODO This is actually ugly isnt it? Since it only works inside a "require", not using a normal "mkdir build && cd build && conan install .. && cmake .."
conan_basic_setup()


if(APPLE)
  option(USE_IMAGEIO "" ON)
  if(USE_IMAGEIO)
    set(IMAGEIO_SOURCE "IMG_ImageIO.m")
  endif()
endif()

set(SOURCE_FILES
IMG.c
IMG_bmp.c
IMG_gif.c
IMG_jpg.c
IMG_lbm.c
IMG_pcx.c
IMG_png.c
IMG_pnm.c
IMG_tga.c
IMG_tif.c
IMG_xcf.c
IMG_xpm.c
IMG_xv.c
IMG_webp.c
${IMAGEIO_SOURCE}
miniz.h
CACHE INTERNAL "")

add_library(SDL2_image ${SOURCE_FILES})

if(FPIC)
    MESSAGE(STATUS "ENABLED FPIC")
    SET_TARGET_PROPERTIES(SDL2_image PROPERTIES COMPILE_FLAGS "-fPIC")
endif()
