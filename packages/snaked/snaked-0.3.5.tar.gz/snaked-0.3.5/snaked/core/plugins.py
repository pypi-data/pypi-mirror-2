import sys
import traceback

from snaked.core.shortcuts import Shortcut, register_shortcut, get_path_by_key
from snaked.core.prefs import ListSettings

default_enabled_plugins = ['quick_open', 'save_positions', 'edit_and_select',
    'python', 'complete_words', 'hash_comment', 'python_flakes', 'goto_line',
    'goto_dir', 'search']

def get_package(name):
    try:
        return sys.modules[name]
    except KeyError:
        __import__(name)
        return sys.modules[name]
        
def get_plugin(plugin):
    package_name = 'snaked.plugins.' + plugin
    return get_package(package_name)


class ShortcutsHolder(object):
    def __init__(self):
        self.shortcuts = []

    def add_shortcut(self, name, accel, category, desc, callback):
        self.shortcuts.append((name, accel, category, desc, callback))


class PluginManager(object):
    def __init__(self):
        self.restore_enabled_plugins()

        self.loaded_plugins = {}

        self.plugin_by_path = {}
        self.shortcuts_by_plugins = {}
        self.binded_shortcuts = {}

    def get_plugin(self, name):
        try:
            return self.loaded_plugins[name]
        except KeyError:
            plugin = get_plugin(name)
            if hasattr(plugin, 'init'):
                holder = ShortcutsHolder()
                plugin.init(holder)
                self.add_shortcuts(plugin, holder)
            self.loaded_plugins[name] = plugin
            return plugin

    def add_shortcuts(self, plugin, holder):
        for name, accel, category, desc, callback in holder.shortcuts:
            shortcut = Shortcut(name, accel, category, desc)
            shortcut.callback = callback

            path = register_shortcut(name, accel, category, desc)

            self.plugin_by_path[path] = (plugin, shortcut)
            self.shortcuts_by_plugins.setdefault(plugin, []).append(shortcut)

    def bind_shortcuts(self, activator, editor):
        for p in self.plugins_for(editor):
            for s in self.shortcuts_by_plugins.get(p, []):
                try:
                    self.binded_shortcuts[activator][s.name]
                except KeyError:
                    self.binded_shortcuts.setdefault(activator, {})[s.name] = True
                    activator.bind_to_name(s.name, self.activate_plugin_shortcut)

    def activate_plugin_shortcut(self, key, modifier, editor, *args):
        try:
            plugin, shortcut = self.plugin_by_path[get_path_by_key(key, modifier)]
        except KeyError:
            return False
        
        if self.plugin_is_for_editor(plugin, editor):
            shortcut.callback(editor, *args)
            return True
        
        return False
    activate_plugin_shortcut.provide_key = True

    def plugin_is_for_editor(self, plugin, editor):
        return not hasattr(plugin, 'langs') or editor.lang in plugin.langs

    def plugins_for(self, editor):
        for name in self.enabled_plugins:
            try:
                plugin = self.get_plugin(name)
            except Exception:
                editor.message("Can't load %s plugin" % name, 5000)
                self.enabled_plugins.remove(name)
                traceback.print_exc()
                continue

            if self.plugin_is_for_editor(plugin, editor):
                yield plugin

    def editor_opened(self, editor):
        for p in self.plugins_for(editor):
            if hasattr(p, 'editor_opened'):
                try:
                    p.editor_opened(editor)
                except:
                    traceback.print_exc()

    def editor_closed(self, editor):
        for p in self.plugins_for(editor):
            if hasattr(p, 'editor_closed'):
                try:
                    p.editor_closed(editor)
                except:
                    traceback.print_exc()

    def editor_created(self, editor):
        for p in self.plugins_for(editor):
            if hasattr(p, 'editor_created'):
                try:
                    p.editor_created(editor)
                except:
                    traceback.print_exc()

    def quit(self):
        for p in self.loaded_plugins.values():
            if hasattr(p, 'quit'):
                try:
                    p.quit()
                except:
                    traceback.print_exc()
    
    @property
    def prefs(self):
        return ListSettings('enabled-plugins.db')
        
    def save_enabled_plugins(self):
        self.prefs.store(self.enabled_plugins)
            
    def restore_enabled_plugins(self):
        prefs = self.prefs
        if prefs.exists():
            self.enabled_plugins = prefs.load()
        else:
            self.enabled_plugins = default_enabled_plugins
        
    def unload_unnecessary_plugins(self):
        bad_plugin_names = [name for name in self.loaded_plugins
            if name not in self.enabled_plugins]
            
        for name in bad_plugin_names:
            p = self.loaded_plugins[name]
            if hasattr(p, 'quit'):
                try:
                    p.quit()
                except:
                    traceback.print_exc()
                    
            del self.loaded_plugins[name]
            self.delete_plugin_shortcuts(p)

    def delete_plugin_shortcuts(self, plugin):
        try:
            del self.shortcuts_by_plugins[plugin]
        except KeyError:
            pass
           
        for path in [path for path, (p,_) in self.plugin_by_path.iteritems() if p is plugin]:
            del self.plugin_by_path[path]
        
    def show_plugins_prefs(self, editor):
        from snaked.core.gui.plugin_prefs import PluginDialog
        dialog = PluginDialog()
        editor.request_transient_for.emit(dialog.window)

        def set_plugin_list(plugin_list):
            self.enabled_plugins = plugin_list
            self.save_enabled_plugins()
            editor.message('Enabled plugins list saved')
            self.unload_unnecessary_plugins()
            editor.plugins_changed.emit()

        dialog.show(self.enabled_plugins, set_plugin_list)
