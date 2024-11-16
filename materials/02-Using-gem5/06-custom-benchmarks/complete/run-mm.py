"""
This script sets up and runs a gem5 simulation for a custom matrix
multiplication workload.

The script performs the following steps:
1. Configures a cache hierarchy with private L1 caches and a shared L2 cache.
2. Sets up a single channel DDR4 memory.
3. Creates a processor with 1 core using a simple timing-based CPU model and the x86 ISA.
4. Sets up a SimpleBoard with a 3GHz clock frequency, the configured processor, memory, and cache hierarchy.
5. Sets the workload to run a custom matrix multiplication binary.
6. Runs the simulation.

This script serves as an example of how to use your own custom workload and customize the simulator control.

$ gem5 run-mm.py
...
Workbegin handler
Workend handler
...
"""

import m5

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import (
    PrivateL1SharedL2CacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator, ExitEvent

cache_hierarchy = PrivateL1SharedL2CacheHierarchy(
    l1d_size="64kB",
    l1i_size="64kB",
    l2_size="1MB",
)

# Setup the system memory.
memory = SingleChannelDDR4_2400()

# Create a processor that runs the x86 ISA, has 1 cores and uses a simple
# timing-based CPU model.
processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, isa=ISA.X86, num_cores=1)

# Create a simple board with the processor, memory and cache hierarchy.
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# Set the workload to run a custom matrix multiplication binary.
board.set_se_binary_workload(
    binary=BinaryResource(local_path="matrix-multiply")
)


def workbegin_handler():
    print("Workbegin handler")
    m5.stats.dump()
    m5.stats.reset()
    yield False


def workend_handler():
    print("Workend handler")
    m5.stats.dump()
    m5.stats.reset()
    yield False


# Create a simulator with the board and run it.
simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.WORKBEGIN: workbegin_handler(),
        ExitEvent.WORKEND: workend_handler(),
    },
)
simulator.run()
