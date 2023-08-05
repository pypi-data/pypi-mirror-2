from zope import interface

from collective.transmogrifier import interfaces as transmog_ifaces

from collective.blueprint.base import blueprint

class Deleter(blueprint.KeyUser):
    interface.classProvides(transmog_ifaces.ISectionBlueprint)

    keys = ('path',)

    def processItem(self, item, path):
        elems = path.strip('/').rsplit('/', 1)
        container, name = (len(elems) == 1 and ('', elems[0]) or elems)
        container = self.context.unrestrictedTraverse(container, None)
        if container is not None:
            if name in container.objectIds():
                container.manage_delObjects([name])
