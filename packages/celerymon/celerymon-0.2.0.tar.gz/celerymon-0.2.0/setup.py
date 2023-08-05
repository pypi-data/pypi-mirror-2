#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import sys
import os
import platform

try:
    from setuptools import setup, find_packages, Command
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages, Command

import celerymonitor as distmeta


class RunTests(Command):
    description = "Run the test suite from the testproj dir."

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        this_dir = os.getcwd()
        testproj_dir = os.path.join(this_dir, "testproj")
        os.chdir(testproj_dir)
        sys.path.append(testproj_dir)
        from django.core.management import execute_manager
        os.environ["DJANGO_SETTINGS_MODULE"] = os.environ.get(
                        "DJANGO_SETTINGS_MODULE", "settings")
        settings_file = os.environ["DJANGO_SETTINGS_MODULE"]
        settings_mod = __import__(settings_file, {}, {}, [''])
        execute_manager(settings_mod, argv=[
            __file__, "test"])
        os.chdir(this_dir)

install_requires = [
    "celery",
    "tornado"
]

# python-daemon doesn't run on windows, so check current platform
if platform.system() == "Windows":
    print("""
    ***WARNING***
    I see you are using windows. You will not be able to run celerymon
    in daemon mode with the --detach parameter.""")
else:
    install_requires.append("python-daemon>=1.4.8")

if os.path.exists("README.rst"):
    long_description = codecs.open("README.rst", "r", "utf-8").read()
else:
    long_description = "See http://pypi.python.org/pypi/celerymon"


setup(
    name='celerymon',
    version=distmeta.__version__,
    description=distmeta.__doc__,
    author=distmeta.__author__,
    author_email=distmeta.__contact__,
    url=distmeta.__homepage__,
    platforms=["any"],
    license="BSD",
    packages=find_packages(exclude=['ez_setup']),
    scripts=["bin/celerymon"],
    zip_safe=False,
    install_requires=install_requires,
    cmdclass = {"test": RunTests},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Distributed Computing",
    ],
    entrypoints={
        "console_scripts": [
            "celerymon = celerymonitor.bin.celerymond:main",
        ],
    },
    long_description=long_description,
)
