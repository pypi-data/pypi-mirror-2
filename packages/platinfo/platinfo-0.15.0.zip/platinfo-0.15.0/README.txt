platinfo: A small library from getting information on the current platform
--------------------------------------------------------------------------

This module determines and returns standardized names for
platforms, where the "standard" is Trent Mick's reasoning :)
from experience building ActivePython on a fairly large number of
platforms.

The driving goal is to provide platform names that are:

- relatively short
- readable (as much as possible making matching the given name to an
  actually machine self-explanatory)
- be capable enough to produce all names needed to distinguish all
  platform-specific application builds
- generally safe for usage in filenames
- not ugly (e.g. "MSWin32" is ugly)

A simple usage example::

    >>> from platinfo import PlatInfo
    >>> pi = PlatInfo()
    >>> pi.os
    'macosx'
    >>> pi.arch
    'x86'
    >>> pi.name()
    'macosx-x86'

Currently this has fairly wide OS coverage (Windows, Linux, Mac, Solaris,
HP-UX, AIX, OpenBSD).
