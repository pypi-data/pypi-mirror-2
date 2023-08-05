#!/usr/bin/env python
from distutils.core import setup
import os
ginfo_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                          'dililatum', 'generalinformation.py')
execfile(ginfo_file) # Gives us a version and a version_text variables
bins = [x[2] for x in os.walk('bin')][0]
bins = [os.path.join('bin', x) for x in bins]

setup(
    name='Dililatum',
    version=version,
    author='Niels Serup',
    author_email='ns@metanohi.org',
    packages=['dililatum', 'dililatum.tools'],
    scripts=bins,
    url='http://metanohi.org/projects/dililatum/',
    license='LICENSE.txt',
    description='A quest system for simple RPGs',
    long_description=open('README.txt').read(),
    classifiers=["Development Status :: 3 - Alpha",
                 "Intended Audience :: End Users/Desktop",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: GNU General Public License (GPL)",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                 "Topic :: Games/Entertainment :: Role-Playing",
                 "Topic :: Software Development :: Libraries :: pygame",
                 "Topic :: Software Development :: Libraries :: Python Modules",
                 "Topic :: Utilities"
                 ],
    requires=['pygame', 'numpy']
)
