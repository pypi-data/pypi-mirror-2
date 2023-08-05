# Copyright: Enfold Systems, LLC

# Setup script for the 'enfold.gcache' package.

import sys, os
from setuptools import setup, find_packages

setup(
    name="enfold.gcache",
    version="1.0.0",
    author='Enfold Systems',
    author_email='info@enfoldsystems.com',
    url='http://www.enfoldsystems.com',
    classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      ],
    keywords='cache caching',
    license='LGPL',
    packages = find_packages('src', exclude=['examples', 'tests']),
    package_dir = {'': 'src'},
    namespace_packages=['enfold'],
    zip_safe=False,
    install_requires=[
          'setuptools',
          'python-dateutil'
      ],
    include_package_data = True,    # include everything in source control
)
