#!/usr/bin/env python
# coding: utf-8
# vim: ai ts=4 sts=4 et sw=4


class Status(gtk.Window):
    def __init__(self, parent):
        self.main = parent
        super(Status, self).__init__()
        self.set_transient_for(parent)
        self.set_destroy_with_parent(True)
        self.set_decorated(False)
        self.set_accept_focus(False)
        self.set_property("skip-taskbar-hint", True)
        self.set_type_hint(gdk.WINDOW_TYPE_HINT_TOOLTIP)
        self.set_border_width(1)
        self.label = gtk.Label('')
        self.add(self.label)
        self.show_all()
    def set_text(self, text):
        if text:
            self.label.set_text(text)
            w,h = self.label.get_layout().get_pixel_size()
            self.label.set_size_request(w,h)
            self.resize(w, h)
            x,y = self.main.window.get_origin()
            y += self.main.window.get_size()[1]-h-2
            self.move(x+2,y)
            self.show_all()
        else:
            self.hide()




