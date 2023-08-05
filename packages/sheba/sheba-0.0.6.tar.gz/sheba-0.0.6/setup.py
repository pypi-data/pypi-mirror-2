# Copyright 2010 - Paul J. Davis <paul.joseph.davis@gmail.com>
#
# This file is part of the Sheba SQL project released
# under the MIT license.

import os
from setuptools import setup

def get_readme():
    fname = os.path.join(os.path.dirname(__file__), "README.rst")
    with open(fname) as handle:
        return handle.read()

setup(
    name="sheba",
    version="0.0.6",
    description="Sheba SQL - SQL for normal people.",
    long_description=get_readme(),

    author="Paul J. Davis",
    author_email="paul.joseph.davis@gmail.com",
    url="http://github.com/davisp/sheba",
    
    packages=["sheba"],
    
    install_requires=["pyyaml", "mako"],
    test_suite="nose.collector",
)
