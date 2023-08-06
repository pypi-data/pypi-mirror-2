#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
import time
import re
import base64
import ssl

from xml.etree.ElementTree import XML

from pyxmpp2.streambase import StreamBase
from pyxmpp2.streamtls import StreamTLSHandler
from pyxmpp2.streamevents import *
from pyxmpp2.exceptions import TLSNegotiationFailed
from pyxmpp2.jid import JID
from pyxmpp2.settings import XMPPSettings

from test_util import EventRecorder, InitiatorSelectTestCase

C2S_SERVER_STREAM_HEAD = '<stream:stream version="1.0" from="server.example.org" xmlns:stream="http://etherx.jabber.org/streams" xmlns="jabber:client">'
C2S_CLIENT_STREAM_HEAD = '<stream:stream version="1.0" to="server.example.org" xmlns:stream="http://etherx.jabber.org/streams" xmlns="jabber:client">'

TLS_FEATURES = """<stream:features>
     <starttls xmlns='urn:ietf:params:xml:ns:xmpp-tls' />
</stream:features>"""
TLS_REQUIRED_FEATURES = """<stream:features>
     <starttls xmlns='urn:ietf:params:xml:ns:xmpp-tls'>
        <required />
     </starttls>
</stream:features>"""


EMPTY_FEATURES = """<stream:features/>"""

PROCEED = "<proceed xmlns='urn:ietf:params:xml:ns:xmpp-tls' />"

STREAM_TAIL = '</stream:stream>'
        
class TestInitiator(InitiatorSelectTestCase):
    def test_enabled_optional(self):
        """Test TLS enabled in settings, and optional on the server."""
        settings = XMPPSettings({
                                u"starttls": True, 
                                u"tls_cacert_file": "data/ca.pem", 
                                })
        handler = EventRecorder()
        handlers = [StreamTLSHandler(settings), handler]
        self.stream = StreamBase(u"jabber:client", None, handlers, settings)
        self.start_transport(handlers)
        self.stream.initiate(self.transport, to = "server.example.org")
        self.connect_transport()
        self.server.write(C2S_SERVER_STREAM_HEAD)
        self.server.write(TLS_FEATURES)
        xml = self.wait(2, expect = re.compile(r".*(<starttls.*/>)"))
        self.assertIsNotNone(xml)
        element = XML(xml)
        self.assertEqual(element.tag, 
                                "{urn:ietf:params:xml:ns:xmpp-tls}starttls")
        self.server.write(PROCEED)
        self.server.starttls(self.server.sock,
                                keyfile = "data/server-key.pem",
                                certfile = "data/server.pem",
                                server_side = True,
                                ca_certs = "data/ca.pem",
                                )
        stream_start = self.wait(expect = re.compile(
                                    r"(<stream:stream[^>]*>)"))
        self.assertIsNotNone(stream_start)
        self.assertTrue(self.stream.tls_established)
        self.stream.disconnect()
        self.server.write(C2S_SERVER_STREAM_HEAD)
        self.server.write(EMPTY_FEATURES)
        self.server.write(b"</stream:stream>")
        self.wait()
        event_classes = [e.__class__ for e in handler.events_received]
        self.assertEqual(event_classes, [ConnectingEvent,
                    ConnectedEvent, StreamConnectedEvent, GotFeaturesEvent,
                    TLSConnectingEvent, TLSConnectedEvent, StreamRestartedEvent,
                    GotFeaturesEvent, DisconnectedEvent])

    def no_test_enabled_required(self):
        """Test TLS enabled in settings, and required on the server."""
        addr, port = self.start_server()
        handler = EventRecorder()
        settings = XMPPSettings({
                                u"starttls": True, 
                                u"tls_cacert_file": "data/ca.pem", 
                                })
        stream = StreamBase(u"jabber:client", None, [StreamTLSHandler(settings), 
                                                            handler], settings)
        stream.connect(addr, port, to = "server.example.org")
        self.server.write(C2S_SERVER_STREAM_HEAD)
        self.server.write(TLS_REQUIRED_FEATURES)
        xml = self.loop(stream, timeout = 1, expect = re.compile(
                                           r".*(<starttls.*/>)"))
        self.assertIsNotNone(xml)
        element = XML(xml)
        self.assertEqual(element.tag, 
                                "{urn:ietf:params:xml:ns:xmpp-tls}starttls")
        self.server.write(PROCEED)
        self.server.starttls(self.server.sock,
                                keyfile = "data/server-key.pem",
                                certfile = "data/server.pem",
                                server_side = True,
                                ca_certs = "data/ca.pem",
                                )
        stream_start = self.loop(stream, timeout = 1, expect = re.compile(
                                                    r"(<stream:stream[^>]*>)"))
        self.assertIsNotNone(stream_start)
        self.assertTrue(stream.tls_established)
        stream.disconnect()
        self.server.write(C2S_SERVER_STREAM_HEAD)
        self.server.write(EMPTY_FEATURES)
        self.server.write(b"</stream:stream>")
        self.loop(stream)
        event_classes = [e.__class__ for e in handler.events_received]
        self.assertEqual(event_classes, [ResolvingAddressEvent, ConnectingEvent,
                    ConnectedEvent, StreamConnectedEvent, GotFeaturesEvent,
                    TLSConnectingEvent, TLSConnectedEvent, StreamRestartedEvent,
                    GotFeaturesEvent, DisconnectedEvent])

    def no_test_enabled_missing(self):
        """Test TLS enabled in settings, and missing on the server."""
        addr, port = self.start_server()
        handler = EventRecorder()
        settings = XMPPSettings({
                                u"starttls": True, 
                                u"tls_cacert_file": "data/ca.pem", 
                                })
        stream = StreamBase(u"jabber:client", None, [StreamTLSHandler(settings), 
                                                            handler], settings)
        stream.connect(addr, port, to = "server.example.org")
        self.server.write(C2S_SERVER_STREAM_HEAD)
        self.server.write(EMPTY_FEATURES)
        self.server.write(b"</stream:stream>")
        xml = self.loop(stream)
        self.assertFalse(stream.tls_established)
        stream.disconnect()
        self.loop(stream)
        event_classes = [e.__class__ for e in handler.events_received]
        self.assertEqual(event_classes, [ResolvingAddressEvent, ConnectingEvent,
                    ConnectedEvent, StreamConnectedEvent, GotFeaturesEvent,
                    DisconnectedEvent])

    def no_test_required_missing(self):
        """Test TLS required in settings, and missing on the server."""
        addr, port = self.start_server()
        handler = EventRecorder()
        settings = XMPPSettings({
                                u"starttls": True, 
                                u"tls_require": True, 
                                u"tls_cacert_file": "data/ca.pem", 
                                })
        stream = StreamBase(u"jabber:client", None, [StreamTLSHandler(settings), 
                                                            handler], settings)
        stream.connect(addr, port, to = "server.example.org")
        self.server.write(C2S_SERVER_STREAM_HEAD)
        self.server.write(EMPTY_FEATURES)
        self.server.write(b"</stream:stream>")
        with self.assertRaises(TLSNegotiationFailed):
            self.loop(stream)
        event_classes = [e.__class__ for e in handler.events_received]
        self.assertEqual(event_classes, [ResolvingAddressEvent, ConnectingEvent,
                    ConnectedEvent, StreamConnectedEvent, GotFeaturesEvent,
                    DisconnectedEvent])


def suite():
     suite = unittest.TestSuite()
     suite.addTest(unittest.makeSuite(TestInitiator))
     return suite

if __name__ == '__main__':
    import logging
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    unittest.TextTestRunner(verbosity=2).run(suite())

# vi: sts=4 et sw=4
