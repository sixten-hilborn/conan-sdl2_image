from conans import ConanFile
from conans.tools import download, unzip, replace_in_file
import os
import shutil
from conans import CMake, ConfigureEnvironment

class SDLConan(ConanFile):
    name = "SDL2_image"
    version = "2.0.1"
    folder = "SDL2_image-%s" % version
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = '''shared=False
    fPIC=True'''
    generators = "cmake"
    url="http://github.com/lasote/conan-sdl2_image"
    requires = "SDL2/2.0.4@lasote/stable", "libpng/1.6.21@lasote/stable", "libjpeg-turbo/1.4.2@lasote/stable", "zlib/1.2.8@lasote/stable"
    license="MIT"

    def config(self):
        del self.settings.compiler.libcxx 

    def source(self):
        zip_name = "%s.tar.gz" % self.folder
        download("https://www.libsdl.org/projects/SDL_image/release/%s" % zip_name, zip_name)
        unzip(zip_name)

    def build(self):
        if self.settings.os == "Windows":
            self.output.error("Windows not supported yet. Contact the author on github: github.com/lasote/conan-sdl2_image")
        else:
            self.build_with_make()

   
    def build_with_make(self):
        
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        if self.options.fPIC:
            env_line = env.command_line.replace('CFLAGS="', 'CFLAGS="-fPIC ')
        else:
            env_line = env.command_line
            
        #env_line = env_line.replace('LIBS="', 'LIBS2="') # Rare error if LIBS is kept
         
        self.run("cd %s" % self.folder)
        self.run("chmod a+x %s/configure" % self.folder)
        
        self.output.warn(env_line)
        if self.settings.os == "Macos": # Fix rpath, we want empty rpaths, just pointing to lib file
            old_str = "-install_name \$rpath/"
            new_str = "-install_name "
            replace_in_file("%s/configure" % self.folder, old_str, new_str)
            self.run("chmod a+x %s/build-scripts/gcc-fat.sh" % self.folder)
            configure_command = 'cd %s && CC=$(pwd)/build-scripts/gcc-fat.sh ./configure %s' % (self.folder, args)
        else:
            configure_command = 'cd %s && %s ./configure' % (self.folder, env_line)
        self.output.warn("Configure with: %s" % configure_command)
        self.run(configure_command)
        self.run("cd %s && %s make" % (self.folder, env_line))


    def package(self):
        """ Define your conan structure: headers, libs and data. After building your
            project, this method is called to create a defined structure:
        """
        self.copy(pattern="SDL_image.h", dst="include", src="%s" % self.folder, keep_path=False)
        
        # UNIX
        if not self.options.shared:
            self.copy(pattern="*.a", dst="lib", src="%s" % self.folder, keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="%s" % self.folder, keep_path=False)   
        else:
            self.copy(pattern="*.so*", dst="lib", src="%s" % self.folder, keep_path=False)
            self.copy(pattern="*.dylib*", dst="lib", src="%s" % self.folder, keep_path=False)

    def package_info(self):  
                
        self.cpp_info.libs = ["SDL2_image"]
