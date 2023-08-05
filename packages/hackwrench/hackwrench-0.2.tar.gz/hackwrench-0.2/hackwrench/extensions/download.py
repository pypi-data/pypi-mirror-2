#!/usr/bin/env python
# coding: utf-8
# vim: ai ts=4 sts=4 et sw=4

from hackwrench.browser import BrowserPlugin
from subprocess import Popen

class DownloadManager(BrowserPlugin):
    preferences = ('download',[
        ('download_manager', 'Download manager', 'uget-gtk %s'),
        ('download_path', 'Default path', '~/Desktop'),
    ])
    
    def download_requested(self, view, download):
        return Popen(view.tab.win.app.conf.download.download_manager % download.get_uri(), shell=True)


