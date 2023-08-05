#!/usr/bin/env python

# $Id: __init__.py 769 2009-02-01 01:50:23Z jaraco $

"""
jaraco.windows

A lightweight wrapper to provide a pythonic API to the Windows Platform.

This package attempts to provide interfaces similar or compatible
with Mark Hammond's pywin32 library, but avoids the use of extension
modules by utilizing ctypes.
"""

__all__ = ('net')

import net