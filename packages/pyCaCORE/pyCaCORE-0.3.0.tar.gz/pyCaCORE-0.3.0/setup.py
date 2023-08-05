#!/usr/bin/env python

from setuptools import setup

setup(name='pyCaCORE',
      version='0.3.0',
      description='caCORE Python API Generator',
      long_description='Python API generator for caCORE-like systems',
      license='caBIO Software License',
      platforms='All',
      author='Konrad Rokicki',
      author_email='rokickik@mail.nih.gov',
      url='http://cabioapi.nci.nih.gov/',
      packages=[
            'cabig',
            'cabig.cacore',
            'cabig.cacore.generate',
            'cabig.cacore.ws',
      ],
      include_package_data = True,
      namespace_packages = ['cabig'],
      install_requires = [ 'setuptools>=0.6c3', 'ZSI==2.1_a1' ],
      dependency_links = [
            'https://gforge.nci.nih.gov/frs/?group_id=525'
      ],
      entry_points = {
            'console_scripts': [
            'cacore2py = cabig.cacore.generate.commands:cacore2py',
         ],
      },
)
