from setuptools import setup, find_packages
import sys, os

version = '1.0b1'

setup(name='benchmaster',
      version=version,
      description="Tools for running and automating distributed loadtests with Funkload",
      long_description=open('README.txt').read() + '\n\n' +
                       open('CHANGES.txt').read() + '\n\n',
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='funkload clustered load testing',
      author='Julian Coyne and Martin Aspeli',
      author_email='optilude@gmail.com',
      url='http://pypi.python.org/pypi/funkload-bench',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'funkload>=0.12',
          'pssh>=2.1.1',
      ],
      entry_points= {
        'console_scripts': [
                'bench-master = benchmaster.master:main',
                'bench-node = benchmaster.node:main',
            ],
      },
      )
