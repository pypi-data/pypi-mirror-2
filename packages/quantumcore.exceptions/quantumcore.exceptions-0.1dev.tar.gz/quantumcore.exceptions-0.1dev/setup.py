from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='quantumcore.exceptions',
      version=version,
      description="Common exceptions for thw QuantumCore libraries.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='exceptions quantumcore library cms',
      author='Christian Scholz',
      author_email='cs@comlounge.net',
      url='http://quantumcore.org',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quantumcore'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
