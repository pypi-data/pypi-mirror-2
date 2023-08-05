# -*- coding: utf-8 -*-
"""
tipfy.ext.jsonrpc
~~~~~~~~~~~~~~~~~

Tipfy extension to create JSON-RPC services. It provides a RequestHandler
mixin to easily set a JSON-RPC service.

Documentation is available at
`http://www.tipfy.org/wiki/extensions/jsonrpc/ <http://www.tipfy.org/wiki/extensions/jsonrpc/>`_.

Links
-----
* `Tipfy <http://www.tipfy.org/>`_
* `API Documentation <http://www.tipfy.org/docs/>`_
* `Wiki <http://www.tipfy.org/wiki/>`_
* `Discussion Group <http://groups.google.com/group/tipfy>`_
* `Issue Tracker <http://code.google.com/p/tipfy-ext-jsonrpc/issues/list>`_
* `Source Code Repository <http://code.google.com/p/tipfy-ext-jsonrpc/>`_
"""
from setuptools import setup

setup(
    name = 'tipfy.ext.jsonrpc',
    version = '0.1',
    license = 'Apache',
    url = 'http://www.tipfy.org/',
    description = 'Tipfy extension to create JSON-RPC services',
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
        'lovely.jsonrpc',
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