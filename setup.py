import re

from setuptools import setup

with open('wordsmith/__init__.py', 'r') as fd:
  version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version:
  raise RuntimeError('Could not locate version information')

setup(
  name = 'wordsmith',
  version = version,
  description = 'A wrapper around the Wordsmith API written in python',
  author = 'John Hegele - Automated Insights',
  packages = ['wordsmith'],
  package_dir = {'wordsmith' : 'wordsmith'},
  install_requires = ['requests', 'six'],
  classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.5'
  ]
)
