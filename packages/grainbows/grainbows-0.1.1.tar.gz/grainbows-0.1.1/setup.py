# -*- coding: utf-8 -
#
# This file is part of grainbow released under the MIT license. 
# See the NOTICE for more information.


import os
from setuptools import setup, find_packages

from grainbows import __version__

setup(
    name = 'grainbows',
    version = __version__,

    description = 'WSGI HTTP Server for UNIX',
    long_description = file(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),
    author = 'Benoit Chesneau',
    author_email = 'benoitc@e-engura.com',
    license = 'MIT',
    url = 'http://github.com/benoitc/grainbows',

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe = False,
    packages = find_packages(exclude=['examples', 'tests']),
    include_package_data = True,
        
    require = [
        'gunicorn>=0.6.5',
    ],
    entry_points="""
    
    [console_scripts]
    grainbows=grainbows.main:run
    grainbows_django=grainbows.main:run_django
    grainbows_paster=grainbows.main:run_paster
    
    [paste.server_runner]
    main=grainbows.main:paste_server
    """,
    test_suite = 'nose.collector',
)