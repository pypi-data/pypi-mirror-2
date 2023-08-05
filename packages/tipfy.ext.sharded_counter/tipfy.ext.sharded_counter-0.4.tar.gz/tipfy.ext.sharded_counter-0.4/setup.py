"""
tipfy.ext.sharded_counter
=========================

A general purpose sharded counter implementation for App Engine, integrated
with `tipfy <http://www.tipfy.org/>`_.

Links
-----
* `Documentation <http://www.tipfy.org/wiki/extensions/shardedcounter/>`_
* `Source Code Repository <http://code.google.com/p/tipfy-ext-sharded-counter/>`_
* `Issue Tracker <http://code.google.com/p/tipfy-ext-sharded-counter/issues/list>`_

About tipfy
-----------
* `Home page <http://www.tipfy.org/>`_
* `Extension list <http://www.tipfy.org/wiki/extensions/>`_
* `Discussion Group <http://groups.google.com/group/tipfy>`_
"""
from setuptools import setup

setup(
    name = 'tipfy.ext.sharded_counter',
    version = '0.4',
    license = 'Apache',
    url = 'http://www.tipfy.org/',
    description = 'A general purpose sharded counter implementation for App Engine',
    long_description = __doc__,
    author = 'Rodrigo Moraes',
    author_email = 'rodrigo.moraes@gmail.com',
    zip_safe = False,
    platforms = 'any',
    packages = [
        'tipfy',
        'tipfy.ext',
    ],
    namespace_packages = [
        'tipfy',
        'tipfy.ext',
    ],
    include_package_data = True,
    install_requires = [
        'tipfy',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)