# vim: set fileencoding=utf8 :

from __future__ import division

import math
from functools import wraps
from time import time

import numpy
from numpy import uint8, cast

from twisted.internet.defer import Deferred

# Coord handling.

def split_coords(x, z):
    """
    Split a pair of coordinates into chunk and subchunk coordinates.

    :param int x: the X coordinate
    :param int z: the Z coordinate

    :returns: a tuple of the X chunk, X subchunk, Z chunk, and Z subchunk
    """

    first, second = divmod(int(x), 16)
    third, fourth = divmod(int(z), 16)

    return first, second, third, fourth

def taxicab2(x1, y1, x2, y2):
    """
    Return the taxicab distance between two blocks.
    """

    return abs(x1 - x2) + abs(y1 - y2)

# Bit twiddling.

def unpack_nibbles(l):
    """
    Unpack bytes into pairs of nibbles.

    Nibbles are half-byte quantities. The nibbles unpacked by this function
    are returned as unsigned numeric values.

    >>> unpack_nibbles("a")
    [6, 1]
    >>> unpack_nibbles("nibbles")
    [6, 14, 6, 9, 6, 2, 6, 2, 6, 12, 6, 5, 7, 3]

    :param list l: bytes

    :returns: list of nibbles
    """
    data = numpy.fromstring(l, dtype=uint8)
    return numpy.dstack((data & 0xf, data >> 4)).flat

def pack_nibbles(a):
    """
    Pack pairs of nibbles into bytes.

    Bytes are returned as characters.

    :param `ndarray` a: nibbles to pack

    :returns: packed nibbles as a string of bytes
    """

    a = a.reshape(-1, 2)
    if a.dtype != uint8:
        a = cast[uint8](a)
    return ((a[:, 1] << 4) | a[:, 0]).tostring()

# Trig.

def rotated_cosine(x, y, theta, lambd):
    r"""
    Evaluate a rotated 3D sinusoidal wave at a given point, angle, and
    wavelength.

    The function used is:

    .. math::

       f(x, y) = -\cos((x \cos\theta - y \sin\theta) / \lambda) / 2 + 1

    This function has a handful of useful properties; it has a local minimum
    at f(0, 0) and oscillates infinitely betwen 0 and 1.

    :param float x: X coordinate
    :param float y: Y coordinate
    :param float theta: angle of rotation
    :param float lambda: wavelength

    :returns: float of f(x, y)
    """

    return -math.cos((x * math.cos(theta) - y * math.sin(theta)) / lambd) / 2 + 1

# Decorators.

timers = {}

def timed(f):
    timers[f] = (0, 0)
    @wraps(f)
    def deco(*args, **kwargs):
        before = time()
        retval = f(*args, **kwargs)
        after = time()
        count, average = timers[f]
        # MMA
        average = (9 * average + after - before) / 10
        count += 1
        if not count % 10:
            print "Average time for %s: %dms" % (f, average * 1000)
        timers[f] = (count, average)
        return retval
    return deco

# Colorizers.

chat_colors = [
    u"§0", # black
    u"§1", # dark blue
    u"§2", # dark green
    u"§3", # dark cyan
    u"§4", # dark red
    u"§5", # dark magenta
    u"§6", # dark orange
    u"§7", # gray
    u"§8", # dark gray
    u"§9", # blue
    u"§a", # green
    u"§b", # cyan
    u"§c", # red
    u"§d", # magenta
    u"§e", # yellow
]

console_colors = {
    u"§0": "\x1b[1;30m", # black        -> bold black
    u"§1": "\x1b[34m",   # dark blue    -> blue
    u"§2": "\x1b[32m",   # dark green   -> green
    u"§3": "\x1b[36m",   # dark cyan    -> cyan
    u"§4": "\x1b[31m",   # dark red     -> red
    u"§5": "\x1b[35m",   # dark magenta -> magenta
    u"§6": "\x1b[33m",   # dark orange  -> yellow
    u"§7": "\x1b[1;37m", # gray         -> bold white
    u"§8": "\x1b[37m",   # dark gray    -> white
    u"§9": "\x1b[1;34m", # blue         -> bold blue
    u"§a": "\x1b[1;32m", # green        -> bold green
    u"§b": "\x1b[1;36m", # cyan         -> bold cyan
    u"§c": "\x1b[1;31m", # red          -> bold red
    u"§d": "\x1b[1;35m", # magenta      -> bold magenta
    u"§e": "\x1b[1;33m", # yellow       -> bold yellow
}

def chat_name(s):
    return "%s%s%s" % (
        chat_colors[hash(s) % len(chat_colors)], s, u"§f"
    )

def fancy_console_name(s):
    return "%s%s%s" % (
        console_colors[chat_colors[hash(s) % len(chat_colors)]],
        s,
        '\x1b[0m'
    )

def sanitize_chat(s):
    """
    Verify that the given chat string is safe to send to Notchian recepients.
    """

    # Check for Notchian bug: Color controls can't be at the end of the
    # message.
    if len(s) > 1 and s[-2] == u"§":
        s = s[:-2]

    return s

# Time manglers.

def split_time(timestamp):
    """
    Turn an MC timestamp into hours and minutes.

    The time is calculated by interpolating the MC clock over the standard
    24-hour clock.

    :param int timestamp: MC timestamp, in the range 0-24000
    :returns: a tuple of hours and minutes on the 24-hour clock
    """

    # 24000 ticks per day
    hours, minutes = divmod(timestamp, 1000)

    # 6:00 on a Christmas morning
    hours = (hours + 6) % 24
    minutes = minutes * 6 // 100

    return hours, minutes

# Deferreds.

def fork_deferred(d):
    """
    Fork a Deferred.

    Returns a Deferred which will fire when the reference Deferred fires, with
    the same arguments, without disrupting or changing the reference Deferred.
    """

    forked = Deferred()
    d.chainDeferred(forked)
    return forked
