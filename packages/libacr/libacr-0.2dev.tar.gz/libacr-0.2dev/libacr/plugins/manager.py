import os, tg, imp, inspect
from base import AcrPlugin

class PluginsManager(object):                    
    def __init__(self):
        self.plugins = {}
                    
    def __call__(self):
        if not self.plugins:
            self.load_plugins(self.builtin_plugins_path)
            self.load_plugins(self.site_plugins_path)
        return self

    @property
    def builtin_plugins_path(self):
        import libacr
        return os.path.dirname(libacr.plugins.__file__)
        
    @property
    def site_plugins_path(self):
        return os.path.join(os.path.dirname(tg.config.package.__file__), 'acr_plugins')

    def load_plugins(self, plugins_dir):
        print 'Loading ACR Plugins from', plugins_dir
        for root, dirs, files in os.walk(plugins_dir):
            if root != plugins_dir:
                continue

            for name in dirs:
                path = os.path.join(root, name)
                module_name = 'acr_plugin_'+name
                print 'Loading', name, '...', 
                try:
                    mfile, pathname, description = imp.find_module(name, [root])
                    module = imp.load_module(module_name, mfile, pathname, description)
                    for class_name, cls in inspect.getmembers(module, inspect.isclass):
                        if issubclass(cls, AcrPlugin) and cls != AcrPlugin:
                            self.plugins[cls.uri] = cls()
                    print 'SUCCESS'
                except Exception, e:
                    print 'FAILED', e

    def admin_actions(self):
        sections = {}
        for plugin in self.plugins.itervalues():
            for action in plugin.admin_entries:
                sections.setdefault(action.section, []).append(action)
        return sections

PluginsManager = PluginsManager()
