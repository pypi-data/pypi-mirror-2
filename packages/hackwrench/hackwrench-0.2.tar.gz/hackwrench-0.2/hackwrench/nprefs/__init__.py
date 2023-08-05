#!/usr/bin/env python
# coding: utf-8
# vim: ai ts=4 sts=4 et sw=4
import gtk, os

# TODO: detect name collision!

class PrefsValues(object):
    def __get__(self, obj, cls):
        values = {}
        for k,v in obj.entries.items():
            t = type(obj.defaults[k])
            if t is bool:
                v = v.get_active()
            elif issubclass(t, basestring):
                v = v.get_text()
            elif t is int:
                v = v.get_value_as_int()
            elif t is float:
                v = v.get_value()
            values[k] = v
        return values

    def __set__(self, obj, values):
        for k,v in obj.entries.items():
            if k in values:
                t = type(obj.defaults[k])
                val = values[k]
                if not (issubclass(t, basestring) and isinstance(val, basestring)) and type(val) != t:
                    raise ValueError('%s should be %r' % (k, t))
                if t is bool:
                    v.set_active(val)
                elif issubclass(t, basestring):
                    v.set_text(val)
                elif t in (int, float):
                    v.set_value(val)
                obj.initial[k] = val


class Section(gtk.ScrolledWindow):
    values = PrefsValues()
    path = None

    def __init__(self, title, items, **kargs):
        self.title = title
        self.label = gtk.Label(kargs.get('label',title.capitalize()))
        self.entries = {}
        self.defaults = {}
        gtk.ScrolledWindow.__init__(self)
        self.items = Items(items)
        self.add_with_viewport(self.items)
        self.entries.update(self.items.entries)
        self.defaults.update(self.items.defaults)
        self.initial = dict(self.defaults)
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.path = kargs.get('path', None)
    
    def __getitem__(self, k):
        return self.initial[k]

class Group(gtk.Frame):
    def __init__(self, title, items):
        self.entries = {}
        self.defaults = {}
        gtk.Frame.__init__(self, title)
        self.items = Items(items)
        self.add(self.items)
        self.entries.update(self.items.entries)                
        self.defaults.update(self.items.defaults)
        self.items = items

class Items(gtk.VBox):
    def __init__(self, items):
        self.entries = {}
        self.defaults = {}
        gtk.VBox.__init__(self, spacing=4)
        self.items = items
        for item in items:
            if isinstance(item, tuple):
                if len(item) == 2:
                    name, default = item
                    title = name.replace('_',' ').capitalize()
                elif len(item) == 3:
                    name, title, default = item
                else:
                    raise ValueError('ban tuple length: %d could be (name, default) or (name, title, default)' % len(item))
                hbox = gtk.HBox(spacing=4)
                self.defaults[name] = default
                if type(default) == bool:
                    self.entries[name] = gtk.CheckButton(title)
                    self.entries[name].set_active(default)
                    hbox.pack_start(self.entries[name], False)
                elif isinstance(default, basestring):
                    if os.path.exists(os.path.expanduser(default)):
                        self.entries[name] = gtk.Entry()
                        self.entries[name].set_text(os.path.expanduser(default))
                    else:
                        self.entries[name] = gtk.Entry()
                        self.entries[name].set_text(default)
                    hbox.pack_start(gtk.Label(title+':'), False, padding=2)
                    hbox.pack_start(self.entries[name], True)
                elif type(default) in (float, int):
                    self.entries[name] = gtk.SpinButton()
                    self.entries[name].set_digits(type(default) is float and 2 or 0)
                    self.entries[name].set_value(default)
                    hbox.pack_start(gtk.Label(title), False, padding=2)
                    hbox.pack_start(self.entries[name], True)

            elif isinstance(item, Group):
                hbox = item
                self.entries.update(item.entries)
                self.defaults.update(item.defaults)
            else:
                raise ValueError('item should be Group, or tuple')

            align = gtk.Alignment(0.0, 0.0, 1.0, 0.0)
            align.set_padding(0,0,2,2)
            align.add(hbox)
            self.pack_start(align, False, padding=4)






class Prefs(gtk.Dialog):
    size = (530, 400)
    sections = []
    format = 'python'

    values = PrefsValues()

    def __init__(self, title='Preferences', parent=None, flags=0, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK)):
        self.entries = {}
        self.defaults = {}
        gtk.Dialog.__init__(self, title, parent, flags, buttons)
        self.set_size_request(*self.size)
        self.notebook = gtk.Notebook()
        self.vbox.pack_start(self.notebook)
        self.sections_by_title = {}
        self.initial = dict(self.defaults)
        for section in self.sections:
            self.append(section)
        self.load()

    def append(self, section):
        if section not in self.sections:
            self.sections.append(section)
        self.sections_by_title[section.title] = section
        self.notebook.append_page(section, section.label)
        if not section.path:
            self.entries.update(section.entries)
            self.defaults.update(section.defaults)
            self.initial.update(section.defaults)
        self.notebook.set_show_tabs(self.notebook.get_n_pages()>1)
        self.notebook.show_all()


    def run(self, *args, **kargs):
        res = super(Prefs, self).run(*args, **kargs) == gtk.RESPONSE_OK
        if res:
            for section in [self]+list(self.sections):
                section.initial.update(section.values)
            self.save()
        self.hide()
        return res

    def load(self):
        for section in [self]+list(self.sections):
            if section.path and section.entries:
                path = os.path.expanduser(section.path)
                section.initial = dict(section.defaults)
                if os.path.exists(path):
                    if self.format == 'python':
                        exec(open(path).read())
                        section.values = locals()
                    elif self.format == 'json':
                        import simplejson
                        section.values = simplejson.load(open(path))
                    else:
                        raise ValueError('unknown format: %r' % self.format)

    def save(self):
        for section in [self]+list(self.sections):
            if section.path and section.entries:
                path = os.path.expanduser(section.path)
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                f = open(path, 'w')
                if self.format == 'python':
                    for item in section.values.items():
                        print >>f, '%s = %r' % item
                elif self.format == 'json':
                    import simplejson
                    simplejson.dump(section.values, f)
                else:
                    raise ValueError('unknown format: %r' % self.format)
                f.close()
    
    def __getitem__(self, k):
        if k in self.sections_by_title:
            return self.sections_by_title[k]
        else:
            return self.initial[k]






