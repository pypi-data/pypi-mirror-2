.. -*-doctest-*-

Blueprint Base Classes
======================

The collective.blueprint.base package provides base classes for
clear and easy transmogrifier blueprints.

Changing Keys
-------------

For blueprints that add or change keys in items, it can be very useful
to make the keys used by the blueprint configurable.

The getKeys functions translates the keys and values passed as keyword
arguments into a dictionary with keys as specified in the options if
present.

    >>> from collective.blueprint.base import keys
    >>> options = {'foo-key': 'baz'}
    >>> sorted(keys.getKeys(
    ...     options, foo='bar', bah='qux').iteritems())
    [('bah', 'qux'), ('baz', 'bar')]

A base class is provided for easily making readable blueprints that
add keys to items or change keys obeying any key names in the
options.

    >>> from collective.blueprint.base import blueprint
    >>> class FooBlueprint(blueprint.KeyChanger):
    ...     keys = ('foo', 'bah')
    ...     def processItem(self, item):
    ...         return dict(foo='bar', bah='qux')

    >>> from collective.blueprint.base import testing
    >>> transmogrifier = testing.Transmogrifier()
    >>> previous = ({'other': 'stuff'},)
    >>> foo_blueprint = FooBlueprint(
    ...     transmogrifier, 'foosection', options, previous)
    >>> item, = foo_blueprint
    >>> sorted(item.iteritems())
    [('bah', 'qux'), ('baz', 'bar'), ('other', 'stuff')]

Source blueprints are by their very nature key changers.  Intead of
adding keys to items from further up the pipeline, they generate
items.  The source base class extends the behavior above to this usage
pattern.

    >>> class BarBlueprint(blueprint.Source):
    ...     keys = ('foo', 'bah')
    ...     def getItems(self):
    ...         yield dict(foo='bar', bah='qux')
    ...         yield dict(foo='bar2', bah='qux2')

    >>> previous = ({'other': 'stuff'},)
    >>> bar_blueprint = BarBlueprint(
    ...     transmogrifier, 'barsection', options, previous)
    >>> other, first, second = bar_blueprint
    >>> other
    {'other': 'stuff'}
    >>> sorted(first.iteritems())
    [('bah', 'qux'), ('baz', 'bar')]
    >>> sorted(second.iteritems())
    [('bah', 'qux2'), ('baz', 'bar2')]

Using Keys
----------

For blueprints that access keys in items and process them somehow,
transmogrifier provides support for matchers that will access keys
on items according to a policy of precedence.

The makeMatchers function does this for multiple keys at once.

    >>> options = {'blueprint': 'foo.blueprint', 'bah-key': 'bar'}
    >>> matchers = keys.makeMatchers(
    ...     options, 'barsection', 'baz', 'bah', blah=('qux', 'quux'))
    >>> sorted(matchers.iteritems())
    [('bah', <collective.transmogrifier.utils.Matcher object at ...>),
     ('baz', <collective.transmogrifier.utils.Matcher object at ...>),
     ('blah', <collective.transmogrifier.utils.Matcher object at ...>)]
     
    >>> item = {'_baz': 'baz-value',
    ...         'bar': 'bah-value',
    ...         'quux': 'blah-value'}
    >>> matchers['baz'](*item)
    ('_baz', True)
    >>> matchers['bah'](*item)
    ('bar', True)
    >>> matchers['blah'](*item)
    ('quux', True)

To make implementing blueprints easier and clearer, a base class is
provided that allows the blueprint author to worry only about the keys
in the item they require.

    >>> class BazKeyUser(blueprint.KeyUser):
    ...     keys = ('baz', 'bah')
    ...     extras = dict(blah=('qux', 'quux'))
    ...     def processItem(self, item, baz, bah, blah):
    ...         print baz, bah, blah

    >>> previous = (item,)
    >>> baz_blueprint = BazKeyUser(
    ...     transmogrifier, 'bazsection', options, previous)
    >>> only, = baz_blueprint
    baz-value bah-value blah-value
    >>> sorted(only.iteritems())
    [('_baz', 'baz-value'),
     ('bar', 'bah-value'),
     ('quux', 'blah-value')]

A KeyUser can pass over items that don't have keys for all the
matchers if the required option is not True.

    >>> class QuxKeyUser(blueprint.KeyUser):
    ...     keys = ('baz', 'bah', 'foo')
    ...     extras = dict(blah=('qux', 'quux'))
    ...     def processItem(self, item, baz, bah, blah, foo):
    ...         print baz, bah, blah

    >>> options['required'] = 'False'
    >>> previous = (item,)
    >>> qux_blueprint = QuxKeyUser(
    ...     transmogrifier, 'quxsection', options, previous)
    >>> only, = qux_blueprint
    >>> sorted(only.iteritems())
    [('_baz', 'baz-value'),
     ('bar', 'bah-value'),
     ('quux', 'blah-value')]
