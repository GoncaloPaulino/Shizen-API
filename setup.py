# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "shizen"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="Shizen API",
    author_email="grpaulino8@gmail.com",
    url="",
    keywords=["Swagger", "Shizen API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['shizen=shizen.__main__:main']},
    long_description="""\
    Shizen
    """
)
