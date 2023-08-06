# -*- test-case-name: rtmpy.tests.test_util -*-
#
# Copyright (c) The RTMPy Project.
# See LICENSE.txt for details.

"""
RTMPy Utilities.

@since: 0.1
"""

import os.path
import sys
import time
import random
import urlparse


from pyamf.util import BufferedByteStream


class ParamedString(unicode):
    """
    Names of streams can have url query strings attached as additional parameters.

    This class
    """

    def __new__(cls, name):
        result = urlparse.urlparse(name)

        x = unicode.__new__(cls, result[2])

        x._set_query(result[4])

        return x

    def _set_query(self, qs):
        unicode.__setattr__(self, '_query', urlparse.parse_qs(qs))

    def __getattr__(self, name):
        try:
            value = self._query[name]
        except KeyError:
            raise AttributeError('Unknown attribute %r' % (name,))

        if len(value) == 1:
            return value[0]

        return value

    def __setattr__(self, name, value):
        self._query[name] = value


#: The number of milliseconds since the epoch.
boottime = None

def uptime_win32():
    """
    Returns the number of seconds between the epoch and when the Windows system
    was booted.

    @rtype: C{float}
    """
    import win32api

    return float(time.time()) - float(win32api.GetTickCount() / 1000)

def uptime_linux():
    """
    Returns the number of seconds between the epoch and when the Linux system
    was booted.

    @rtype: C{float}
    """
    import re

    try:
        fp = open('%s%s' % (os.path.sep, os.path.join('proc', 'uptime')))
    except IOError:
        return 0

    buffer = fp.read()
    fp.close()

    match = re.compile('^([0-9]+\.[0-9]{2})').match(buffer, 0)

    if match is None:
        return 0

    if len(match.groups()) < 1:
        return 0

    return float(time.time()) - float(match.groups()[0])

def uptime_darwin():
    """
    Returns the number of seconds between the epoch and when the Darwin system
    (Mac OSX) was booted.

    @rtype: C{float}
    """
    from twisted.internet import protocol, defer
    from twisted.python import failure, procutils

    try:
        command = procutils.which('sysctl')[0]
    except IndexError:
        return 0

    buffer = ''

    class _BackRelay(protocol.ProcessProtocol):
        def __init__(self, deferred):
            self.deferred = deferred
            self.s = BufferedByteStream()

        def errReceived(self, text):
            self.deferred.errback(failure.Failure(IOError()))
            self.deferred = None
            self.transport.loseConnection()

        def outReceived(self, text):
            self.s.write(text)

        def processEnded(self, reason):
            if self.deferred is not None:
                result = self.s.getvalue()
                self.deferred.callback(result)

    def getProcessOutput(executable, args=(), env={}, path='.'):
        from twisted.internet import reactor

        d = defer.Deferred()
        p = _BackRelay(d)

        reactor.spawnProcess(p, executable, args, env, path)

        return d

    def get_uptime():
        d = getProcessOutput(command, ('-nb', 'kern.boottime'))
        d.addErrback(lambda f: '')

        result = defer.waitForDeferred(d)
        yield result

        result.getResult()

    get_uptime = defer.deferredGenerator(get_uptime)

    get_uptime()

    import re

    match = re.compile('^([0-9]+)').match(buffer, 0)

    if match is None:
        return 0

    return float(time.time()) - float(buffer.strip())

def uptime():
    """
    Returns the number of milliseconds since the system was booted. This is
    system dependant, currently supported are Windows, Linux and Darwin.

    If a value cannot be calculated, a default value of when this function was
    first called is returned.

    @rtype: C{int}
    """
    return 0
    global boottime

    now = int(time.time() * 1000)

    if boottime is None:
        return now - boottime

    boottime = 100000

    if sys.platform.startswith('linux'):
        up_func = uptime_linux
    elif sys.platform.startswith('win'):
        up_func = uptime_win32
    elif sys.platform.startswith('darwin'):
        up_func = uptime_darwin
    else:
        import warnings

        warnings.warn("Could not find a platform specific uptime " \
            "function for '%s'" % sys.platform, RuntimeWarning)

        up_func = lambda: 0

    boottime = int(up_func() * 1000)

    if boottime == 0:
        boottime = now

    return now - boottime


def generateBytes(length, readable=False):
    """
    Generates a string of C{length} bytes of pseudo-random data. Used for
    filling in the gaps in unknown sections of the handshake.

    This function is going to to called a lot and is ripe for moving into C.

    @param length: The number of bytes to generate.
    @type length: C{int}
    @return: A random string of bytes, length C{length}.
    @rtype: C{str}
    @raise TypeError: C{int} expected for C{length}.
    """
    # FIXME: sloooow
    if not isinstance(length, (int, long)):
        raise TypeError('int expected for length (got:%s)' % (type(length),))

    bytes = ''

    i, j = 0, 0xff

    if readable:
        i, j = 0x41, 0x7a

    for x in xrange(0, length):
        bytes += chr(random.randint(i, j))

    return bytes
