from conans import ConanFile, CMake, tools
from conans.tools import os_info

class zziplibConan(ConanFile):
    name = "zziplib"
    version = "0.13.69"
    license = "GNU"
    author = "Edgar (Edgar@AnotherFoxGuy.com)"
    url = "https://github.com/AnotherFoxGuy/conan-ZZIPlib"
    description = "The zziplib provides read access to zipped files in a zip-archive, using compression based solely on free algorithms provided by zlib."
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    requires = "zlib/[1.x]@conan/stable"

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/gdraheim/zziplib.git", "develop")
        tools.replace_in_file("CMakeLists.txt", "### Path to additional CMake modules",
                              '''
                              include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
                              conan_basic_setup(TARGETS)
                              ''')
        tools.replace_in_file("zzip/CMakeLists.txt", "ZLIB::ZLIB", "CONAN_PKG::zlib")
        tools.replace_in_file("zzip/CMakeLists.txt", "find_package ( ZLIB REQUIRED )", "")
        tools.replace_in_file("zzip/CMakeLists.txt", "add_library(libzzip ${libzzip_SRCS} )",
                              "add_library(libzzip STATIC ${libzzip_SRCS} )")
        tools.replace_in_file("zzipwrap/CMakeLists.txt", "ZLIB::ZLIB", "CONAN_PKG::zlib")
        tools.replace_in_file("zzipwrap/CMakeLists.txt", "pkg_search_module", "# pkg_search_module")
        tools.replace_in_file("zzipwrap/CMakeLists.txt", "find_package ( ZLIB REQUIRED )", "")
        tools.replace_in_file("zzipwrap/CMakeLists.txt", "add_library(libzzipwrap ${libzzipwrap_SRCS} )",
                              "add_library(libzzipwrap STATIC ${libzzipwrap_SRCS} )")

    def build(self):
        cmake = CMake(self)
        if os_info.is_windows:
            cmake.definitions['ZZIPCOMPAT'] = 'OFF'
        cmake.definitions['ZZIPTEST'] = 'OFF'
        cmake.definitions['ZZIPDOCS'] = 'OFF'
        cmake.definitions['ZZIPBINS'] = 'OFF'
        cmake.definitions['ZZIPSDL'] = 'OFF'
        cmake.definitions['BUILD_STATIC_LIBS'] = 'ON'
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
