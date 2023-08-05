import copy

from zope import interface

from collective.transmogrifier import interfaces as transmog_ifaces
from collective.transmogrifier import utils

from collective.blueprint.base import blueprint

class Recurser(blueprint.KeyUser):
    interface.classProvides(transmog_ifaces.ISectionBlueprint)

    key = 'recurser'
    keys = (key,)

    def __init__(self, *args, **kw):
        super(Recurser, self).__init__(*args, **kw)
        self.list = blueprint.ListIter()
        self.pipeline = utils.constructPipeline(
            self.transmogrifier,
            self.options['pipeline'].splitlines(),
            iter(self.list))

    def __iter__(self):
        for item in self.previous:
            for recursed in self.processItem(item):
                yield recursed

    def processItem(self, item):
        self.list.append(item)
        item = self.pipeline.next()
        
        before = self.options.get('before')
        if not before:
            yield item
            
        for new in self.getNewItems(item):
            for recursed in self.processItem(new):
                yield recursed
            
        if before:
            yield item

    def getNewItems(self, item):
        item_key, match = self.matchers[self.key](*item)
        if match:
            for value in item[item_key]:
                new = copy.deepcopy(item)
                del new[item_key]
                new[self.options['key']] = value
                yield new
