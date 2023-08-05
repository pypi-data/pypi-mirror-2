#!/usr/bin/env python

try:
    from setuptools import setup
except:
    from distutils.core import setup


def infoFromModule(path):
    ns = {}
    execfile(path, ns)
    return dict(
            name = ns["version"].package,
            version = ns["version"].short(),
            )


setup(
    packages = ["vtwt",],
    scripts = ["bin/vtwt",],

    description = "Ver's Twitter CLI",
    long_description = open("README").read(),

    url = "http://github.com/olix0r/vtwt",
    download_url = "http://pypi.python.org/pypi/vtwt",

    author = "Oliver Gould", author_email = "ver@olix0r.net",
    maintainer = "Oliver Gould", maintainer_email = "ver@olix0r.net",

    license = "MIT",
    classifiers = [
        "Framework :: Twisted",
        "License :: OSI Approved :: MIT License",
        ],

    provides = ["vtwt",],
    requires = [
        "twittytwister",
        "twisted",
        "oauth",
        "pendrell(>=0.2.2)",
        "jersey(>=0.1.2)",
        ],

    **infoFromModule("vtwt/_version.py")
    )


