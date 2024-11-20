"""
This script runs the RISC-V Getting Started benchmark suite on two different
processors: BigProcessor and LittleProcessor.
This script uses the MultiSim module to run the simulations in parallel.

$ gem5 -m gem5.utils.multisim my-cores-run.py
"""

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import (
    PrivateL1CacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
import gem5.utils.multisim as multisim

from my_processor import BigProcessor, LittleProcessor

multisim.set_num_processes(2)

for processor_type in [BigProcessor, LittleProcessor]:
    for benchmark in obtain_resource("riscv-getting-started-benchmark-suite"):
        board = SimpleBoard(
            clk_freq="3GHz",
            processor=processor_type(),
            memory=SingleChannelDDR4_2400("1GiB"),
            cache_hierarchy=PrivateL1CacheHierarchy(
                l1d_size="32KiB", l1i_size="32KiB"
            ),
        )
        board.set_workload(benchmark)
        simulator = Simulator(
            board=board, id=f"{processor_type.get_name()}-{benchmark.get_id()}"
        )
        multisim.add_simulator(simulator)
