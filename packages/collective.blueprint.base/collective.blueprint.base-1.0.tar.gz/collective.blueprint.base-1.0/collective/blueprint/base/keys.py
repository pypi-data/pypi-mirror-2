from collective.transmogrifier import utils as transmog_utils

def getKeys(options, **keys):
    """Remap keys according to options if present"""
    return dict(
        (options.get(key+'-key', key), value)
        for key, value in keys.iteritems())

def makeMatchers(options, section, *keys, **extras):
    matchers = {}

    extras.update(
        extras.fromkeys(keys, ()))

    for key, extra in extras.iteritems():

        # Allow extra to be None or False
        if not extra:
            extra = ()
            
        optionname = key+'-key'
        matchers[key] = transmog_utils.defaultMatcher(
            options, optionname, section, key, extra)

    return matchers
