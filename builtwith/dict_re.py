"""
library to perform bulk regular expression matching.
"""
import re2 as re

def _make_names(vals):
    """
    generate unique valid python identifiers for iterator

    >>> list(_make_names([0, 1, 2]))
    [('n_0', 0), ('n_1', 1), ('n_2', 2)]
    """
    for idx, val in enumerate(vals):
        yield ('n_' + str(idx), val)


def _rexify(val):
    """ turn 'val' into a regular expression """
    if isinstance(val, list):
        # wrap 'v' in non-binding group to ensure proper '|'
        return '|'.join(r'(?:%s)' % (v, ) for v in val if v)
    else:
        return val


def chain_patterns(dct, flags=re.I):
    """
    create combined regexes matcher.

    dct is of form {"name": "pattern" | ["pattern"]}.
    patterns are not escaped, so they have to be valid regex.

    returns a matcher that will return an iterator of match objects.

    NOTE: this function does not return overlapping patterns.
    if needed, overlapping matches could be supported using `(?=(...))`
        or `regex.finditer(..., overlapped=True)`

    >>> list(chain_patterns({'pattern1': r'ab.cdf?', 'pattern2': r'e[fh]gh$|xxx', 'pattern3': 'xyz'})('dabbcdefgh'))
    [{'pattern1': 'abbcd'}, {'pattern2': 'efgh'}]
    """
    items = dct.items()

    # creating forward and reverse lookup, since match names have to be
    #   valid python identifiers
    reverse = {name:item[0] for name, item in _make_names(items)}
    forward = {v:k for k, v in reverse.items()}
    rules = [r'(?P<%s>%s)' % (forward[k], _rexify(v))
             for k, v in items if v]
    rex = re.compile('|'.join(rules), flags=flags)

    def finder(string):
        # overwriting multiple identical labels
        return {reverse[k]:v
                for match in rex.finditer(string)
                for k, v in match.groupdict().items()
                if v is not None}

    return finder

