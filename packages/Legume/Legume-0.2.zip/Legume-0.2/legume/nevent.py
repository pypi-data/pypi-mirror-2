# legume. Copyright 2009 Dale Reidy. All rights reserved.
# See LICENSE for details.

__docformat__ = 'restructuredtext'

class NEventError(Exception): pass

class Event(object):
    def __init__(self):
        self._handlers = []

    def __iadd__(self, other):
        if other not in self._handlers:
            self._handlers.append(other)
        else:
            raise NEventError, 'Event %s error: Handler %s is already bound' % (self, other)
        return self

    def __isub__(self, other):
        try:
            self._handlers.remove(other)
        except IndexError, e:
            raise NEventError, 'Event %s error: Handler %s is not bound' % (self, other)
        return self

    def __call__(self, sender, args):
        result = None
        for handler in self._handlers:
            result = handler(sender, args)
        return result

    def is_handled_by(self, handler):
        return handler in self._handlers