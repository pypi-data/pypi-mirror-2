#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import django_dumpdb


def get_long_description():
    return open('README').read()

setup(
    name='django-dumpdb',
    version=str(django_dumpdb.__version__),
    description='A better, faster, stronger alternative for manage.py dumpdata',
    long_description=get_long_description(),
    author='Andrey Golovizin',
    author_email='golovizin@gmail.com',
    url='http://code.google.com/p/django-dumpdb/',
    packages=['django_dumpdb', 'testproject', 'testproject.testmodels'],
    include_package_data=True,
    license='MIT',
    platforms=['platform-independent'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Topic :: Utilities',
    ],
)
