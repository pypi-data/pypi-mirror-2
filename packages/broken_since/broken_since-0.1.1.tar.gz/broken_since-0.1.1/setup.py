#!/usr/bin/env python

from setuptools import setup, find_packages
from broken_since import __version__, __doc__

setup(name='broken_since',
      version=__version__,
      author='Francis Pieraut',
      packages = find_packages(),
      description = __doc__,
      entry_points = {
          'nose.plugins.0.10': [
              'broken_since = broken_since.broken_since:BrokenSinceDetail'
              ]
          },
      )
