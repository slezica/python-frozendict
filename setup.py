from setuptools import setup

with open("README.rst") as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setup(
    name     = 'frozendict',
    version  = '1.3',
    url      = 'https://github.com/slezica/python-frozendict',

    author       = 'Santiago Lezica',
    author_email = 'slezica89@gmail.com',

    packages = ['frozendict'],
    license  = 'MIT License',

    description      = 'An immutable dictionary',
    long_description=LONG_DESCRIPTION,

    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
)
