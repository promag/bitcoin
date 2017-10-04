#!/usr/bin/env python3
# Copyright (c) 2015-2016 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test the ZMQ notification interface."""
import configparser
import os
import struct

from test_framework.test_framework import BitcoinTestFramework, SkipTest
from test_framework.util import (assert_equal,
                                 bytes_to_hex_str,
                                 hash256,
                                )

class ZMQSubscriber:
    def __init__(self, socket, address):
        self.address = address
        self.socket = socket
        self.sequence = 0

class ZMQTest (BitcoinTestFramework):
    def set_test_params(self):
        self.address = "tcp://127.0.0.1:28332"
        self.num_blocks = 5
        self.num_nodes = 2
        self.subscribers = {}

    def subscribe(self, type):
        import zmq
        self.socket.setsockopt(zmq.SUBSCRIBE, type.encode('latin-1'))
        self.subscribers[type] = ZMQSubscriber(self.socket, self.address)

    def receive(self, type):
        subscriber = self.subscribers[type]
        topic, body, seq = subscriber.socket.recv_multipart()
        # Topic should match the subscriber type.
        assert_equal(topic, type.encode('latin-1'))
        # Sequence should be incremental.
        assert_equal(struct.unpack('<I', seq)[-1], subscriber.sequence)
        subscriber.sequence += 1
        return body

    def setup_nodes(self):
        # Try to import python3-zmq. Skip this test if the import fails.
        try:
            import zmq
        except ImportError:
            raise SkipTest("python3-zmq module not available.")

        # Check that bitcoin has been built with ZMQ enabled.
        config = configparser.ConfigParser()
        if not self.options.configfile:
            self.options.configfile = os.path.dirname(__file__) + "/../config.ini"
        config.read_file(open(self.options.configfile))

        if not config["components"].getboolean("ENABLE_ZMQ"):
            raise SkipTest("bitcoind has not been built with zmq enabled.")

        # Initialize ZMQ context and socket.
        # At the moment all messages are received in the same socket which means
        # that this test fails if the publishing order changes.
        # Note that the publishing order is not defined in the documentation and
        # is subject to change.
        self.zmq_context = zmq.Context()
        self.socket = self.zmq_context.socket(zmq.SUB)
        self.socket.set(zmq.RCVTIMEO, 60000)
        self.socket.connect(self.address)

        # Subscribe to all available topics.
        self.subscribe("hashblock")
        self.subscribe("hashtx")
        self.subscribe("rawblock")
        self.subscribe("rawtx")

        self.extra_args = [["-zmqpub%s=%s" % (type, sub.address) for type, sub in self.subscribers.items()], []]
        self.add_nodes(self.num_nodes, self.extra_args)
        self.start_nodes()

    def run_test(self):
        try:
            self._zmq_test()
        finally:
            # Destroy the ZMQ context.
            self.log.debug("Destroying ZMQ context")
            self.zmq_context.destroy(linger=None)

    def _zmq_test(self):
        self.log.info("Generate %(n)d blocks (and %(n)d coinbase txes)" % {"n": self.num_blocks})
        genhashes = self.nodes[0].generate(self.num_blocks)
        self.sync_all()

        for x in range(self.num_blocks):
            # Should receive the coinbase txid.
            txid = self.receive("hashtx")

            # Should receive the coinbase raw transaction.
            hex = self.receive("rawtx")
            assert_equal(hash256(hex), txid)

            # Should receive the generated block hash.
            hash = bytes_to_hex_str(self.receive("hashblock"))
            assert_equal(genhashes[x], hash)
            # The block should only have the coinbase txid.
            assert_equal([bytes_to_hex_str(txid)], self.nodes[1].getblock(hash)["tx"])

            # Should receive the generated raw block.
            block = self.receive("rawblock")
            assert_equal(genhashes[x], bytes_to_hex_str(hash256(block[:80])))

        self.log.info("Wait for tx from second node")
        payment_txid = self.nodes[1].sendtoaddress(self.nodes[0].getnewaddress(), 1.0)
        self.sync_all()

        # Should receive the broadcasted txid.
        txid = self.receive("hashtx")
        assert_equal(payment_txid, bytes_to_hex_str(txid))

        # Should receive the broadcasted raw transaction.
        hex = self.receive("rawtx")
        assert_equal(payment_txid, bytes_to_hex_str(hash256(hex)))

if __name__ == '__main__':
    ZMQTest().main()
