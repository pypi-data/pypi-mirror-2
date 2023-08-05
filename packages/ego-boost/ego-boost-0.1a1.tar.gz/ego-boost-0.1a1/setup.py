#!/usr/bin/python
from setuptools import setup

setup(name='ego-boost',
    version='0.1a1',
    description="Package to track you module's download statistics",
    long_description=open('README').read(),
    author='Sebastian Rahlf',
    author_email='basti at redtoad dot de',
    license='MIT', 
    url='http://pypi.python.org/pypi/egoboost',
    packages=['egoboost'],
    scripts=['ego-boost'],
    install_requires=[
        'simplejson',
        'lxml'
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: System :: Logging', 
    ]
)
