
# setup.py

from setuptools import setup, find_packages
import os

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

theFolder = "iscorpio/themes/redmaple"

setup(name='iscorpio.themes.redmaple',
      version=open(os.path.join(theFolder, "version.txt")).read().split('\n')[0],
      description="iscorpio readmaple Plone 3 theme",
      long_description=open(os.path.join(theFolder, "README.txt")).read() +
                       "\n" +
                       open(os.path.join(theFolder, "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Zope",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Zope Plone Python Theme Web',
      author='Sean Chen',
      author_email='sean.chen@leocorn.com',
      url='http://plonexp.leocorn.com/plonepm',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['iscorpio'],
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
