# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='dae',
    version='0.1',
    author='Daniel Skinner',
    author_email='dasacc22@gmail.com',
    url='http://dae.dasa.cc',
    license = "MIT License",
    packages = ["dae"],
    requires = ["cherrypy"],
    description='da Engine that provides toolbox and namespace extensions for writing modular cherrypy applications.',
    long_description = """\
Follow development at http://github.com/dasacc22/dae
    """,
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Environment :: Web Environment",
        ]
    )
