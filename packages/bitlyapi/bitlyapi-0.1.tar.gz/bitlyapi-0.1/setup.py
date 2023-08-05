import os, sys
from setuptools import setup

version = '0.1'

install_requires = ['setuptools']
if sys.version_info < (2, 6):
    install_requires.append('simplejson')

setup(
    name='bitlyapi',
    version=version,
    description='A thin wrapper for the bit.ly REST API',
    long_description='\n\n'.join([
        open("README.rst").read(),
        open("CHANGES.rst").read(),
    ]),
    url = 'http://github.com/hellp/bitlyapi',
    license = 'BSD',
    author='Fabian Neumann',
    author_email='fn@sturzbach.de',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['bitlyapi'],
    scripts=['scripts/bitly',],
    install_requires=install_requires,
)
