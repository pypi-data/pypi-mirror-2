import itertools

from zope import interface

from collective.transmogrifier import interfaces as transmog_ifaces

from collective.blueprint.base import keys

class ListIter(list):

    def __iter__(self):
        while self:
            yield self.pop(0)
               
class Base(object):
    interface.implements(transmog_ifaces.ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context

class KeyChanger(Base):

    def __iter__(self):
        for item in self.previous:
            item.update(
                keys.getKeys(self.options, **self.processItem(item)))
            yield item

    def processItem(self, item):
        raise NotImplementedError(
            'KeyChanger blueprints must implement processItem')

class Source(Base):
    """Source blueprints iterate over all previous items then inject
    new items."""

    def __iter__(self):
        return itertools.chain(self.previous, self._getItems())

    def _getItems(self):
        for item in self.getItems():
            yield keys.getKeys(self.options, **item)

    def getItems(self):
        raise NotImplementedError(
            'Source blueprints must implement getItems')

class KeyUser(Base):

    def __init__(self, transmogrifier, name, options, previous):
        super(KeyUser, self).__init__(
            transmogrifier, name, options, previous)
        self.required = self.options.get(
            'required', 'True').strip().lower() in ('true', 'on', '1')
        self.matchers = keys.makeMatchers(
            options, name,
            *getattr(self, 'keys', ()),
            **getattr(self, 'extras', {}))

    def __iter__(self):
        for item in self.previous:
            yield self.matchItem(item)

    def matchItem(self, item):
        kw = {}
        for key, matcher in self.matchers.iteritems():
            item_key, match = matcher(*item)
            if item_key:
                kw[key] = item[item_key]
            elif not self.required:
                break
        else:
            self.processItem(item, **kw)
        return item

    def processItem(self, item):
        raise NotImplementedError(
            'KeyUser blueprints must implement processItem')
