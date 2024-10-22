"""
Script with a specialized O3 CPU
This script creates a simple system with a single ARM processor, a single
channel DDR4 memory and a MESI two level cache hierarchy. The processor is
configured to run the ARM ISA and uses an out-of-order CPU model. The system is
then run with the BFS workload from the GAPBS benchmark suite.

$ gem5-mesi 02-processor.py
Graph has 1024 nodes and 10496 undirected edges for degree: 10
...
Average Time:        0.00002
"""

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
from gem5.isas import ISA

from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor

from m5.objects import ArmO3CPU
from m5.objects import TournamentBP

class MyOutOfOrderCore(BaseCPUCore):
    def __init__(self, width, rob_size, num_int_regs, num_fp_regs):
        super().__init__(ArmO3CPU(), ISA.ARM)


class MyOutOfOrderProcessor(BaseCPUProcessor):
    def __init__(self, width, rob_size, num_int_regs, num_fp_regs):
        """
        :param width: sets the width of fetch, decode, raname, issue, wb, and
        commit stages.
        :param rob_size: determine the number of entries in the reorder buffer.
        :param num_int_regs: determines the size of the integer register file.
        :param num_int_regs: determines the size of the vector/floating point
        register file.
        """
        pass


main_memory = SingleChannelDDR4_2400(size="2GB")

cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="16kB",
    l1d_assoc=8,
    l1i_size="16kB",
    l1i_assoc=8,
    l2_size="256kB",
    l2_assoc=16,
    num_l2_banks=1,
)

my_ooo_processor = MyOutOfOrderProcessor(
    width=8, rob_size=192, num_int_regs=256, num_fp_regs=256
)

board = SimpleBoard(
    processor=my_ooo_processor,
    memory=main_memory,
    cache_hierarchy=cache_hierarchy,
    clk_freq="3GHz",
)

board.set_workload(obtain_resource("arm-gapbs-bfs-run"))

simulator = Simulator(board)
simulator.run()
