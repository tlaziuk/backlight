#! /usr/bin/env python3
import py_compile
import os
py_compile.compile("backlight.py", cfile="backlight", doraise=True)
os.chmod("backlight", 0o555)
