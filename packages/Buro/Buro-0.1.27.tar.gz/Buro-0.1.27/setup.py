import os
from setuptools import setup, find_packages

major = 0
minor = 1
build = 27
__version__ = ".".join(map(str, (major, minor, build)))


setup(
    name='Buro',
    version=__version__,
    url="http://buro.sourceinhabitants.com/",
    license='BSD',
    author='Thomas Pelletier',
    author_email='thomas@pelletier.im',
    description='A very simple Python-powered open-source web framework '
                'inspired by Flask, but following different design decisions',
    py_modules=['buro'],
    platforms='any',
    packages=  find_packages(exclude=['tests',]),
    install_requires = [
    'Jinja2>=2.5',
    'Werkzeug>=0.6.2',
    'setuptools',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite = 'nose.collector',
)