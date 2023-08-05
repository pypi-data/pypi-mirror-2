#!/usr/bin/env python
# coding: utf-8
# vim: ai ts=4 sts=4 et sw=4
import os, gtk
#import gconf
from hackwrench.nprefs import *

#class Conf(object):
#    home_url = 'file://%s' % os.path.join(os.path.realpath(os.path.dirname(__file__)),'about.html')
#    new_tab_show_home = True
#    always_show_tabs = False
#    open_all_in_tabs = False
#    tabs_on_top = True
#    search = 'http://google.com/search?q=%s'
#    search_name = 'google'
#    download_manager = 'uget-gtk %s'
#    user_agent = "default"
#    decorated = True

#        #conf = gconf.Client()
#        #pref = '/apps/hackwrench'
#        #types = self.__class__.__dict__
#        #for e in conf.all_entries(pref):
#        #    if e.value:
#        #        k = e.key.split('/')[-1]
#        #        if type(types.get(k)) == int:
#        #            setattr(self, k, e.value.get_int())
#        #        elif type(types.get(k)) == bool:
#        #            setattr(self, k, e.value.get_bool())
#        #        elif isinstance(types.get(k), basestring):
#        #            setattr(self, k, e.value.get_string())

#    #def write(self):
#    #    conf = gconf.Client()
#    #    pref = '/apps/hackwrench/'
#    #    types = self.__class__.__dict__
#    #    for k,v in types.items():
#    #        if type(v) == int:
#    #            conf.set_int(pref+k, v)
#    #        elif type(v) == bool:
#    #            conf.set_bool(pref+k, v)
#    #        elif isinstance(v, basestring):
#    #            conf.set_string(pref+k, v)

#class EasyPrefs(gtk.Dialog):
#    size = (530, 400)
#    items = ()
#    def __init__(self, title='Preferences', parent=None, flags=0, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK)):
#        self.entries = {}
#        gtk.Dialog.__init__(self, title, parent, flags, buttons)
#        self.set_size_request(*self.size)
#        nb = gtk.Notebook()
#        self.vbox.pack_start(nb)
#        for label, items in self.items:
#            sw = gtk.ScrolledWindow()
#            sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
#            table = gtk.Table(len(items),2)
#            for i, (name, title, default) in enumerate(items):
#                table.attach(gtk.Label(title), 0, 1, i, i+1, gtk.FILL)
#                if type(default) == bool:
#                    self.entries[name] = gtk.CheckButton()
#                    self.entries[name].set_active(default) 
#                elif isinstance(default, basestring):
#                    self.entries[name] = gtk.Entry()
#                    self.entries[name].set_text(default)
#                table.attach(self.entries[name], 1, 2, i, i+1)
#            sw.add_with_viewport(table)
#            nb.append_page(sw, gtk.Label(label))
#        self.show_all()


#class Preferencies(EasyPrefs):
#    size = (530, 400)
#    items = (
#        ('General',
#         (
#            ('home_url', 'Home', ''),#'file://%s' % os.path.join(os.path.realpath(os.path.dirname(__file__)),'about.html')),
#            ('new_tab_show_home', 'Open home page in new tabs', True),
#            ('always_show_tabs', 'Always show tab bar', False),
#            ('open_all_in_tabs', 'Open new windows in new tabs', False),
#            ('tabs_on_top', 'Tabs on the top of window', True),
#            ('download_manager', 'Download manager', 'uget-gtk %s'),
#            ('user_agent', 'User agent', "default"),
#         ),
#        ),
#        ('Search',
#         (
#            ('search', 'Search engine', 'http://google.com/search?q=%s'),
#            ('search_name', 'Search engine title', 'google'),
#         ),
#        ),
#    )

#    def __init__(self):
#        super(EasyPrefs, self).__init__()



class Preferences(Prefs):
    path = '~/.hackwrench/hackwrench.conf'
    format = 'python'
    size = (530, 400)
    sections = [
        Section('general',
         [
            ('home_url', 'Home', 'file://%s' % os.path.join(os.path.realpath(os.path.dirname(__file__)),'about.html')),
            Group('Options',[
                ('new_tab_show_home', 'Open home page in new tabs', True),
                ('always_show_tabs', 'Always show tab bar', False),
                ('open_all_in_tabs', 'Open new windows in new tabs', False),
                ('tabs_on_top', 'Tabs on the top of window', True),
                ]
            ),
         ],
        ),
        Section('search',
         [
            ('search', 'Search engine', 'http://google.com/search?q=%s'),
            ('search_name', 'Search engine title', 'google'),
         ]
        ),
        Section('webkit',
         [
            ('user_agent', ''),
            ('tab_key_cycles_through_elements', True),
            ('enable_private_browsing', True),
            ('enable_caret_browsing', True),
            ('enable_html5_database', True),
            ('enable_html5_local_storage', True),
            ('enable_developer_extras', True),
         ],
         label='WebKit',
         path = '~/.hackwrench/webkit.conf',
        ),
    ]

    def __init__(self):
        for f in ('favicons', 'userscripts', 'extensions'):
            f = os.path.join(os.path.expanduser('~/.hackwrench/'),f)
            if not os.path.exists(f):
                os.makedirs(f)
        super(Preferences, self).__init__()

class Conf(object):
    def __init__(self, obj=None):
        self.obj = obj
    def __getattr__(self, k):
        res = self.obj[k]
        if isinstance(res, Section) or isinstance(res, dict):
            return Conf(res)
        return res

if __name__ == '__main__':
    Preferences().run()

