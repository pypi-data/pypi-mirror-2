# -*- coding: utf-8 -*-
# (c) 2008, Marcin Kasperski

from setuptools import setup, find_packages

version = '1.0.0'
long_description = open("README.txt").read()
classifiers = [
    "Programming Language :: Python",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    # TODO: Development Status, Environment, Topic
    ]

setup(name='mekk.greader',
      version=version,
      description="Simple wrapper for Google Reader API.",
      long_description=long_description,
      classifiers=classifiers,
      keywords='org',
      license='BSD',
      author='Marcin Kasperski',
      author_email='Marcin.Kasperski@mekk.waw.pl',
      url='http://bitbucket.org/Mekk/mekk.greader',
      package_dir={'':'src'},
      packages=find_packages('src', exclude=['ez_setup', 'examples', 'tests']),
      namespace_packages=['mekk'],
      test_suite = 'nose.collector',
      include_package_data = True,
      package_data = {
        'mekk' : [
            'README.txt',
            'LICENSE.txt',
            'doc/usage.txt',
            ],
        },
      zip_safe = True,
      install_requires=[
        'lxml', 'simplejson',
      ],
      tests_require=[
        'nose',
        ],
)
