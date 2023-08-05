#!/usr/bin/env python

from distutils.core import setup

setup(name='django-ifnav-templatetag',
      version='1.1',
      description='ifnav template tag for django',
      keywords='django if navigation template tag regular expression regex',
      author='Michael P. Jung',
      author_email='mpjung@terreon.de',
      url='http://bitbucket.org/mp/django-ifnav-templatetag',
      packages=['ifnav_templatetag', 'ifnav_templatetag.templatetags'],
      license='BSD',
     )
