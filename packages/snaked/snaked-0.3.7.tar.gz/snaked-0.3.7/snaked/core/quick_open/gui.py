import os.path
import weakref

import gtk

from snaked.util import idle, join_to_file_dir, BuilderAware, open_mime, refresh_gui
from snaked.core.shortcuts import ShortcutActivator
from snaked.core.prefs import ListSettings, load_json_settings, save_json_settings

import settings
import searcher

class QuickOpenDialog(BuilderAware):
    def __init__(self):
        super(QuickOpenDialog, self).__init__(join_to_file_dir(__file__, 'gui.glade'))
        self.shortcuts = ShortcutActivator(self.window)
        self.shortcuts.bind('Escape', self.escape)
        self.shortcuts.bind('<alt>Up', self.project_up)
        self.shortcuts.bind('<alt>Down', self.project_down)
        self.shortcuts.bind('Return', self.open_file)
        self.shortcuts.bind('<ctrl>Return', self.open_mime)
        self.shortcuts.bind('<alt>s', self.focus_search)
        self.shortcuts.bind('<ctrl>o', self.free_open)
        self.shortcuts.bind('<ctrl>p', self.popup_projects)
        self.shortcuts.bind('<ctrl>Delete', self.delete_project)

    def get_stored_recent_projects(self):
        if self.editor().session:
            return load_json_settings(
                '%s.session' % self.editor().session, {}).get('recent_projects', [])
        else:
            return ListSettings('project-roots.db').load()
            
    def store_recent_projects(self, projects):
        if self.editor().session:
            name = '%s.session' % self.editor().session
            settings = load_json_settings(name, {})
            settings['recent_projects'] = list(projects)
            save_json_settings(name, settings)
        else:
            return ListSettings('project-roots.db').store(projects)
    
    def show(self, editor):
        self.editor = weakref.ref(editor)
        self.update_recent_projects()
        self.update_projects(editor.project_root)
        editor.request_transient_for.emit(self.window)
        
        self.search_entry.grab_focus()
        
        self.window.present()
    
    def update_recent_projects(self):
        saved_projects = self.get_stored_recent_projects()
                
        if any(p not in saved_projects for p in settings.recent_projects):
            [saved_projects.append(p) for p in settings.recent_projects
                if p not in saved_projects]
            self.store_recent_projects(saved_projects)
            settings.recent_projects = saved_projects
            return
            
        if any(p not in settings.recent_projects for p in saved_projects):
            [settings.recent_projects.append(p) for p in saved_projects
                if p not in settings.recent_projects]
    
    def update_projects(self, root):
        self.projects_cbox.set_model(None)
        self.projectlist.clear()
        
        index = 0
        for i, r in enumerate(settings.recent_projects):
            if r == root:
                index = i
            self.projectlist.append((r,))
        
        self.projects_cbox.set_model(self.projectlist)
        self.projects_cbox.set_active(index)
    
    def hide(self):
        self.window.hide()
        
    def on_delete_event(self, *args):
        self.escape()
        return True
    
    def project_up(self):
        idx = self.projects_cbox.get_active()
        idx = ( idx - 1 ) % len(self.projectlist)
        self.projects_cbox.set_active(idx)
        
    def project_down(self):
        idx = self.projects_cbox.get_active()
        idx = ( idx + 1 ) % len(self.projectlist)
        self.projects_cbox.set_active(idx)

    def get_current_root(self):
        return self.projectlist[self.projects_cbox.get_active()][0]
    
    def fill_filelist(self, search):
        self.filelist.clear()
        
        current_search = object()
        self.current_search = current_search
        
        already_matched = {}
        i = 0
        
        for m in (searcher.name_start_match, searcher.name_match,
                searcher.path_match, searcher.fuzzy_match):
            for p in searcher.search(self.get_current_root(), '', m(search), already_matched):
                if self.current_search is not current_search:
                    return
                    
                already_matched[p] = True            
                self.filelist.append(p)
                
                if i % 10 == 0:
                    refresh_gui()
                    
                i += 1

        self.filelist_tree.columns_autosize()

    def on_search_entry_changed(self, *args):
        search = self.search_entry.get_text().strip()
        if search:
            idle(self.fill_filelist, search)
        
    def on_projects_cbox_changed(self, *args):
        self.on_search_entry_changed()

    def get_selected_file(self):
        (model, iter) = self.filelist_tree.get_selection().get_selected()
        if iter:
            return os.path.join(self.get_current_root(), *self.filelist.get(iter, 1, 0))
        else:
            return None
    
    def open_file(self):
        fname = self.get_selected_file()
        if fname:
            self.hide()
            refresh_gui()
            self.editor().open_file(fname)
        
    def open_mime(self):
        fname = self.get_selected_file()
        if fname:
            self.hide()
            refresh_gui()
            open_mime(fname)

    def focus_search(self):
        self.search_entry.grab_focus()

    def escape(self):
        if hasattr(self.editor(), 'on_dialog_escape'):
            idle(self.editor().on_dialog_escape, self)
        self.hide()
        
    def free_open(self):
        dialog = gtk.FileChooserDialog("Open file...",
            None,
            gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        
        dialog.set_default_response(gtk.RESPONSE_OK)
        
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            idle(self.editor().open_file, dialog.get_filename())
            idle(self.hide)
        
        dialog.destroy()

    def popup_projects(self):
        self.projects_cbox.popup()
        
    def delete_project(self):
        if len(self.projectlist):
            current_root = self.get_current_root()
            if current_root == self.editor().project_root:
                self.editor().message('You can not remove current project')
                return
            settings.recent_projects.remove(current_root)
            self.store_recent_projects(settings.recent_projects)
        
            idx = self.projects_cbox.get_active()
            self.projectlist.remove(self.projects_cbox.get_active_iter())
            self.projects_cbox.set_active(idx % len(self.projectlist))
            self.editor().message('Project removed')
