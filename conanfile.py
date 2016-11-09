from conans import ConanFile, CMake
from conans.tools import download, unzip
import shutil, os

class SDLConan(ConanFile):
    name = "SDL2_image"
    version = "2.0.1"
    folder = "SDL2_image-%s" % version
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = '''shared=False
    fPIC=True'''
    generators = "cmake"
    exports = ["CMakeLists.txt"]
    url="http://github.com/lasote/conan-sdl2_image"
    requires = "SDL2/2.0.4@lasote/stable", "libpng/1.6.21@lasote/stable", "libjpeg-turbo/1.5.1@lasote/stable"  # TODO: We should add libwebp
    license="MIT"

    def config(self):
        del self.settings.compiler.libcxx 

    def source(self):
        zip_name = "%s.tar.gz" % self.folder
        download("https://www.libsdl.org/projects/SDL_image/release/%s" % zip_name, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        shutil.copy("CMakeLists.txt", "%s/CMakeLists.txt" % self.folder)
        cmake = CMake(self.settings)
        shared = "-DBUILD_SHARED_LIBS=%s" % ("ON" if self.options.shared else "OFF")
        if self.settings.compiler == "Visual Studio":
            self.options.fPIC = False
        fpic = "-DFPIC=ON" if self.options.fPIC else ""

        self.run("cd %s &&  mkdir build" % self.folder)
        self.run('cd %s/build && cmake .. %s %s %s' % (self.folder, cmake.command_line, shared, fpic))
        self.run("cd %s/build && cmake --build . %s" % (self.folder, cmake.build_config))

    def package(self):
        self.copy(pattern="SDL_image.h", dst="include", src="%s" % self.folder, keep_path=False) #TODO: "SDL2" subfolder
        self.copy(pattern="*.lib", dst="lib", src="%s" % self.folder, keep_path=False)

        if not self.options.shared:
            self.copy(pattern="*.a", dst="lib", src="%s" % self.folder, keep_path=False)
        else:
            self.copy(pattern="*.so*", dst="lib", src="%s" % self.folder, keep_path=False)
            self.copy(pattern="*.dylib*", dst="lib", src="%s" % self.folder, keep_path=False)
            self.copy(pattern="*.dll", dst="bin", src="%s" % self.folder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["SDL2_image"]
