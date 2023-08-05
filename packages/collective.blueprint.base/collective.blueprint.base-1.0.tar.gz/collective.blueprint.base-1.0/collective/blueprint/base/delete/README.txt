.. -*-doctest-*-

Delete Blueprint
================

The collective.blueprint.base.delete transmogrifier blueprint can be used
to make pipleine sections that delete existing objects at the item
path.

Some objects exist before running the transmogrifier, others don't.

    >>> hasattr(folder, 'foo')
    True
    >>> folder.foo
    <File at /test_folder_1_/foo>
    >>> hasattr(folder, 'bar')
    False

Assemble and register a transmogrifier with a deleter section.

    >>> deleter = """
    ... [transmogrifier]
    ... pipeline =
    ...     foosource
    ...     barsource
    ...     deleter
    ...     printer
    ...     
    ... [foosource]
    ... blueprint = collective.blueprint.base.configsource
    ... _path = /foo
    ...     
    ... [barsource]
    ... blueprint = collective.blueprint.base.configsource
    ... _path = /bar
    ... 
    ... [deleter]
    ... blueprint = collective.blueprint.base.deleter
    ... 
    ... [printer]
    ... blueprint = collective.transmogrifier.sections.tests.pprinter
    ... """
    >>> registerConfig(
    ...     u'collective.blueprint.base.delete.testing.deleter',
    ...     deleter)

Run the transmogrifier.  The blueprint ignores items with paths that
don't point to existing objects.

    >>> from collective.transmogrifier import transmogrifier
    >>> transmogrifier.Transmogrifier(folder)(
    ...     u'collective.blueprint.base.delete.testing.deleter')
    {'_path': '/foo'}
    {'_path': '/bar'}

The object has been deleted.

    >>> hasattr(folder, 'foo')
    False
    >>> hasattr(folder, 'bar')
    False
