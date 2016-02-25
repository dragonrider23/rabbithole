from os.path import dirname, basename, isfile
import glob
__all__ = []

modules = glob.glob(dirname(__file__)+"/*.py")
modules.extend(glob.glob(dirname(__file__)+"/*.pyc"))
modules.extend(glob.glob(dirname(__file__)+"/*.pyo"))
for f in modules:
    fn = basename(f)
    fn = fn.rsplit('.', 1)[0]
    if isfile(f) and not fn.startswith('__') and not fn in __all__:
        __all__.append(fn)
