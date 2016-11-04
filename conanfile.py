from conans import ConanFile
from conans import tools
import os
import shutil
from conans import CMake, ConfigureEnvironment
from conans.model.settings import Settings
import copy

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
    requires = "SDL2/2.0.4@lasote/stable", "libpng/1.6.21@lasote/stable", "libjpeg-turbo/1.4.2@lasote/stable", 
    license="MIT"

    def config(self):
        del self.settings.compiler.libcxx 

    def source(self):
        zip_name = "%s.tar.gz" % self.folder
        tools.download("https://www.libsdl.org/projects/SDL_image/release/%s" % zip_name, zip_name)
        tools.unzip(zip_name)

    def build(self):
        if self.settings.os == "Windows":
            sln_path = "%s/VisualC/SDL_image.sln" % self.folder
            more_libs = ["%s.lib" % lib for lib in self.deps_cpp_info["SDL2"].libs]
            lib_path = self.deps_cpp_info["SDL2"].lib_paths[0]
            additional_libs = ";".join(more_libs).replace("SDL2.lib;", "").replace("SDL2main.lib;", "")
            tools.replace_in_file("%s/VisualC/SDL_image.vcxproj" % self.folder, "SDL2.lib", "%s\\SDL2.lib;%s\\SDL2main.lib;%s" % (lib_path, lib_path, additional_libs))
            build_command = tools.build_sln_command(self.settings, sln_path, targets=["SDL2_image"])
            env = ConfigureEnvironment(self)
            command = "%s && %s" % (env.command_line_env, build_command)
            self.output.warn(command)
            self.run(command)
        else:
            self.build_with_make()

   
    def build_with_make(self):
        
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        if self.options.fPIC:
            env_line = env.command_line.replace('CFLAGS="', 'CFLAGS="-fPIC ')
        else:
            env_line = env.command_line
            
        custom_vars = 'LIBPNG_LIBS= SDL_LIBS= LIBPNG_CFLAGS='
        sdl2_config_path = os.path.join(self.deps_cpp_info["SDL2"].lib_paths[0], "sdl2-config")
         
        self.run("cd %s" % self.folder)
        self.run("chmod a+x %s/configure" % self.folder)
        self.run("chmod a+x %s" % sdl2_config_path)
        
        self.output.warn(env_line)
        if self.settings.os == "Macos": # Fix rpath, we want empty rpaths, just pointing to lib file
            old_str = "-install_name \$rpath/"
            new_str = "-install_name "
            replace_in_file("%s/configure" % self.folder, old_str, new_str)
        
        old_str = '#define LOAD_PNG_DYNAMIC "$png_lib"'
        new_str = ''
        tools.replace_in_file("%s/configure" % self.folder, old_str, new_str)
        
        old_str = '#define LOAD_JPG_DYNAMIC "$jpg_lib"'
        new_str = ''
        tools.replace_in_file("%s/configure" % self.folder, old_str, new_str)
        
        configure_command = 'cd %s && %s SDL2_CONFIG=%s %s ./configure' % (self.folder, env_line, sdl2_config_path, custom_vars)
        self.output.warn("Configure with: %s" % configure_command)
        self.run(configure_command)
        
        old_str = 'DEFS = '
        new_str = 'DEFS = -DLOAD_JPG=1 -DLOAD_PNG=1 ' # Trust conaaaan!
        tools.replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
        
        old_str = '\nLIBS = '
        new_str = '\n# Removed by conan: LIBS2 = '
        tools.replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
        
        old_str = '\nLIBTOOL = '
        new_str = '\nLIBS = %s \nLIBTOOL = ' % " ".join(["-l%s" % lib for lib in self.deps_cpp_info.libs]) # Trust conaaaan!
        tools.replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
        
        old_str = '\nLIBPNG_CFLAGS ='
        new_str = '\n# Commented by conan: LIBPNG_CFLAGS ='
        tools.replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
        
        old_str = '\nLIBPNG_LIBS ='
        new_str = '\n# Commented by conan: LIBPNG_LIBS ='
        tools.replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
        
        old_str = '\nOBJCFLAGS'
        new_str = '\n# Commented by conan: OBJCFLAGS ='
        tools.replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
        
        old_str = '\nSDL_CFLAGS ='
        new_str = '\n# Commented by conan: SDL_CFLAGS ='
        tools.replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
        
        old_str = '\nSDL_LIBS ='
        new_str = '\n# Commented by conan: SDL_LIBS ='
        tools.replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
        
        old_str = '\nCFLAGS ='
        new_str = '\n# Commented by conan: CFLAGS ='
        tools.replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
        
        old_str = '\n# Commented by conan: CFLAGS ='
        fpic = "-fPIC"  if self.options.fPIC else ""
        m32 = "-m32" if self.settings.arch == "x86" else ""
        debug = "-g" if self.settings.build_type == "Debug" else "-s -DNDEBUG"
        new_str = '\nCFLAGS =%s %s %s %s\n# Commented by conan: CFLAGS =' % (" ".join(self.deps_cpp_info.cflags), fpic, m32, debug)
        tools.replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
        
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
            self.copy(pattern="*.dll", dst="bin", src="%s" % self.folder, keep_path=False) 
        else:
            self.copy(pattern="*.so*", dst="lib", src="%s" % self.folder, keep_path=False)
            self.copy(pattern="*.dylib*", dst="lib", src="%s" % self.folder, keep_path=False)
            
        self.copy(pattern="*.lib", dst="lib", src="%s" % self.folder, keep_path=False)

    def package_info(self):  
                
        self.cpp_info.libs = ["SDL2_image"]
