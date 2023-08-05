.. -*-doctest-*-

Key Splitter
============

The collective.blueprint.base.keysplitter transmogrifier blueprint can
be used to insert an arbitrary number of items into the pipeline from
a key in the original item.  This can be useful, for example, when an
arbitrary number of objects must be constricted (or any other pipeline
action) based on a key in the upstream item.

The values to iterate over and insert new items will be retrieved from
(in order)
``_collective.blueprint.base.keysplitter_[sectionname]_keysplitter``,
``_collective.blueprint.base.keysplitter_keysplitter``,
``_[sectionname]_keysplitter``, and ``_keysplitter``, where
``[sectionname]`` is replaced with the name given to the current
section. This allows you to target the right section precisely if
needed. Alternatively, you can specify what key to use for the
keysplitter by specifying the ``keysplitter-key`` option, which should
be a list of keys to try (one key per line, use a ``re:`` or
``regexp:`` prefix to specify regular expressions).

The 'pipeline' option may be used to specify a list of sections which
will be run for new items only.  The original items will not be put
through this pipeline.  Unless the 'include' option is set, the new
items will not be put through the rest of the originating pipeline.

By default the new items are inserted into the pipeline before the
original item is yielded.  This is useful when the results of
processing the new items are required to finish processing the
original item.  For example, several objects may need to be created
based on the key values so that the object created for the original
item can set references to them.  If, however, the original item must
be processed before the new items, then setting the "after" option in
the keysplitter section will cause the new items to be inserted after
the original item is yielded and processed.

Assemble and register a transmogrifier with a key splitter section.

    >>> keysplitter = """
    ... [transmogrifier]
    ... pipeline =
    ...     initsource
    ...     keysplitter
    ...     qux
    ...     printer
    ...     
    ... [initsource]
    ... blueprint = collective.blueprint.base.configsource
    ... configsource-lists = _keysplitter
    ... _keysplitter =
    ...     bar
    ...     baz
    ... 
    ... [keysplitter]
    ... blueprint = collective.blueprint.base.keysplitter
    ... pipeline =
    ...     foo
    ...     printer
    ... 
    ... [foo]
    ... blueprint = collective.transmogrifier.sections.inserter
    ... key = string:foo
    ... value = item/_keysplitter
    ... 
    ... [qux]
    ... blueprint = collective.transmogrifier.sections.inserter
    ... key = string:qux
    ... value = item/_keysplitter
    ... 
    ... [printer]
    ... blueprint = collective.transmogrifier.sections.tests.pprinter
    ... """
    >>> registerConfig(
    ...     u'collective.blueprint.base.keysplitter.testing',
    ...     keysplitter)

Run the transmogrifier.  An item with two values targeted for the
keysplitter section is inserted into the pipeline.  When this item
reaches the keysplitter section, the values in the '_keysplitter' key
are iterated over to insert new items.

    >>> transmogrifier(
    ...     u'collective.blueprint.base.keysplitter.testing')
    {'_keysplitter': 'bar', 'foo': 'bar'}
    {'_keysplitter': 'baz', 'foo': 'baz'}
    {'_keysplitter': ['bar', 'baz'], 'qux': ['bar', 'baz']}

This transmogrifier uses the after and include options and doesn't
include a sub-pipeline.

    >>> keysplitter = """
    ... [transmogrifier]
    ... pipeline =
    ...     initsource
    ...     keysplitter
    ...     printer
    ...     
    ... [initsource]
    ... blueprint = collective.blueprint.base.configsource
    ... configsource-lists = _keysplitter
    ... _keysplitter =
    ...     bar
    ...     baz
    ... 
    ... [keysplitter]
    ... blueprint = collective.blueprint.base.keysplitter
    ... after = True
    ... include = True
    ... 
    ... [printer]
    ... blueprint = collective.transmogrifier.sections.tests.pprinter
    ... """
    >>> registerConfig(
    ...     u'collective.blueprint.base.keysplitter.testing2',
    ...     keysplitter)

    >>> transmogrifier(
    ...     u'collective.blueprint.base.keysplitter.testing2')
    {'_keysplitter': ['bar', 'baz']}
    {'_keysplitter': 'bar'}
    {'_keysplitter': 'baz'}
