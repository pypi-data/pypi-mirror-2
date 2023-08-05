from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='collective.blueprint.base',
      version=version,
      description=("Some core transmogrifier blueprints and base classes"), 
      long_description=open(
          os.path.join("README.txt")).read() + "\n" +
      open(os.path.join("collective", "blueprint", "base",
                        "README.txt")).read() + "\n" +
      open(os.path.join("collective", "blueprint", "base",
                        "delete", "README.txt")).read() + "\n" +
      open(os.path.join("collective", "blueprint", "base",
                        "configsource", "README.txt")).read() + "\n" +
      open(os.path.join("collective", "blueprint", "base",
                        "keysplitter", "README.txt")).read() + "\n" +
      open(os.path.join("collective", "blueprint", "base",
                        "recurser", "README.txt")).read() + "\n" +
      open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: "
          "Python Modules",
        ],
      keywords='',
      author='Ross Patterson',
      author_email='me@rpatterson.net',
      url='http://pypi.python.org/pypi/collective.blueprint.base',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.blueprint'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'collective.transmogrifier',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
