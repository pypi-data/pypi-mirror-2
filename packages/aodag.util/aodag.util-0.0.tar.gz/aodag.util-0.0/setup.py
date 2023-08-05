from setuptools import setup, find_packages
import sys, os

version = '0.0'

readme = os.path.join(os.path.dirname(__file__), 'README')
long_description = open(readme).read()

setup(name='aodag.util',
      version=version,
      description="command utilities for python developer",
      long_description=long_description,
      classifiers=[
      "Development Status :: 3 - Alpha",
      "Programming Language :: Python",
      "Topic :: Software Development",
      "Topic :: Utilities",
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Atsushi Odagiri',
      author_email='aodagx@gmail.com',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      mkpkg = aodag.util.mkpkg:main
      """,
      )
