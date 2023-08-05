#!/usr/bin/env python
# coding: utf-8
# vim: ai ts=4 sts=4 et sw=4

import gtk
from hackwrench.browser import BrowserPlugin
import gobject
from fnmatch import fnmatch
from os import path
from glob import glob
import os
from urllib import urlretrieve
from hackwrench.gui import confirm

class GreaseMonkey(BrowserPlugin):
    #def __init__(self, view):
    #    BrowserPlugin.__init__(self, view)

    def load_finished(self, view, frame=None):
        if frame and frame.get_uri():
            for f in glob(path.expanduser('~/.hackwrench/userscripts/*user.js')):
                for line in open(f):
                    if '@include' in line or '@match' in line:
                        line = line.replace('@match','@include')
                        mask = line.split('@include',1)[1].strip()
                        if fnmatch(frame.get_uri(), mask):
                            print 'userscript %s match(%s,%s)' % (f, frame.get_uri(), mask)
                            view.execute_script(open(f).read())
                            break
                        elif '==/UserScript==' in line:
                            break

    def install_userscript(self, view, url):
        save_to = os.path.expanduser('~/.hackwrench/userscripts/%s' % os.path.basename(url))
        if not os.path.exists(os.path.dirname(save_to)):
            os.makedirs(os.path.dirname(save_to))

        urlretrieve(url, save_to)
        msg = "userscript %s installed from <a href=\"%s\">%s</a>" % (os.path.basename(url), url, url)
        view.load_string(msg, "text/html", "iso-8859-15", '')

    @BrowserPlugin.after
    def populate_popup(self, view, menu):
        if view.hovered_uri and view.hovered_uri.endswith('.user.js'):
            menuitem = gtk.MenuItem('Install userscript')
            menuitem.connect('activate', lambda *args: gobject.idle_add(self.install_userscript, view, view.hovered_uri))
            menu.insert(menuitem, 0)
            menu.show_all()

    def navigation_policy_decision_requested(self, view, frame, request, action, decision):
        if request.get_uri().startswith('http://') and request.get_uri().endswith('.user.js'):
            if confirm('Install userscript from %s?' % request.get_uri()):
                gobject.idle_add(self.install_userscript, view, request.get_uri())
            decision.ignore()
        return False




