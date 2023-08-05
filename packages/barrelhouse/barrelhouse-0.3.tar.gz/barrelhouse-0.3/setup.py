# -*- coding: utf-8 -*-
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup
import re

#from barrelhouse import __version__
version_rx = r"^__version__ = '(.*)'$"
version_pattern = re.compile(version_rx)


fd = open('barrelhouse/__init__.py')
try:
    for line in fd:
        m = version_pattern.match(line)
        if m:
            break
    else:
        raise Exception("couldn't find __version__")
finally:
    fd.close()

__version__ = m.group(1)

print "running setup for barrelhouse version %s" % __version__

requires = ['liberet']


setup(
    name="barrelhouse",
    version=__version__,
    description="WSGI OpenID authentication handler",
    author="Walter Wefft",
    author_email = "walterwefft@gmail.com",
    classifiers=["Development Status :: 1 - Planning",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: BSD License",
                "Programming Language :: Python",
                "Environment :: Web Environment",
                "Topic :: Internet :: WWW/HTTP :: WSGI",
                "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
                ],
    url="http://bitbucket.org/walterwefft/barrelhouse",
    license="BSD",
    download_url="http://pypi.python.org/packages/source/b/barrelhouse/barrelhouse-%s.tar.gz" % __version__,
    packages=[
        'barrelhouse',
        'barrelhouse.conf',
        ],
    install_requires=requires,
      )
    
