#!/usr/bin/env python3
# Copyright (c) 2017 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test blocknotify.

Verify that a bitcoind node calls the given command for each block
"""
from os import close, remove
from tempfile import mkstemp
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal, assert_raises_jsonrpc
from time import sleep

class BlockNotifyTest(BitcoinTestFramework):

    def __init__(self):
        super().__init__()

        # get a temporary file path to store the notified blocks
        (fd, path) = mkstemp(text = True)
        os.close(fd)

        self.path = path
        self.setup_clean_chain = False
        self.num_nodes = 1
        self.extra_args = [['-blocknotify=echo %%s >> %s' % path]]

    def run_test(self):
        # generate 5 blocks
        blocks = self.nodes[0].generate(5)
        sleep(1)

        # temporary file content should equal the generated blocks
        with open(self.path, 'r') as f:
            assert_equal(blocks, f.read().splitlines())
        
        # remove temporary file
        os.remove(self.path)

if __name__ == '__main__':
    BlockNotifyTest().main()
