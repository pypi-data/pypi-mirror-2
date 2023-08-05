#!/usr/bin/env python
# coding: utf-8
# vim: ai ts=4 sts=4 et sw=4

class PluginBase(object):
    signals = []
    def __init__(self, *args, **kargs):
        super(PluginBase, self).__init__(*args, **kargs)
        for signal, fun, args, after in self.signals:
            (after and self.connect_after or self.connect)(signal, fun, *args)
        print self.signals
    @classmethod
    def connect_(cls, signal, fun, *args):
        cls.signals.append((signal, fun, args, False))

    @classmethod
    def connect_after_(cls, signal, fun, *args):
        cls.signals.append((signal, fun, args, True))

class metacls(type):
    def __new__(mcs, name, bases, dict):
        dict['signals'] = []
        #bases = bases+(PluginBase,)
        return type.__new__(mcs, name, bases, dict)

#def after(method):
#    orig_method = method
#    def wrap(f):
#        def wrapped(*args,**kargs):
#            res = orig_method(*args,**kargs)
#            f(*args,**kargs)
#            return res
#        method = wrapped
#        return wrapped
#    return wrap

#def before(method):
#    orig_method = method
#    def wrap(f):
#        def wrapped(*args,**kargs):
#            f(*args,**kargs)
#            return orig_method(*args,**kargs)
#        method = wrapped
#        return wrapped
#    return wrap

#def override(method):
#    pass

#import gui, browser

#@after(browser.BrowserPage.on_view_load_finished)
#def zzz(*args):
#    print args

#gui.main()
