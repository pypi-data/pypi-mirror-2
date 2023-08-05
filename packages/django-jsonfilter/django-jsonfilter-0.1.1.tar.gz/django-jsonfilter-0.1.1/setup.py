#!/usr/bin/env python

from distutils.core import setup

setup(
    name='django-jsonfilter',
    version='0.1.1',
    description='Django json datadump object filtering',
    long_description=open('README.rst').read(),
    author='WiswauD',
    author_email='esj@wwd.ca',
    url='http://bitbucket.org/wiswaud/django-jsonfilter',
    install_requires=[],
    setup_requires=[],
    requires=[],
    license='License :: OSI Approved :: GNU General Public License (GPL)',
    packages=['jsonfilter'],
    package_data={},
    scripts=['scripts/jsonfilter'],
    zip_safe=False,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers', 
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: System :: Archiving :: Backup'
    ]
)
