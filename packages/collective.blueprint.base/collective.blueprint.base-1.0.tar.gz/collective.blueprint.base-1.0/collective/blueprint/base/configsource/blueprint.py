from zope import interface

from collective.transmogrifier import interfaces as transmog_ifaces

from collective.blueprint.base import blueprint

class ConfigSource(blueprint.Source):
    interface.classProvides(transmog_ifaces.ISectionBlueprint)

    reserved = ['blueprint', 'configsource-lists']

    def getItems(self):
        lists = self.options.get('configsource-lists', '').split()
        item = {}
        for key, value in self.options.iteritems():
            if key in self.reserved:
                continue

            value = value.strip()

            if key in lists:
                item[key] = [
                    line.strip() for line in value.split('\n')
                    if line.strip()]
            else:
                item[key] = value
            
        yield item
