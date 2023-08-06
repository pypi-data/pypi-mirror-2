"""\
Allows nested imports, a la Java. It installs a harmless meta import-hook that 
adds support for *nested packages*, i.e., multiple packages that "live" under a 
common namespace. This is the idiom in Java, where you have packages like 
``com.foo.bar.spam`` and ``com.foo.bar.eggs``, as well as in Haskell. 
Nimp basically allows packages to "inject" themselves into shared namespaces.

Compatible with Python 2.3 and up and 3.0 and up

Usage::

  import nimp
  nimp.install()

Example Layout
--------------
Assume the following directory structure, say, in your ``site-packages``::

  com.ibm.storage/
    files...
  com.ibm.storage.plugins/
    files...
  com.ibm.pythontools/
    files...

Using Nimp, the following imports will work as expected::
  
  import com                              # a namespace package (empty)
  import com.ibm                          # a namespace package (empty)
  import com.ibm.pythontools              # a real package
  com.ibm.pythontools.myfunc(1,2,3)
  
  # and of course using `from` works too
  from com.ibm.storage import ScsiDisk    
  
  # note how the `plugins` package was "injected" into `storage`
  from com.ibm.storage.plugins import MySQLPlugin
"""
import os
import sys
import imp


class _Nimp(object):
    def __init__(self):
        self.cache = {}
    
    @staticmethod
    def _get_name_prefixes(dotted_name):
        i = -1
        while i is not None:
            i = dotted_name.find(".", i+1)
            if i < 0:
                i = None
            yield dotted_name[0:i]
    
    def _find_all(self, fullname):
        assert fullname not in self.cache
        for path in sys.path:
            if not os.path.isdir(path):
                continue
            for fn in os.listdir(path):
                fullpath = os.path.join(path, fn)
                if not os.path.isdir(fullpath) or "." not in fn or not fn.startswith(fullname):
                    continue
                for pref in self._get_name_prefixes(fn):
                    fullpath = os.path.join(path, pref)
                    if os.path.exists(fullpath):
                        if pref in self.cache and self.cache[pref] != fullpath:
                            raise ImportError("%r duplicated: %s and %s" % (pref, fullpath, self.cache[pref]))
                        self.cache[pref] = fullpath # real
                    else:
                        if pref in self.cache and self.cache[pref] is not None:
                            continue # do not override real
                        self.cache[pref] = None # namespace only
    
    def clear_cache(self):
        self.cache.clear()
    
    def find_module(self, fullname, path=None):
        if fullname in self.cache:
            return self
        self._find_all(fullname)
        if fullname in self.cache:
            return self
        else:
            return None
    
    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        path = self.cache[fullname]
        
        # must insert to sys.modules first, to avoid cyclic imports
        try:
            imp.acquire_lock()
            mod = sys.modules[fullname] = imp.new_module(fullname)
            try:
                if path is None:
                    mod.__file__ = "<namespace module>"
                    mod.__path__ = []
                else:
                    info = imp.find_module(fullname, [os.path.dirname(path)])
                    mod = imp.load_module(fullname, *info)
                    # replace the stub in sys.modules
                    sys.modules[fullname] = mod
            except Exception:
                del sys.modules[fullname]
                raise
        finally:
            imp.release_lock()
        
        return mod

# create Nimp singleton
the_nimp = _Nimp()
_installed = False

def install():
    """installs the nimp meta-importer hook; this enables the use of nested imports"""
    global _installed
    if _installed:
        return
    sys.meta_path.append(the_nimp)
    _installed = True

def uninstall():
    """removed the nimp meta-importer hook; nested imports will no longer be possible"""
    global _installed
    if not _installed:
        return
    sys.meta_path.remove(the_nimp)
    _installed = False


