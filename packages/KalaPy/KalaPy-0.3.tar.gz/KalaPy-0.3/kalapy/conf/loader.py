"""
kalapy.conf.loader
~~~~~~~~~~~~~~~~~~

This module defines a Loader class to automatically load all the installed
packages given in settings.INSTALLED_PACKAGES.

:copyright: (c) 2010 Amit Mendapara.
:license: BSD, see LINCESE for more details.
"""
from werkzeug import find_modules, import_string

from kalapy.conf import settings


try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading


class Loader(object):
    """Loader class automatically loads all the installed packages listed
    in settings.INSTALLED_PACKAGES.
    """

    # Borg pattern
    __shared_state = dict(
        packages = {},
        lock = _threading.RLock(),
        loaded = False
    )

    def __init__(self):
        self.__dict__ = self.__shared_state


    def load_modules(self, package, name):

        modules = tuple(find_modules(package, include_packages=True))
        fullname = '%s.%s' % (package, name)

        result = []

        if fullname in modules:
            mod = import_string(fullname)
            result.append(mod)

        try:
            submodules = tuple(find_modules(fullname))
        except (ValueError, AttributeError):
            return result

        for module in submodules:
            mod = import_string(module)
            result.append(mod)

        return result

    def load(self):
        """Load the installed packages.
        """
        if self.loaded:
            return

        self.lock.acquire()
        try:
            for package in settings.INSTALLED_PACKAGES:
                if package in self.packages:
                    continue
                self.packages[package] = registry = {}

                registry['models'] = self.load_modules(package, 'models')
                registry['views'] = self.load_modules(package, 'views')

            self.loaded = True
        finally:
            self.lock.release()

    def get_package(self, name):
        """Get the package resources which have been loaded by the loader.

        :param name: name of an package
        :returns: a dict or None
        """
        self.load()
        return self.packages.get(name)

    def get_packages(self):
        """Get the list of all the installed packages.
        """
        self.load()
        return self.packages.keys()


loader = Loader()
get_package = loader.get_package
get_packages = loader.get_packages

