#!/usr/bin/env python
from __future__ import division

__version__ = "$Revision: 320 $"

from functools import wraps
from itertools import count
import platform
import sys

import pkg_resources

_DESC_TEMPLATE = "%s (%s on %s: %s Python/%s)"
def _init_desc(template=_DESC_TEMPLATE):
    node = platform.node()
    platform_str = platform.platform()
    python_version = platform.python_version()

    package_name = __name__.partition(".")[0]
    package = pkg_resources.require(package_name)[0]
    package_version = package.version

    return template % (" ".join(sys.argv), package_version, node,
                       platform_str, python_version)

DESC = _init_desc()

def _correct_range_point(point, start):
    if point is None:
        return None
    else:
        return point - start

def correct_range(r, start):
    res_start = _correct_range_point(r.start, start)
    res_stop = _correct_range_point(r.stop, start)

    return slice(res_start, res_stop, r.step)

def enum(iterable, n=0):
    """
    returns dict such that seq[enum(seq)[name]] == name
    """
    return dict(zip(iterable, count(n)))

def die(message, returncode=1):
    print >>sys.stderr, message
    sys.exit(returncode)

def enabled(func):
    return func

def disabled_noop(func):
    @wraps(func)
    def noop(*args, **kwargs):
        pass

    return noop

def disabled_passthrough(func):
    @wraps(func)
    def passthrough(x):
        return x

    return passthrough

def passthrough(x):
    return x

def enable_if(condition, disabled=disabled_noop):
    if condition:
        return enabled
    else:
        return disabled

@enable_if(sys.stderr.isatty())
def progress(text, *args):
    print >>sys.stderr, text % tuple(args)

@enable_if(sys.stderr.isatty(), disabled_passthrough)
def progress_iter(it, describe_func=passthrough):
    for index, item in enumerate(it):
        progress("%d: %s", index, describe_func(item))

        yield item

class FastaIterator(object):
    def __init__(self, handle):
        self._handle = handle
        self._defline = None

    def __iter__(self):
        return self

    def next(self):
        lines = []
        defline_old = self._defline

        while 1:
            line = self._handle.readline()
            if not line:
                if not defline_old and not lines:
                    raise StopIteration
                if defline_old:
                    self._defline = None
                    break
            elif line[0] == '>':
                self._defline = line[1:].rstrip()
                if defline_old or lines:
                    break
                else:
                    defline_old = self._defline
            else:
                lines.append(line.rstrip())

        return defline_old, ''.join(lines)

def main(args):
    pass

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
