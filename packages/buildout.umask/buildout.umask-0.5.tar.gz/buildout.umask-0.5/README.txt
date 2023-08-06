Introduction
============

This extension allows better control over the initial permissions of
files created by buildout by allowing the umask used by the buildout
script to be specified in the configuration file.

Because of bug 180705 of zc.buildout, this doesn't work for scripts
installed by buildout.

This doesn't affect the umask of other scripts in the buildout, unless
they set their own the umask of the user running them will be used,
e.g.: ZEO/Zope might still make var/filestore/Datafile.fs world
readable if your umask is 022.

Usage
=====

  [buildout]
  extensions = buildout.umask
  umask = 027

The `umask` parameter can be specified using any of Python conventions
for numeric literals of binary, octal, decimal or hexadecimal
radix. If any of them is used and a `0` is the first digit, octal is
assumed as well.

Questions
=========

The code is quite simple, take a glimpse.

Bugs
====

https://bugs.launchpad.net/buildout.umask
