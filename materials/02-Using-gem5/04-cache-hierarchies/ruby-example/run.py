"""
From https://jlpteaching.github.io/comparch/modules/gem5/assignment5/
"""

import argparse

from components.boards import HW5X86Board
from components.cache_hierarchies import HW5MESITwoLevelCacheHierarchy
from components.memories import HW5DDR4
from components.processors import HW5O3CPU

from workloads.array_sum_workload import (
    NaiveArraySumWorkload,
    ChunkingNoResultRaceArraySumWorkload,
    ChunkingNoBlockRaceArraySumWorkload,
)

from gem5.simulate.simulator import Simulator

workloads = {
    "naive": NaiveArraySumWorkload,
    "false_sharing": ChunkingNoResultRaceArraySumWorkload,
    "blocking": ChunkingNoBlockRaceArraySumWorkload,
}

parser = argparse.ArgumentParser()
parser.add_argument("workload", choices=workloads.keys())
args = parser.parse_args()

board = HW5X86Board(
    clk_freq="3GHz",
    processor=HW5O3CPU(num_cores=4),
    memory=HW5DDR4(),
    cache_hierarchy=HW5MESITwoLevelCacheHierarchy(xbar_latency=16),
)

board.set_workload(workloads[args.workload](array_size=16384, num_threads=4))

sim = Simulator(board=board)
sim.run()
