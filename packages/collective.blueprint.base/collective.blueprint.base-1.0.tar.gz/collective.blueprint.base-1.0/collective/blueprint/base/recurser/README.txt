.. -*-doctest-*-

Recursive Splitter
==================

The collective.blueprint.base.recurser transmogrifier blueprint can be
used to add recursion to a pipeline.

The values to recurse into will be retrieved from (in order)
``_collective.blueprint.base.recurser_[sectionname]_recurser``,
``_collective.blueprint.base.recurser_recurser``,
``_[sectionname]_recurser``, and ``_recurser``, where
``[sectionname]`` is replaced with the name given to the current
section. This allows you to target the right section precisely if
needed. Alternatively, you can specify what key to use for the
recurser by specifying the ``recurser-key`` option, which should
be a list of keys to try (one key per line, use a ``re:`` or
``regexp:`` prefix to specify regular expressions).

The 'pipeline' option is used to specify a list of sections which will
be run recursively.  By default, recursive items are inserted into the
pipeline after the original item is yielded.  If, however, the
'before' option is set, the recursive items will be inserted before
the original item is yielded and processed.

When recursing into a value, the value will be inserted into the item
under the key specified in the 'key' option.  The recursive pipeline
is responsible for processing the 'key' value and inserting the
'_recurser' key if it's a appropriate to recurse.

Assemble and register a transmogrifier with a list splitter section.

    >>> recurser = """
    ... [transmogrifier]
    ... pipeline =
    ...     initsource
    ...     inserter
    ...     recurser
    ...     printer
    ...     
    ... [initsource]
    ... blueprint = collective.blueprint.base.configsource
    ... 
    ... [inserter]
    ... blueprint = collective.transmogrifier.sections.inserter
    ... key = string:foo
    ... value = python:[['bar', 'baz'], ['qux', 'quux']]
    ... 
    ... [recurser]
    ... blueprint = collective.blueprint.base.recurser
    ... key = foo
    ... pipeline = foo
    ... 
    ... [foo]
    ... blueprint = collective.transmogrifier.sections.inserter
    ... condition = python:isinstance(item['foo'], list)
    ... key = string:_recurser
    ... value = item/foo
    ... 
    ... [printer]
    ... blueprint = collective.transmogrifier.sections.tests.pprinter
    ... """
    >>> registerConfig(
    ...     u'collective.blueprint.base.recurser.testing',
    ...     recurser)

Run the transmogrifier.

    >>> transmogrifier(
    ...     u'collective.blueprint.base.recurser.testing')
    {'_recurser': [['bar', 'baz'], ['qux', 'quux']],
     'foo': [['bar', 'baz'], ['qux', 'quux']]}
    {'_recurser': ['bar', 'baz'], 'foo': ['bar', 'baz']}
    {'foo': 'bar'}
    {'foo': 'baz'}
    {'_recurser': ['qux', 'quux'], 'foo': ['qux', 'quux']}
    {'foo': 'qux'}
    {'foo': 'quux'}

This transmogrifier uses the before option.

    >>> recurser = """
    ... [transmogrifier]
    ... pipeline =
    ...     initsource
    ...     inserter
    ...     recurser
    ...     printer
    ...     
    ... [initsource]
    ... blueprint = collective.blueprint.base.configsource
    ... 
    ... [inserter]
    ... blueprint = collective.transmogrifier.sections.inserter
    ... key = string:foo
    ... value = python:[['bar', 'baz'], ['qux', 'quux']]
    ... 
    ... [recurser]
    ... blueprint = collective.blueprint.base.recurser
    ... key = foo
    ... pipeline = foo
    ... before = True
    ... 
    ... [foo]
    ... blueprint = collective.transmogrifier.sections.inserter
    ... condition = python:isinstance(item['foo'], list)
    ... key = string:_recurser
    ... value = item/foo
    ... 
    ... [printer]
    ... blueprint = collective.transmogrifier.sections.tests.pprinter
    ... """
    >>> registerConfig(
    ...     u'collective.blueprint.base.recurser.testing2',
    ...     recurser)

    >>> transmogrifier(
    ...     u'collective.blueprint.base.recurser.testing2')
    {'foo': 'bar'}
    {'foo': 'baz'}
    {'_recurser': ['bar', 'baz'], 'foo': ['bar', 'baz']}
    {'foo': 'qux'}
    {'foo': 'quux'}
    {'_recurser': ['qux', 'quux'], 'foo': ['qux', 'quux']}
    {'_recurser': [['bar', 'baz'], ['qux', 'quux']],
     'foo': [['bar', 'baz'], ['qux', 'quux']]}
