# -*- coding: utf-8 -*-
"""
These modules extend Rabbithole's base functionality.
All non-trivial commands are implemented as modules.
"""
from os.path import dirname, basename, isfile
import glob
__all__ = []

MODULES = glob.glob(dirname(__file__) + "/*.py")
for f in MODULES:
    fn = basename(f).rsplit('.', 1)[0]
    if isfile(f) and not fn.startswith('__') and not fn in __all__:
        __all__.append(fn)
