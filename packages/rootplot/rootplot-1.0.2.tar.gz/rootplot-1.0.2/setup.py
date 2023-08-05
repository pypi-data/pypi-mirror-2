try:
    import setuptools
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
from setuptools import setup, find_packages

import sys, os

setup(
    name         = 'rootplot',
    version      = '1.0.2',
    description  = 'Tools for use with the ROOT Data Analysis Framework',
    long_description = ('Includes command-line scripts for plotting '
                        'images from ROOT histograms and generating '
                        'histograms from ntuples; also contains the '
                        'root2matplotlib library for plotting ROOT histograms '
                        'with matplotlib.'),
    author       = 'Jeff Klukas',
    author_email = 'klukas@wisc.edu',
    url          = 'http://packages.python.org/rootplot/',
    download_url = '',
    packages = find_packages('lib'),
    package_dir = {'': 'lib'},
    include_package_data=True,
    entry_points = {
        'console_scripts': [
            'rootplot = rootplot_scripts.rootplot:main',
            'tree2hists = rootplot_scripts.tree2hists:main'
            ]
        },
    classifiers  = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Utilities',
        ],
    )
