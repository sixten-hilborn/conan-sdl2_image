[![Build Status](https://travis-ci.org/lasote/conan-sdl2_image.svg)](https://travis-ci.org/lasote/conan-sdl2_image)


# conan-sdl2_image

[Conan.io](https://conan.io) package for SDL2_image library

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/SDL2_image/2.0.1/lasote/stable).

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py

## Upload packages to server

    $ conan upload SDL2_image/2.0.3@lasote/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install SDL2_image/2.0.3@lasote/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    SDL2_image/2.0.3@lasote/stable

    [options]
    SDL2_image:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install .

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
