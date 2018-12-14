from conans import ConanFile, CMake, tools


class LibzzipConan(ConanFile):
    name = "libZZIP"
    version = "0.13.63"
    license = "GNU"
    author = "Edgar (Edgar@AnotherFoxGuy.com)"
    url = "https://github.com/AnotherFoxGuy/conan-ZZIPlib"
    description = "The zziplib provides read access to zipped files in a zip-archive, using compression based solely on free algorithms provided by zlib."
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_paths"
    requires = "zlib/1.2.11@conan/stable"

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/paroj/ZZIPlib.git")
        tools.replace_in_file("CMakeLists.txt", "# Zlib library needed","include(${CMAKE_BINARY_DIR}/conan_paths.cmake)")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
