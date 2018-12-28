from straight.plugin import loaders
import logging
import sys
import os
import importlib
import types
import pkgutil

def ML_newFindPluginModules(self, namespace):
    # _findPluginFilePaths is unable to work with python eggs
    # So we iterate through the module itself, using importlib, and 
    # using pkgutil to implement chaining, instead of constructing module paths
    
    # use pkgutil in your namespace module to allow for chaining
    
    ns_mod = importlib.import_module(namespace)
    # walk_package recurses, iter_modules does not
    walker_function = pkgutil.walk_packages if self.recurse else pkgutil.iter_modules
                
    for importer, modname, ispkg in walker_function(
            path = ns_mod.__path__,
            prefix = namespace+'.'):
        yield importlib.import_module(modname)
        
loaders.ModuleLoader._findPluginModules = ML_newFindPluginModules

# straight.plugin's object loader comes with no filtering by default
# I want to be able to define a function to act as a filter
def OL_matchesFilter(self, module, attr_name):
    return not attr_name.startswith('_')

def OL_newFillCache(self, namespace):
    modules = self.module_loader.load(namespace)
    objects = []
    
    for module in modules:
        for attr_name in dir(module):
            if self._matchesFilter(module, attr_name):
                objects.append(getattr(module, attr_name))
 
    self._cache = objects
    return objects
loaders.ObjectLoader._matchesFilter = OL_matchesFilter
loaders.ObjectLoader._fill_cache = OL_newFillCache
