#!/usr/bin/env python
"""
Sub-Package STDLIB.IO.SOCKET of Package PLIB
Copyright (C) 2008-2010 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This sub-package includes classes for handling socket
I/O channels. See the docstring for the parent package,
``plib.stdlib.io``, for information on how this package
fits into the overall I/O package structure.
"""

import os
import glob

from plib.utils import ModuleProxy

from _socket import *

def module_helper(modname):
    def f():
        result = __import__(modname, globals(), locals())
        return getattr(result, modname)
    f.__name__ = "%s_helper" % modname
    return f

module_dict = {}
for pathname in __path__:
    for filename in glob.glob(os.path.join(pathname, "*.py")):
        modname = os.path.splitext(os.path.basename(filename))[0]
        if modname not in ("__init__", "_socket"):
            module_dict[modname] = module_helper(modname)

ModuleProxy(__name__, module_dict)

# Now clean up our namespace
del os, glob, ModuleProxy, module_helper, module_dict, \
    pathname, filename, modname
