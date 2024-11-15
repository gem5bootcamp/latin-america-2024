"""
This script sets up and runs a gem5 simulation with a specified CPU type.

The script performs the following steps:
1. Parses command line arguments to determine the CPU type.
2. Configures a SimpleProcessor with the specified CPU type and RISC-V ISA.
3. Sets up a SimpleBoard with a 3GHz clock frequency, 1GiB DDR4 memory, and a private L1 cache hierarchy.
4. Obtains a RISC-V matrix multiplication workload resource.
5. Runs the simulation.

Arguments:
- --cpu-type: Specifies the type of CPU to use for the simulation. Must be one of the types defined in CPUTypes.

$ gem5 cores-run.py --cpu-type TIMING
...
Total time: 20.879ms
Total instructions: 33955006
"""

import argparse

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import (
    PrivateL1CacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

# Parse command line arguments
parser = argparse.ArgumentParser(description="gem5 core simulation")
parser.add_argument(
    "--cpu-type",
    type=lambda s: CPUTypes[s.upper()],
    choices=list(CPUTypes),
    required=True,
    help="Type of CPU to use for the simulation",
)
args = parser.parse_args()

processor = SimpleProcessor(cpu_type=args.cpu_type, isa=ISA.RISCV, num_cores=1)

board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=SingleChannelDDR4_2400("1GiB"),
    cache_hierarchy=PrivateL1CacheHierarchy(
        l1d_size="32KiB", l1i_size="32KiB"
    ),
)

workload = obtain_resource("riscv-matrix-multiply-run")
board.set_workload(workload)
simulator = Simulator(board=board)
simulator.run()

stats = simulator.get_simstats()

print(f"Total time: {stats.simTicks.value / stats.simFreq.value * 1e3:0.3f}ms")
print(f"Total instructions: {int(stats.simInsts.value)}")
