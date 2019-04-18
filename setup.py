from setuptools import setup

setup(
    name     = 'frozendict',
    version  = '1.2',
    url      = 'https://github.com/slezica/python-frozendict',

    author       = 'Santiago Lezica',
    author_email = 'slezica89@gmail.com',

    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    packages = ['frozendict'],
    license  = 'MIT License',

    description      = 'An immutable dictionary',
    long_description = open('README.rst').read()
)
