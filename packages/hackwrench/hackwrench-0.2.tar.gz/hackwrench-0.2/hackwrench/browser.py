#!/usr/bin/env python
# coding: utf-8
# vim: ai ts=4 sts=4 et sw=4
from gettext import gettext as _
import os
from os import path
from urllib import quote_plus
from shlex import shlex

import gobject
import gtk
from gtk import gdk
import pango
import webkit
from inspector import Inspector
import nprefs

from urllib import urlretrieve
from hashlib import md5
from subprocess import Popen
from functools import wraps

common_js = open(path.join(path.dirname(__file__),'common.js')).read()

def foo(*args):
    print args
    return False

def get_icon(url, callback):
    f = path.expanduser('~/.hackwrench/favicons/%s.ico' % md5(url).hexdigest())
    if not path.exists(f):
        urlretrieve(url, f)
    callback(f)

class BrowserPlugin(object):
    def __init__(self, view):
        self.view = view
        for k, f in self.__class__.__dict__.items():
           if not k.startswith('_') and k in BrowserPlugin.__dict__:
              if getattr(getattr(self, k), 'after', False):
                  view.connect_after(k.replace('_','-'), getattr(self, k))
              else:
                  view.connect(k.replace('_','-'), getattr(self, k))
        if __debug__:
           print 'Plugin %r loaded' % self

    @staticmethod
    def stop(func):
        @wraps(func)
        def wrap(self, view, *args, **kargs):
            view.stop_emission(func.__name__.replace('_', '-'))
            return func(self, view, *args,**kargs)
        return wrap

    @staticmethod
    def after(func):
        func.after = True
        return func

    def hovering_over_link(self, view, title, uri):
        """ callback on 'hovering-over-link' webkit.WebView signal """
        pass
    def populate_popup(self, view, menu):
        """ callback on 'populate-popup' webkit.WebView signal """
        pass
    def load_started(self, *args):
        """ callback on 'load-started' webkit.WebView signal """
        pass
    def load_committed(self, view, frame=None):
        """ callback on 'load-committed' webkit.WebView signal """
        pass
    def load_finished(self, view, frame=None):
        """ callback on 'load-finished' webkit.WebView signal """
        pass
    def icon_loaded(self, *args):
        """ callback on 'icon-loaded' webkit.WebView signal """
        pass
    def load_error(self, *args):
        """ callback on 'load-error' webkit.WebView signal """
        pass
    def load_progress_changed(self, *args):
        """ callback on 'load-progress-changed' webkit.WebView signal """
        pass
    def download_requested(self, *args):
        """ callback on 'download-requested' webkit.WebView signal """
        pass
    def title_changed(self, view, frame, title):
        """ callback on 'title-changed' webkit.WebView signal """
        pass
    def create_web_view(self, *args):
        """ callback on 'create-web-view' webkit.WebView signal """
        pass
    def script_alert(self, *args):
        """ callback on 'script-alert' webkit.WebView signal """
        pass
    def console_message(self, *args):
        """ callback on 'console-message' webkit.WebView signal """
        pass
    def status_bar_text_changed(self, *args):
        pass
    def resource_request_starting(self, *args):
        pass
    def script_confirm(self, *args):
        pass
    def cut_clipboard(self, *args):
        pass
    def copy_clipboard(self, *args):
        pass
    def paste_clipboard(self, *args):
        pass
    def status_bar_text_changed(self, *args):
        pass
    def navigation_policy_decision_requested(self, *args):
        pass
    def navigation_policy_decision_requested(self, view, frame, request, action, decision):
        pass
    def navigation_requested(self, *args):
        pass
    def close_web_view(self, *args):
        pass
    def create_web_view(self, *args):
        pass
    def selection_changed(self, *args):
        pass
    def move_cursor(self, *args):
        pass
    def set_scroll_adjustments(self, *args):
        pass





class BrowserPage(webkit.WebView):
    __gsignals__ = {
        "started": (gobject.SIGNAL_RUN_FIRST,
                  gobject.TYPE_NONE,
                  (gobject.TYPE_OBJECT,))
        }

    def __init__(self, tab, actions):
        self.tab = tab
        self.actions = actions
        self.url = self.hovered_uri = self.icon_path = self.title = None
        super(BrowserPage, self).__init__()
        settings = self.get_settings()
        try:
            if self.tab.win.app.conf.user_agent and self.tab.win.app.conf.user_agent != 'default':
                settings.set_property("user-agent", self.tab.win.app.conf.user_agent)
            settings.set_property("auto-load-images", True)
            settings.set_property("tab-key-cycles-through-elements", True)
            #settings.set_property("enable-private-browsing", True)
            #settings.set_property("enable-caret-browsing", True)
            settings.set_property("enable-html5-database", True)
            settings.set_property("enable-html5-local-storage", True)
            settings.set_property("enable-developer-extras", True)
        except Exception,e:
            print e

        # scale other content besides from text as well
        self.set_full_content_zoom(True)
        self.plugins = [plugin(self) for plugin in BrowserPlugin.__subclasses__()]
        for plugin in self.plugins:
            if hasattr(plugin, 'preferences'):
                pr_title, pr_items = plugin.preferences
                self.tab.win.app.dlg_preferences.append(nprefs.Section(pr_title, pr_items, path='~/.hackwrench/extensions/%s.conf' % plugin.__class__.__name__.lower()))

        try:
            self.connect_after("populate-popup", self.populate_popup)
            self.connect("hovering-over-link", self.hovering_over_link)
            self.connect("populate-popup", self.populate_page_popup)
            self.connect("load-started", self.load_started)
            self.connect("load-committed", self.load_committed)
            self.connect("load-finished", self.view_load_finished)
            self.connect("icon-loaded", self.icon_loaded)
            self.connect("load-error", self.load_error)
            self.connect("load-progress-changed", self.load_progress)
            #self.connect("download-requested", self.download)
            self.connect("title-changed", self.title_changed)
            self.connect("create-web-view", self.new_web_view_request)
            self.connect("script-alert", foo)
            self.connect("console-message", self.console_message)
        except Exception, e:
            print e


    @property
    def js(self):
        if not hasattr(self, '_js'):
            try:
                import jswebkit
            except ImportError:
                try:
                    import javascriptcore as jswebkit
                except ImportError:
                    raise ImportError('You need jswebkit or javascriptcore module to use this')
            context = self.get_main_frame().get_global_context()
            self._js = jswebkit.JSContext(context)
            self.document = self._js.EvaluateScript('document')
            #self.html = lambda: self.js.EvaluateScript('document.documentElement.outerHTML')
        return self._js
    
    @property
    def html(self):
        return self.js.EvaluateScript('document.documentElement.outerHTML')


    def open(self, url):
        self.url = url.strip()
        super(BrowserPage, self).open(url)
        #self.grab_focus()

    def print_cb(self, *args):
        mainframe = self.get_main_frame()
        mainframe.print_full(gtk.PrintOperation(), gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG)

    def populate_popup(self, view, menu):
        for action in self.actions:
            menu.append(action.create_menu_item())

        printitem = gtk.ImageMenuItem(gtk.STOCK_PRINT)
        printitem.connect('activate', self.print_cb)
        menu.append(printitem)
        menu.show_all()
        for item in menu.get_children():
            if not item.props.sensitive or \
               str(item.get_label()).replace('_','')=='Open Link':
                item.hide()
        return False

    def search(self, q):
        if q not in (row[0] for row in self.tab.win.app.search_history):
            self.tab.win.app.search_history.append((q,))
        self.open(self.tab.win.app.conf.search % quote_plus(q))

    def set_cursor(self, cursor_name=None):
        self.execute_script('if(document.body) document.body.style.cursor="%s";' % (cursor_name or 'default'))
        

    def title_changed(self, view, frame, title):
        self.title = title or self.url or ''
        self.tab.set_label_text(self.title)
        if self.tab.win.view == self:
            self.tab.win.main.set_title(self.title)

    #def download(self, view, download):
    #    return Popen(self.tab.win.app.conf.download_manager % download.get_uri(), shell=True)
    
    def icon_loaded(self, view, icon):
        #if not self.icon_path:
        self.loading_icon = True
        gobject.idle_add(lambda: get_icon(icon,self._got_icon))
    
    def _got_icon(self, path):
        self.icon_path = path
        if gtk.gdk.pixbuf_get_file_info(path):
            self.tab.win.app.history.append((self.url, self.icon_path or '', self.title or self.url))
            pb = gtk.gdk.pixbuf_new_from_file_at_scale(path,18,18,True)
            self.tab.label.icon.set_from_pixbuf(pb)
            self.tab.win.app.icon_cache[self.url] = path
        #if self.tab.win.view == self:
        #    self.tab.win.location.set_icon_from_pixbuf(gtk.ENTRY_ICON_PRIMARY, self.icon)

    def populate_page_popup(self, view, menu):
        # misc
        if self.hovered_uri:
            open_in_new_win = gtk.ImageMenuItem(gtk.STOCK_OPEN)
            open_in_new_win.set_label(_("Open in new _window"))
            open_in_new_win.connect("activate", lambda *a: self.tab.win.app.new_window(self.hovered_uri))
            menu.insert(open_in_new_win, 0)
            open_in_new_tab = gtk.ImageMenuItem(gtk.STOCK_ADD)
            open_in_new_tab.set_label(_("Open in new _tab"))
            open_in_new_tab.connect("activate", self.open_in_new_tab, view)
            menu.insert(open_in_new_tab, 0)
        self.get_selection(self.google_it, menu)
        #sel = self.get_selection()
        #if sel:
        #    google_it = gtk.ImageMenuItem(gtk.STOCK_FIND)
        #    google_it.set_label("Search google for %r" % sel)
        #    google_it.connect("activate", lambda *args: self.tab.win.new_tab().browser.search(sel))
        #    menu.insert(google_it, 1)
        #    google_it.show()
        for item in menu.get_children():
            if str(item.get_label()).replace('_','')=='Copy':
                break
        menu.show_all()
    
    def google_it(self, sel, menu):
        if sel:
            google_it = gtk.ImageMenuItem(gtk.STOCK_ADD)
            label = sel[:30] + (len(sel)>30 and '..' or '')
            google_it.set_label("Search %s for %r" % (self.tab.win.app.conf.search_name, label))
            google_it.connect("activate", lambda *args: self.tab.win.new_tab().browser.search(sel))
            menu.insert(google_it, 1)
            google_it.show()


    def open_in_new_tab (self, menuitem, view=None):
        if isinstance(menuitem, basestring):
            self.tab.win.new_tab(menuitem)
        else:
            self.tab.win.new_tab(self.hovered_uri)


    def hovering_over_link(self, view, title, uri):
        self.hovered_uri = uri
        self.tab.win.set_status(uri or '', 'uri')

    def load_started (self, view, frame):
        self.tab.loading = True
        self.tab.update_toolbar()

    def load_progress(self, view, prc):
        if self.tab.win.view == view:
            self.tab.win.location.set_progress_fraction(prc/100.0)
            self.tab.loading = True
            self.tab.update_toolbar()

    def load_error (self, *args):
        self.tab.loading = False
        self.tab.update_toolbar()
    
    def load_committed (self, view, frame):
        self.url = frame.get_uri().strip()
        frame.connect('load-done', self.frame_load_done)
        self.loading_icon = False
        if self.url in self.tab.win.app.icon_cache and gtk.gdk.pixbuf_get_file_info(self.tab.win.app.icon_cache[self.url]):
            self.icon_path = self.tab.win.app.icon_cache[self.url]
            pb = gtk.gdk.pixbuf_new_from_file_at_scale(self.icon_path, 18, 18, True)
            self.tab.label.icon.set_from_pixbuf(pb)
        else:
            self.tab.label.icon.set_from_stock(gtk.STOCK_ORIENTATION_PORTRAIT, gtk.ICON_SIZE_MENU)
        gtk.main_iteration(False)
        title = frame.get_title()
        if not title:
            title = self.url or ''
        if self.tab.win.view == view:
            self.tab.win.main.set_title(title.strip())
            self.tab.win.location.set_text(str(frame.get_uri() or self.url).strip())
            self.tab.win.back.set_sensitive(view.can_go_back())
        return True

    def frame_load_done(self, frame, param):
        #print frame.get_uri(), param, frame.props.load_status
        self.execute_script(common_js)

    def view_load_finished(self, view, frame=None):
        self.tab.loading = False
        self.tab.update_toolbar()
        label = self.tab.label
        frame = view.get_main_frame()
        if frame.get_uri():
            self.url = frame.get_uri().strip()
            self.execute_script(common_js)
            if self.url == self.tab.win.app.conf.home_url:
                settings = self.get_settings()
                settings.set_property('enable-file-access-from-file-uris', True)
                self.execute_script('set_app_dir("%s");' % os.path.realpath(os.path.dirname(__file__)))
                for row in self.tab.win.app.history.top(9):
                    self.execute_script('speeddial_add("%(url)s","%(title)s","file://%(favicon)s");' % row)
                for row in self.tab.win.app.history.last(10):
                    self.execute_script('history_add("%s","%s");' % (row[0],row[2]))
                self.execute_script('table();')
            else:
                if not self.loading_icon:
                    self.tab.win.app.history.append((self.url, self.icon_path or '', label.title or self.url))
                if self.icon_path:
                    self.tab.win.app.icon_cache[self.url] = self.icon_path
        if self.tab.win.view == view:
            if self.url == self.tab.win.app.conf.home_url:
                self.tab.win.location.set_text('')
            else:
                self.tab.win.location.set_text(self.url)
            if view.can_go_back():
                self.tab.win.toolbar_back.show()
            else:
                self.tab.win.toolbar_back.hide()
        print self.search_text('test', True, True, False)

    def new_web_view_request(self, web_view, web_frame):
        view = BrowserPage(self.tab, self.tab.win.browser_actions)
        if self.tab.win.app.conf.open_all_in_tabs:
            self.tab.win.new_tab(view)
        else:
            self.tab.win.app.new_window(view)
        view.connect("web-view-ready", self.new_web_view_ready)
        return view

    def new_web_view_ready (self, web_view):
        self.new_window_requested(web_view)

    def new_window_requested(self, view):
        features = view.get_window_features()
        window = view.get_toplevel()
        scrolled_window = view.get_parent()
        window.set_default_size(features.props.width, features.props.height)
        window.move(features.props.x, features.props.y)
        return True
    
    def get_selection(self, callback, *args):
        self.eval('document.getSelection()', callback, *args)

    #def get_selection(self):
    #    self.execute_script('oldtitle=document.title;document.title=document.getSelection();')
    #    sel = self.get_main_frame().get_title().strip()
    #    self.execute_script('document.title=oldtitle;oldtitle=null;')
    #    if sel == self.title:
    #        return
    #    return sel

    def get_html(self):
        self.execute_script('oldtitle=document.title;document.title=document.documentElement.outerHTML;')
        html = self.get_main_frame().get_title()
        self.execute_script('document.title=oldtitle;oldtitle=null;')
        if html == self.title:
            return
        return html

    def _got_response_cb(self, view, msg, n, something, callback, *args):
        self.disconnect(self._got_response)
        callback(msg.strip(), *args)
        view.stop_emission('console-message')

    def eval(self, js, callback, *args):
        self._got_response = self.connect("console-message", self._got_response_cb, callback, *args)
        self.execute_script('console.log(%s);' % js)

    def console_message(self, view, msg, n, something):
        msg = shlex(msg)
        try:
            cmd = msg.next()
            if cmd.startswith('__'):
                cmd = cmd.lstrip('_')
                view.stop_emission('console-message')
                args = [arg.strip('\'"') for arg in msg]
                if cmd == 'new_tab':
                    self.open_in_new_tab(*args)
        except StopIteration:
            return
   

