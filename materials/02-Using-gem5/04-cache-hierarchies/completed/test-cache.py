"""
A simple run script using a PrivateL1PrivateL2 cache hierarchy.
This script runs a simple test with a linear generator.

The generator can be configured for how much traffic it generates to measure
different levels of cache performance.

$ gem5 test-cache.py L1
...
Total bandwidth: 99.93 GiB/s
Average latency: 0.51 ns
"""

import argparse

from gem5.components.boards.test_board import TestBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)
from gem5.components.memory.multi_channel import DualChannelDDR4_2400
from gem5.components.processors.random_generator import RandomGenerator
from gem5.components.processors.linear_generator import LinearGenerator

from gem5.simulate.simulator import Simulator

from three_level import PrivateL1PrivateL2SharedL3CacheHierarchy

if __name__ == "__m5_main__":
    args = argparse.ArgumentParser()
    args.add_argument(
        "cache_level",
        type=str,
        help="The level of cache to test",
        choices=["L1", "L2", "L3", "memory"],
    )

    args = args.parse_args()
    if args.cache_level == "L1":
        max_addr = 16384  # fits in L1
    elif args.cache_level == "L2":
        max_addr = 131072
    elif args.cache_level == "L3":
        max_addr = 1048576
    else:
        max_addr = 8388608

    board = TestBoard(
        generator=LinearGenerator(
            num_cores=1, max_addr=max_addr, rd_perc=75, duration="1ms"
        ),
        cache_hierarchy=PrivateL1PrivateL2SharedL3CacheHierarchy(
            l1d_size="32KiB",
            l1i_size="32KiB",
            l2_size="256KiB",
            l3_size="2MiB",
        ),
        memory=DualChannelDDR4_2400(size="1GiB"),
        clk_freq="3GHz",
    )

    simulator = Simulator(board)
    simulator.run()

    stats = simulator.get_simstats()
    seconds = stats.simTicks.value / stats.simFreq.value
    total_bytes = (
        stats.board.processor.cores[0].generator.bytesRead.value
        + stats.board.processor.cores[0].generator.bytesWritten.value
    )
    latency = (
        stats.board.processor.cores[0].generator.totalReadLatency.value
        / stats.board.processor.cores[0].generator.totalReads.value
    )

    print(f"Total bandwidth: {total_bytes / seconds / 2**30:0.2f} GiB/s")
    print(f"Average latency: {latency / stats.simFreq.value * 1e9:0.2f} ns")
