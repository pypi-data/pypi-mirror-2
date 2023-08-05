# -*- coding: utf-8 -*-
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "html2data",
    version = "0.2",
    author = "Daniel Perez Rada",
    author_email = "daniel@zappedy.com",
    description = ("A simple way to transform a HTML file or URL to structured data."),
    license = "BSD",
    keywords = "html2data html data xpath crawler transform",
    url = "http://packages.python.org/html2data",
    packages=['html2data', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
    ],
)
