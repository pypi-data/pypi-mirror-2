# -*- coding: UTF-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (2, 4):
    raise SystemExit("Python 2.4 or later is required")

# import meta data (version, author etc.)
execfile(os.path.join("korgws", "release.py"))

setup(
    name="korgwslib",
    description=description,
    long_description=long_description,
    version=version,
    author=author,
    author_email=email,
    url=url,
    download_url=download_url,
    license=license,
    zip_safe=False,
    packages=['korgws', 'korgws.scripts'],
    entry_points = """
    [console_scripts]
        wslistbanks = korgws.scripts.listbanks:main
    """,
    tests_require = ["nose"],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    test_suite = 'nose.collector',
)
