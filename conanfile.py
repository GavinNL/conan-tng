from conans import ConanFile, tools, CMake
import os

#
# This is the conan recipe for libcci. This recipe is for the older
# version of cci which does not use Cmake or Git. The source is
# downloaded from ftp.
#
#
# This will need to be modified for the newer versions which use git
#
class gromacsTng(ConanFile):
    name        = "tng"
    version     = "1.8.2"
    sha256      = "242b2ecab5018a42ba80d8df58528ecb9edf419caa671eca4864234672bf025d"

    homepage    = "http://www.gromacs.org/"
    url         = "https://github.com/GavinNL/conan-tng"
    description = "External GROMACS library for loading tng files."
    license     = "BSD"

    generators  = "cmake"

    options = { "shared": [True, False],
                "fPIC": [True, False]
                }

    default_options = { 'shared': True,
                        'fPIC': True
                        }

    settings = "os", "compiler", "build_type", "arch"
    build_policy = "missing"


    filename = "tng-{0}.tar.gz".format(version)
    url_file_path = "https://github.com/gromacs/tng/archive/v{0}.tar.gz".format(version)

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"




    requires = (
        "zlib/1.2.11@conan/stable"
    )

    def configure(self):
        #pass
        del self.settings.compiler.libcxx

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        print("Downloading: " + self.url_file_path)
        tools.get(self.url_file_path, sha256=self.sha256)
        os.rename("tng-{0}".format(self.version), self._source_subfolder)


    def _configure_cmake(self):
        cmake = CMake(self)

        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["TNG_BUILD_OWN_ZLIB"] = False

        cmake.configure(build_folder=self._build_subfolder, source_folder=self._source_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        #self.copy(pattern="FindDecaf.cmake", dst="", src=os.path.join(self._source_subfolder,"cmake"))
        cmake = self._configure_cmake()
        cmake.install()
#    def package(self):
#        self.copy("*COPYING*", dst="licenses")

    def package_info(self):
        self.cpp_info.libs = ["tng_io"]
        #self.env_info.ALSA_CONFIG_DIR = os.path.join(self.package_folder, "share", "alsa")
