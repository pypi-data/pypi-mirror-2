#!/usr/bin/env python

"""
jaraco.windows.message

Windows Messaging support
"""

# $Id: message.py 859 2009-02-24 19:10:23Z jaraco $

import ctypes
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, LPVOID
LRESULT = LPARAM

SendMessage = ctypes.windll.user32.SendMessageW
SendMessage.argtypes = (HWND, UINT, WPARAM, LPVOID)
SendMessage.restype = LRESULT

HWND_BROADCAST=0xFFFF
WM_SETTINGCHANGE=0x1A
