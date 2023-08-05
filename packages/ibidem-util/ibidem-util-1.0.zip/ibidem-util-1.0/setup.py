#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup

setup(
    name = "ibidem-util",
    version = "1.0",
    packages = ["ibidem", "ibidem.util"],
    namespace_packages = ["ibidem"],
    zip_safe = True,
    include_package_data = True,

    # Metadata
    author = "Morten Lied Johansen",
    author_email = "mortenjo@ifi.uio.no",
    description = "Ibidem utilities",
    license = "LGPL",
    keywords = "ibidem util",
    url = "http://ibidem.homeip.net/Misc/wiki/Utils"
)
