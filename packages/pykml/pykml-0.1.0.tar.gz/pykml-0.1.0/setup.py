from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(
    name='pykml',
    version=version,
    packages=['pykml',],
    package_dir={'': 'src'},
    package_data={
        'pykml': [
            'schemas/*.xsd',
            'test/*.py',
            'test/testfiles/*.kml',
            'test/testfiles/google_kml_developers_guide/*.kml',
            'test/testfiles/google_kml_tutorial/*.kml',
        ],
    },
    install_requires=[
        'setuptools',
        'lxml>=2.2.6',
    ],
    tests_require=['nose'],
    #test_suite='nose.collector',
    description="Python KML library",
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics :: Viewers',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='kml',
    author='Tyler Erickson',
    author_email='tylerickson@gmail.com',
    url='http://pypi.python.org/pypi/pykml',
    license='BSD',
    long_description="""\
=========
PyKML
=========
PyKML is a Python package for parsing and authoring KML documents. It is based
on the lxml.objectify API (http://codespeak.net/lxml/objectify.html) which
provides Pythonic access to XML documents.

See the Package Documentation for information on installation and usage.
""",
)
