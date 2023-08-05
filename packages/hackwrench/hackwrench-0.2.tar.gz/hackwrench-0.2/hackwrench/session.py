#!/usr/bin/env python
# coding: utf-8
# vim: ai ts=4 sts=4 et sw=4
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

DBusGMainLoop(set_as_default=True)

class Session(dbus.service.Object):
    def __init__(self, webbrowser):
        self.webbrowser = webbrowser
        dbus.service.Object.__init__(self, dbus.SessionBus(), '/hackwrench')
    @dbus.service.method(dbus_interface='com.hackwrench.open_url',
                         in_signature='s', out_signature='b')
    def open_url(self, url):
        return bool(self.webbrowser.new_window(url))

    @dbus.service.method(dbus_interface='com.hackwrench.open_tab',
                         in_signature='s', out_signature='b')
    def open_tab(self, url):
        return bool(self.webbrowser.active_window.new_tab(url))



