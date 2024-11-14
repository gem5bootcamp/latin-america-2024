"""
A simple run script using a specialized CHI cache hierarchy.
This script runs a simple test with a linear generator.

> gem5 run-test.py
"""

from three_level import PrivateL1PrivateL2SharedL3CacheHierarchy

from gem5.components.boards.test_board import TestBoard
from gem5.components.memory.multi_channel import DualChannelDDR4_2400
from gem5.components.processors.linear_generator import LinearGenerator

from gem5.simulate.simulator import Simulator

board = TestBoard(
    generator=LinearGenerator(num_cores=4, max_addr=2**22, rd_perc=75),
    cache_hierarchy=PrivateL1PrivateL2SharedL3CacheHierarchy(
        l1d_size="32KiB",
        l1d_assoc=8,
        l1i_size="32KiB",
        l1i_assoc=8,
        l2_size="256KiB",
        l2_assoc=16,
        l3_size="2MiB",
        l3_assoc=32,
    ),
    memory=DualChannelDDR4_2400(size="2GB"),
    clk_freq="3GHz",
)

sim = Simulator(board)
sim.run()
