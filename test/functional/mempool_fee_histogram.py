#!/usr/bin/env python3
# Copyright (c) 2019 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test mempool fee histogram."""

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import (
    assert_equal,
    assert_greater_than,
    assert_greater_than_or_equal,
    assert_no_key,
)

class MempoolFeeHistogramTest(BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 1

    def skip_test_if_missing_module(self):
        self.skip_if_no_wallet()

    def run_test(self):
        node = self.nodes[0]

        node.sendtoaddress(node.getnewaddress(), 1)

        info = node.getmempoolinfo()
        assert_no_key('fee_histogram', info)

        info = node.getmempoolinfo(with_fee_histogram=True)
        total_fees = 0

        for key, bin in info['fee_histogram'].items():
            if (key != 'total_fees'):
                assert_equal(int(key), bin['from_feerate'])
                if bin['fees'] > 0:
                    assert_greater_than(bin['count'], 0)
                else:
                    assert_equal(bin['count'], 0)
                assert_greater_than_or_equal(bin['fees'], 0)
                assert_greater_than_or_equal(bin['sizes'], 0)
                assert_greater_than(bin['to_feerate'], bin['from_feerate'])
                total_fees += bin['fees']

        assert_equal(total_fees, info['fee_histogram']['total_fees'])


if __name__ == '__main__':
    MempoolFeeHistogramTest().main()
