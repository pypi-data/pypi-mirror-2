# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = open('VERSION', 'r').read().replace('\n', '')

setup(
    name='piwik',
    version=VERSION,
    description='Access Piwik in python',
    long_description=open('README.rst').read(),

    author='François de Metz',
    author_email='francois@2metz.fr',
    url='http://forge.2metz.fr/p/python-piwik/',
    
    license='BSD',
    packages = find_packages(),
    package_data = {'piwik': ['django/templates/admin/piwik/*.html']},
    
    install_requires = [
        'simplejson'
    ],
    extras_require = {
        'django':  ["Django>=1.0"],
    },

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Topic :: Internet :: Log Analysis',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ],
)
