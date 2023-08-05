#!/usr/bin/env python
# coding: utf-8
# vim: ai ts=4 sts=4 et sw=4
import gtk
import gui, browser

def foo(self, ):
    print args

js = """(function(){ var urls = new Array();
            var selection = window.getSelection();
            var hrefs = document.links;
            for ( i = 0; i < hrefs.length; i++)
            {
                if ( selection.containsNode( hrefs[i], true) )
                {
                    urls.push( hrefs[i].href);
                }
            }
            for(var i=0;i<urls.length;i++)
            {
                window.openTab(urls[i]);
            }
            })()
"""

orig = browser.BrowserPage.populate_popup
def populate_popup(self, view, menu):
    orig(self, view, menu)
    view.get_selection(has_selection, view, menu)

def has_selection(sel, view, menu):
    if sel:
        printitem = gtk.MenuItem('open links in tabs')
        printitem.connect('activate', lambda *args: view.execute_script(js))
        menu.insert(printitem, 0)
        menu.show_all()

def dectest(f):
    def wrap(self, view, menu):
        testitem = gtk.MenuItem('test')
        testitem.connect('activate', lambda *args: False)
        menu.insert(testitem, 0)
        menu.show_all()
        f(self, view, menu)
    return wrap


gui.BrowserWindow.back_cb = foo
browser.BrowserPage.populate_popup = dectest(populate_popup)

gui.main()





