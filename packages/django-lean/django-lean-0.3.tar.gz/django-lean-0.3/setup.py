# -*- coding: utf-8 -*-
"""A/B Testing for Django

django-lean allows you to perform split-test experiments on your users.
In brief, this involves exposing 50% of your users to one implementation 
and 50% to another, then comparing the performance of these two groups 
with regards to certain metrics.
"""

from distutils.core import setup

description, long_description = __doc__.split('\n\n', 1)

setup(
    name='django-lean',
    version='0.3',
    author='Akoha, Inc.',
    author_email='django-lean@akoha.com',
    description=('A framework for performing and analyzing split-test ' +
                 'experiments in Django applications.'),
    long_description=('django-lean aims to be a collection of tools for ' +
                      'Lean Startups using the Django platform. Currently ' +
                      'it provides a framework for implementing split-test ' +
                      'experiments in JavaScript, Python, or Django template ' +
                      'code along with administrative views for analyzing ' +
                      'the results of those experiments.'),
    license='BSD',
    platforms=['any'],
    url='http://bitbucket.org/akoha/django-lean/wiki/Home',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=['experiments',
        'experiments.management',
        'experiments.management.commands',
        'experiments.templatetags',
        'experiments.migrations',
        'experiments.tests',
        'experiments.tests.data',
        ],
    package_data={
       'experiments': ['templates/experiments/*.html',
                       'templates/experiments/include/*.html',
                       'templates/experiments/include/*.js'],
       'experiments.tests': ['data/*.json']
       },
    install_requires=['django >= 1.0', 'BeautifulSoup', 'mox'],
    )
