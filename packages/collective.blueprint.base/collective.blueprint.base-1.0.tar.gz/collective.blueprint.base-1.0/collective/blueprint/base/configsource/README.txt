.. -*-doctest-*-

Section Configuration Source
============================

The collective.blueprint.base.configsource transmogrifier blueprint can be used
to inject an item into the pipeline with keys and values taken from
the section configuration.

Assemble and register a transmogrifier with a deleter section.

    >>> configsource = """
    ... [transmogrifier]
    ... pipeline =
    ...     configsource
    ...     printer
    ... 
    ... [configsource]
    ... blueprint = collective.blueprint.base.configsource
    ... configsource-lists = baz qux
    ... foo =
    ...     bar blah
    ... baz =
    ...     bah
    ... qux =
    ...     quux
    ...     foo bar
    ...     baz blah
    ... 
    ... [printer]
    ... blueprint = collective.transmogrifier.sections.tests.pprinter
    ... """
    >>> registerConfig(
    ...     u'collective.blueprint.base.delete.testing.configsource',
    ...     configsource)

Run the transmogrifier.  An item with contents corresponding the
section config is injected.  All values are stripped of whitespace.  A
variable whose name is listed in the configsource-lists variable will
be broken up on newlines into a list.

    >>> transmogrifier(
    ...     u'collective.blueprint.base.delete.testing.configsource')
    {'qux': ['quux', 'foo bar', 'baz blah'],
     'foo': 'bar blah',
     'baz': ['bah']}
