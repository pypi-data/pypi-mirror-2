#!/usr/bin/env python
import os
from setuptools import *

import aptdaemon

readme = open(os.path.join(os.path.dirname(__file__), "README")).read()

# The transaction class has got it's own gettext translation
# Don't set bug-contact in setup.cfg since p-d-u-e will overwrite
# XGETTEXT_ARGS otherwise.
os.environ["XGETTEXT_ARGS"] = "--keyword=self.trans.gettext"

setup(name="aptdaemon",
      version=aptdaemon.__version__,
      description="DBus driven daemon for APT",
      long_description=readme,
      author="Sebastian Heinlein",
      author_email="devel@glatzor.de",
      packages=["aptdaemon"],
      scripts=["aptd", "aptdcon"],
      test_suite="nose.collector",
      license="GNU LGPL",
      keywords="apt package manager deb dbus d-bus debian ubuntu dpkg",
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: System Administrators",
                   "License :: OSI Approved :: GNU Library or Lesser General " \
                       "Public License (LGPL)",
                   "Programming Language :: Python :: 2.6",
                   "Topic :: System :: Systems Administration",
                   "Topic :: System :: Software Distribution"],
      url="http://launchpad.net/sessioninstaller",
      data_files=[("../etc/dbus-1/system.d/",
                   ["data/org.debian.apt.conf"]),
                  ("../etc/apt/apt.conf.d/",
                   ["data/20dbus"]),
                  ("share/dbus-1/system-services/",
                   ["data/org.debian.apt.service"]),
                  ("share/man/man1",
                   ["doc/aptd.1", "doc/aptdcon.1"]),
                  ("share/man/man7",
                   ["doc/org.debian.apt.7",
                    "doc/org.debian.apt.transaction.7"])],
      platforms="posix")
