#!/usr/bin/env python
# Copyright (c) 2007 Qtrac Ltd. All rights reserved.
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

import os
from setuptools import setup

setup(name='cronwrap',
      version = '1.0',
      author="amix the lucky stiff",
      author_email="amix@amix.dk",
      url="http://www.amix.dk/",
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],

      install_requires=[
          'argparse>=1.1'
      ],

      scripts=['scripts/cronwrap'],
      packages=[''],
      platforms=["Any"],
      license="BSD",
      keywords='cron wrapper crontab cronjob',
      description="A cron wrapper that wraps cron jobs and enables better error reproting and command timeouts.",
      long_description="""\
cronwrap
---------------

A cron wrapper that wraps cron jobs and enables better error reproting and command timeouts.


Example
-------

Basic example of usage::

    #Will send out a timeout alert to cron@my_domain.com:
    $ cronwrap -c "sleep 2" -t "1s" -e cron@my_domain.com

    #Will send out an error alert to cron@my_domain.com:
    $ cronwrap -c "blah" -t "1s" -e cron@my_domain.com

    #Will not send any reports:
    $ cronwrap -c "ls" -e cron@my_domain.com

    #Will send a succefull report to cron@my_domain.com:
    $ cronwrap -c "ls" -e cron@my_domain.com -v
""")
