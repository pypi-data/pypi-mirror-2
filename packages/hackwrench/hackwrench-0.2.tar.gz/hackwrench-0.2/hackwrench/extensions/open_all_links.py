#!/usr/bin/env python
# coding: utf-8
# vim: ai ts=4 sts=4 et sw=4

import gtk
from hackwrench.browser import BrowserPlugin

open_links_js = """(function(){ var urls = new Array();
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

class OpenAllLinks(BrowserPlugin):
    def populate_popup(self, view, menu):
        view.get_selection(self.got_selection, view, menu)
        #return False

    def got_selection(self, sel, view, menu):
        if sel:
            menuitem = gtk.MenuItem('Open all selected links')
            menuitem.connect('activate', self.open_all_links, view)
            menu.insert(menuitem, 0)
            menu.show_all()

    def open_all_links(self, widget, view):
        view.execute_script(open_links_js)



