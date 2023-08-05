from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='CustomizeMe',
      version='0.0',
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='nsi',
      author_email='nsi@iff.edu.br',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points = {
            'console_scripts': [
                'customizeme = customizeme.servidor:iniciar',
      ],}
      )

