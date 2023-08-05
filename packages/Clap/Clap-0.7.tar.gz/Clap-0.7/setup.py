"""
====
Clap
====
Clap is a library that makes it easy to write powerful, flexible command-line
applications in Python. It is inspired by Denis Defreyne's `Cri`_.

* Get the source code at `Bitbucket`_
* Read the `documentation`_

.. _Bitbucket: http://bitbucket.org/leafstorm/clap/
.. _Cri: http://projects.stoneship.org/hg/cri
.. _documentation: http://packages.python.org/Clap/
"""
from distutils.core import setup

setup(
    name='Clap',
    version='0.7',
    description="Command Line Applications for Python",
    long_description=__doc__,
    author='Matthew "LeafStorm" Frazier',
    author_email='leafstormrush@gmail.com',
    package_dir={'': 'lib'},
    packages=['clap'],
    license='MIT/X11'
)
