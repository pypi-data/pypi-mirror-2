"""
tipfy.ext.auth
==============

This extension provides authentication utilities for
`tipfy <http://www.tipfy.org/>`_. It allows users to authenticate using own
users, OpenId, Oauth, Facebook, Google, FriendFeed, Twitter or App Engine's
built-in users API.

Try a multi-authentication working example at `http://tipfy-auth.appspot.com/ <http://tipfy-auth.appspot.com/>`_.

Links
-----
* `Documentation <http://www.tipfy.org/wiki/extensions/auth/>`_
* `Source Code Repository <http://code.google.com/p/tipfy-ext-auth/>`_
* `Issue Tracker <http://code.google.com/p/tipfy-ext-auth/issues/list>`_

About tipfy
-----------
* `Home page <http://www.tipfy.org/>`_
* `Extension list <http://www.tipfy.org/wiki/extensions/>`_
* `Discussion Group <http://groups.google.com/group/tipfy>`_
"""
from setuptools import setup

setup(
    name = 'tipfy.ext.auth',
    version = '0.6.4',
    license = 'BSD',
    url = 'http://www.tipfy.org/',
    description = 'Authentication extension for tipfy',
    long_description = __doc__,
    author = 'Rodrigo Moraes',
    author_email = 'rodrigo.moraes@gmail.com',
    zip_safe = False,
    platforms = 'any',
    packages = [
        'tipfy',
        'tipfy.ext',
        'tipfy.ext.auth',
    ],
    namespace_packages = [
        'tipfy',
        'tipfy.ext',
        'tipfy.ext.auth',
    ],
    include_package_data = True,
    install_requires = [
        'tipfy',
        'tipfy.ext.session',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
