"""
"""

from twisted.trial import unittest
from twisted.python import failure
from twisted.internet import defer, reactor, protocol
from twisted.test.proto_helpers import StringTransport, StringIOWithoutClosing

from rtmpy import server, exc
from rtmpy.protocol.rtmp import message, ExtraResult


class SimpleApplication(object):
    """
    An L{server.IApplication} that returns a deferred for all that it can.
    """

    factory = None
    name = None
    client = None

    ret = None
    reject = False

    def __init__(self):
        self.events = []

    def _add_event(self, name, args, kwargs):
        self.events.append((name, args, kwargs))

    def startup(self, *args, **kwargs):
        self._add_event('startup', args, kwargs)

        return self.ret

    def shutdown(self, *args, **kwargs):
        self._add_event('shutdown', args, kwargs)

        return self.ret

    def buildClient(self, *args, **kwargs):
        self._add_event('build-client', args, kwargs)

        return self.client

    def onConnect(self, *args, **kwargs):
        self._add_event('connect', args, kwargs)

        return not self.reject

    def onConnectAccept(self, *args, **kwargs):
        self._add_event('connect-accept', args, kwargs)

    def onConnectReject(self, *args, **kwargs):
        self._add_event('connect-reject', args, kwargs)

    def acceptConnection(self, *args, **kwargs):
        self._add_event('accept-connection', args, kwargs)

    def onAppStart(self, *args, **kwargs):
        self._add_event('app-start', args, kwargs)


class ApplicationRegisteringTestCase(unittest.TestCase):
    """
    Tests for L{server.ServerFactory.registerApplication}
    """

    def setUp(self):
        self.factory = server.ServerFactory()
        self.app = SimpleApplication()

    def test_create(self):
        """
        Test initial args for L{server.ServerFactory}
        """
        self.factory = server.ServerFactory({'foo': self.app})

        self.assertEqual(self.factory.applications, {'foo': self.app})

        d = self.app.ret = defer.Deferred()

        self.factory = server.ServerFactory({'foo': self.app})

        self.assertEqual(self.factory.applications, {})

        def cb(res):
            self.assertEqual(self.factory.applications, {'foo': self.app})

        reactor.callLater(0, d.callback, None)

    def test_invalid_pending(self):
        """
        Pending applications cannot be registered twice.
        """
        self.factory._pendingApplications['foo'] = None

        self.assertRaises(exc.InvalidApplication,
            self.factory.registerApplication, 'foo', None)

    def test_invalid_active(self):
        """
        Active applications cannot be registered twice.
        """
        self.factory.applications['foo'] = None

        self.assertRaises(exc.InvalidApplication,
            self.factory.registerApplication, 'foo', None)

    def test_deferred_startup(self):
        """
        Registering an application can be paused whilst the app is startup is
        called.
        """
        d = self.app.ret = defer.Deferred()
        ret = self.factory.registerApplication('foo', self.app)

        self.assertIsInstance(ret, defer.Deferred)
        self.assertEqual(self.app.factory, None)
        self.assertEqual(self.app.name, None)
        self.assertTrue('foo' in self.factory._pendingApplications)
        self.assertFalse('foo' in self.factory.applications)

        def cb(res):
            self.assertEqual(res, None)

            self.assertIdentical(self.app.factory, self.factory)
            self.assertEqual(self.app.name, 'foo')
            self.assertFalse('foo' in self.factory._pendingApplications)
            self.assertTrue('foo' in self.factory.applications)

        ret.addCallback(cb)

        reactor.callLater(0, d.callback, None)

        return ret

    def test_failed_deferred(self):
        """
        An error in app.startup should stop the registering process
        """
        def blowup():
            raise RuntimeError

        self.patch(self.app, 'startup', blowup)

        ret = self.factory.registerApplication('foo', self.app)

        self.assertIsInstance(ret, defer.Deferred)

        def eb(fail):
            fail.trap(RuntimeError)

            self.assertEqual(self.app.factory, None)
            self.assertEqual(self.app.name, None)
            self.assertFalse('foo' in self.factory._pendingApplications)
            self.assertFalse('foo' in self.factory.applications)

        ret.addErrback(eb)

        return ret


class ApplicationUnregisteringTestCase(unittest.TestCase):
    """
    Tests for L{server.ServerFactory.unregisterApplication}
    """

    def setUp(self):
        self.factory = server.ServerFactory()
        self.app = SimpleApplication()

    def test_not_registered(self):
        """
        Unregistering an unknown app should error.
        """
        self.assertRaises(exc.InvalidApplication,
            self.factory.unregisterApplication, 'foo')

    def test_unregister_pending(self):
        """
        Unregistering a pending application should immediately succeed.
        """
        # this never gets its callback fired, meaning that after registering
        # the application, it is considered pending.
        self.app.ret = defer.Deferred()

        self.factory.registerApplication('foo', self.app)

        self.assertTrue('foo' in self.factory._pendingApplications)

        d = self.factory.unregisterApplication('foo')

        def cb(res):
            self.assertIdentical(res, self.app)

        d.addCallback(cb)

        return d

    def test_simple_unregister(self):
        """
        app.shutdown doesn't need to return a deferred
        """
        self.factory.registerApplication('foo', self.app)

        ret = self.factory.unregisterApplication('foo')

        self.assertIsInstance(ret, defer.Deferred)

        def cb(res):
            self.assertIdentical(res, self.app)

            self.assertEqual(self.app.factory, None)
            self.assertEqual(self.app.name, None)
            self.assertFalse('foo' in self.factory._pendingApplications)
            self.assertFalse('foo' in self.factory.applications)

        ret.addCallback(cb)

        return ret

    def test_deferred(self):
        """
        app.shutdown can return a deferred
        """
        self.factory.registerApplication('foo', self.app)
        d = self.app.ret = defer.Deferred()

        ret = self.factory.unregisterApplication('foo')

        self.assertIsInstance(ret, defer.Deferred)

        def cb(res):
            self.assertIdentical(res, self.app)

            self.assertEqual(self.app.factory, None)
            self.assertEqual(self.app.name, None)
            self.assertFalse('foo' in self.factory._pendingApplications)
            self.assertFalse('foo' in self.factory.applications)

        ret.addCallback(cb)

        reactor.callLater(0, d.callback, None)

        return ret

    def test_deferred_failure(self):
        """
        Removing the app from the factory should not fail due to app.shutdown
        erroring.
        """
        self.factory.registerApplication('foo', self.app)

        d = self.app.ret = defer.Deferred()

        def boom(res):
            self.executed = True

            raise RuntimeError

        d.addCallback(boom)

        ret = self.factory.unregisterApplication('foo')

        self.assertIsInstance(ret, defer.Deferred)

        def cb(res):
            self.assertIdentical(res, self.app)
            self.assertTrue(self.executed)

            self.assertEqual(self.app.factory, None)
            self.assertEqual(self.app.name, None)
            self.assertFalse('foo' in self.factory._pendingApplications)
            self.assertFalse('foo' in self.factory.applications)

        ret.addCallback(cb)

        reactor.callLater(0, d.callback, None)

        return ret


class ServerFactoryTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        self.factory = server.ServerFactory()
        self.protocol = self.factory.buildProtocol(None)

        self.protocol.connectionMade()
        self.protocol.handshakeSuccess('')


class ConnectingTestCase(unittest.TestCase):
    """
    Tests all facets of connecting to an RTMP server.
    """

    def setUp(self):
        self.file = StringIOWithoutClosing()
        self.transport = protocol.FileWrapper(self.file)

        self.factory = server.ServerFactory()
        self.protocol = self.factory.buildProtocol(None)

        self.protocol.factory = self.factory

        self.protocol.transport = self.transport
        self.protocol.connectionMade()
        self.protocol.handshakeSuccess('')

        self.messages = []

        def send_message(*args):
            self.messages.append(args)

        self.patch(self.protocol, 'sendMessage', send_message)

        self.control = self.protocol.getStream(0)

    def assertStatus(self, code=None, description=None, level='status'):
        """
        Ensures that a status message has been sent.
        """
        stream, msg, whenDone = self.messages.pop(0)

        self.assertEqual(self.messages, [])

        self.assertIdentical(stream, self.control)
        self.assertEqual(whenDone, None)

        self.assertIsInstance(msg, message.Invoke)
        self.assertEqual(msg.name, 'onStatus')

        _, args = msg.argv

        self.assertEqual(_, None)

        if code is not None:
            self.assertEqual(args['code'], code)

        if description is not None:
            self.assertEqual(args['description'], description)

        self.assertEqual(args['level'], level)

    def assertErrorStatus(self, code=None, description=None):
        """
        Ensures that a status message has been sent.
        """
        if code is None:
            code = 'NetConnection.Connect.Failed'

        if description is None:
            description = 'Internal Server Error'

        self.assertStatus(code, description, 'error')

    def assertMessage(self, msg, type_, **state):
        """
        Ensure that the msg is of a particular type and state
        """
        self.assertEqual(msg.RTMP_TYPE, type_)

        d = msg.__dict__

        for k, v in state.copy().iteritems():
            self.assertEqual(v, d[k])
            del state[k]

        self.assertEqual(state, {})

    def connect(self, packet):
        return self.control.onConnect(packet)

    def test_invokable_target(self):
        self.assertEqual(self.control.getInvokableTarget('connect'),
            self.control.onConnect)

    def test_invoke(self):
        """
        Make sure that invoking connect call self.protocol.onConnect
        """
        my_args = {'foo': 'bar'}
        self.executed = False

        def connect(args):
            self.executed = True
            self.assertEqual(args, my_args)

        self.patch(self.protocol, 'onConnect', connect)

        d = self.control.onInvoke('connect', 0, [my_args], 0)

        return d

    def test_missing_app_key(self):
        """
        RTMP connect packets contain {'app': 'name_of_app'}.
        """
        d = self.connect({})

        def cb(res):
            self.assertEqual(res, {
                'code': 'NetConnection.Connect.Failed',
                'description': "Bad connect packet (missing 'app' key)",
                'level': 'error'
            })

        d.addCallback(cb)

        return d

    def test_random_failure(self):
        """
        If something random goes wrong, make sure the status is correctly set.
        """
        def bork(*args):
            raise EnvironmentError('woot')

        self.patch(self.protocol, '_onConnect', bork)

        d = self.connect({})

        def cb(res):
            self.assertEqual(res, {
                'code': 'NetConnection.Connect.Failed',
                'description': 'woot',
                'level': 'error'
            })


        d.addCallback(cb)

        return d

    def test_unknown_application(self):
        self.assertEqual(self.factory.getApplication('what'), None)

        d = self.connect({'app': 'what'})

        def cb(res):
            self.assertEqual(res, {
                'code': 'NetConnection.Connect.InvalidApp',
                'description': "Unknown application 'what'",
                'level': 'error'
            })

        d.addCallback(cb)

        return d

    def test_success(self):
        """
        Ensure a successful connection
        """
        a = self.factory.applications['what'] = SimpleApplication()

        d = self.connect({'app': 'what'})

        def check_status(res):
            self.assertIsInstance(res, ExtraResult)
            self.assertEqual(res.extra, {
                'capabilities': 31, 'fmsVer': 'FMS/3,5,1,516', 'mode': 1})
            self.assertEqual(res.result, {
                'code': 'NetConnection.Connect.Success',
                'objectEncoding': 0,
                'description': 'Connection succeeded.',
                'level': 'status'
            })

            msg, = self.messages.pop(0)

            self.assertMessage(msg, message.DOWNSTREAM_BANDWIDTH,
                bandwidth=2500000L)

            msg, = self.messages.pop(0)

            self.assertMessage(msg, message.UPSTREAM_BANDWIDTH,
                bandwidth=2500000L, extra=2)

            msg, = self.messages.pop(0)

            self.assertMessage(msg, message.CONTROL,
                type=0, value1=0)

            self.assertEqual(self.messages, [])

        d.addCallback(check_status)

        self.protocol.onDownstreamBandwidth(2000, 2)

        return d

    def test_reject(self):
        a = self.factory.applications['what'] = SimpleApplication()
        a.reject = True
        a.client = object()

        d = self.connect({'app': 'what'})

        def check_status(res):
            self.assertEqual(res, {
                'code': 'NetConnection.Connect.Rejected',
                'level': 'error',
                'description': 'Authorization is required'
            })

            self.assertEqual(self.messages, [])

            name, args, kwargs = a.events.pop()

            self.assertEqual(name, 'connect-reject')
            self.assertIdentical(args[0], a.client)
            self.assertEqual(len(args), 2)
            self.assertEqual(kwargs, {})

        d.addCallback(check_status)

        return d
