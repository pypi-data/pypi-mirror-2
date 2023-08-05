from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='eximloganalyzer',
      version=version,
      description="Command line script to parse exim logs",
      long_description="""\
Command line script to parse exim logs and returns a detailed report about log statistics""",
      classifiers=[
        "Topic :: Communications :: Email",
        "Topic :: Internet :: Log Analysis",
      ],
      keywords='exim log analyzer',
      author='Joe Topjian',
      author_email='joe@terrarum.net',
      url='http://terrarum.net',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
      ],
      entry_points = {
          'console_scripts': [
                'eximloganalyzer = eximloganalyzer.cli:main'
          ]
      },
      )
