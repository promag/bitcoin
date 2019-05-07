// Copyright (c) 2011-2019 The Bitcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <bench/bench.h>
#include <policy/policy.h>
#include <rpc/blockchain.h>
#include <streams.h>
#include <net.h>
#include <txmempool.h>

#include <univalue.h>

#include <list>
#include <vector>

namespace block_bench {
#include <bench/data/block413567.raw.h>
} // namespace block_bench


static void AddTx(const CTransactionRef& tx, const CAmount& fee, CTxMemPool& pool) EXCLUSIVE_LOCKS_REQUIRED(cs_main, pool.cs)
{
    LockPoints lp;
    pool.addUnchecked(CTxMemPoolEntry(tx, fee, /* time */ 0, /* height */ 1, /* spendsCoinbase */ false, /* sigOpCost */ 4, lp));
}

static void RpcMempool(benchmark::State& state)
{
    CTxMemPool pool;
    LOCK2(cs_main, pool.cs);

    for (int i = 0; i < 1000; ++i) {
        CMutableTransaction tx = CMutableTransaction();
        tx.vin.resize(1);
        tx.vin[0].scriptSig = CScript() << OP_1;
        tx.vin[0].scriptWitness.stack.push_back({1});
        tx.vout.resize(1);
        tx.vout[0].scriptPubKey = CScript() << OP_1 << OP_EQUAL;
        tx.vout[0].nValue = i;
        const CTransactionRef tx_r{MakeTransactionRef(tx)};
        AddTx(tx_r, /* fee */ i, pool);
    }

    while (state.KeepRunning()) {
        (void)MempoolToJSON(pool, /*verbose*/ true);
    }
}

static void Test(benchmark::State& state)
{
  CDataStream stream((const char*)block_bench::block413567,
          (const char*)block_bench::block413567 + sizeof(block_bench::block413567),
          SER_NETWORK, PROTOCOL_VERSION);
  char a = '\0';
  stream.write(&a, 1); // Prevent compaction

  CBlock block;
  stream >> block;

  while (state.KeepRunning()) {
      UniValue result = blockToJSON(block, nullptr, nullptr, true);
      // result.write();
  }
}


BENCHMARK(RpcMempool, 40);
BENCHMARK(Test, 40);
