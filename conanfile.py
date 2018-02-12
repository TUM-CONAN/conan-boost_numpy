#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class BoostNumpyConan(ConanFile):
    name = "boost_numpy"
    version = "0.8"
    url = "https://github.com/ulricheck/conan-boost_numpy"
    description = "Boost Numpy extension (obsolete after boost 1.63.0"
    license = "https://github.com/someauthor/somelib/blob/master/LICENSES"
    requires = (
        "Boost/[>=1.59.0,<1.63.0]@camposs/stable",
        )

    exports_sources = ["LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"

    def configure(self):
        self.options['Boost'].without_python = False

    def source(self):
        self.run("git clone https://github.com/ndarray/Boost.NumPy.git sources")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.configure(source_dir="sources")
        cmake.build()
        cmake.install()

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="LICENSE")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.defines.append("HAVE_BOOST_NUMPY")
