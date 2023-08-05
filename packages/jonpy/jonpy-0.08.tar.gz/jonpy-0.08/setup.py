#!/usr/bin/env python

# $Id: setup.py,v 1.11 2010/03/17 19:13:14 jribbens Exp $

from distutils.core import setup

setup(name="jonpy",
      version="0.08",
      description="Jon's Python modules",
      author="Jon Ribbens",
      author_email="jon+jonpy@unequivocal.co.uk",
      url="http://jonpy.sourceforge.net/",
      packages=['jon', 'jon.wt']
)
