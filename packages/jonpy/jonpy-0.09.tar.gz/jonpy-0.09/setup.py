#!/usr/bin/env python

# $Id: setup.py,v 3c2581c6cdaf 2010/03/22 15:04:18 jon $

from distutils.core import setup

setup(name="jonpy",
      version="0.09",
      description="Jon's Python modules",
      author="Jon Ribbens",
      author_email="jon+jonpy@unequivocal.co.uk",
      url="http://jonpy.sourceforge.net/",
      packages=['jon', 'jon.wt']
)
