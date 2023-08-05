import copy

from zope import interface

from collective.transmogrifier import interfaces as transmog_ifaces
from collective.transmogrifier import utils

from collective.blueprint.base import blueprint

class KeySplitter(blueprint.KeyUser):
    interface.classProvides(transmog_ifaces.ISectionBlueprint)

    key = 'keysplitter'
    keys = (key,)

    def __init__(self, *args, **kw):
        super(KeySplitter, self).__init__(*args, **kw)
        self.list = blueprint.ListIter()
        self.pipeline = utils.constructPipeline(
            self.transmogrifier,
            self.options.get('pipeline', '').splitlines(),
            iter(self.list))
        self.include = self.options.get('include')

    def __iter__(self):
        for item in self.previous:
            after = self.options.get('after')
            if after:
                yield item

            for new in self.getNewItems(item):
                self.list.append(new)
                new = self.pipeline.next()
                if self.include:
                    yield new

            if not after:
                yield item

    def getNewItems(self, item):
        item_key, match = self.matchers[self.key](*item)
        if match:
            for value in item[item_key]:
                new = copy.deepcopy(item)
                new[item_key] = value
                yield new

# TODO: insert the original item under a key in the new item for
# reference?
