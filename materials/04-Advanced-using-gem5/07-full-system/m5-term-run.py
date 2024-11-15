"""

This script demonstrates how to use KVM CPU without perf.
This simulation boots Ubuntu 18.04 using 2 KVM CPUs without using perf.

Once the OS has booted the script runs `/bin/sh` to keep the simulation
running.

Usage
-----

```
scons build/X86/gem5.opt -j`nproc`
./build/X86/gem5.opt materials/02-Using-gem5/07-full-system/m5-term-run.py
```
"""

from gem5.coherence_protocol import CoherenceProtocol
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import (
    SimpleProcessor,
)
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator



from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)

cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="32KiB",
    l1d_assoc=8,
    l1i_size="32KiB",
    l1i_assoc=8,
    l2_size="512KiB",
    l2_assoc=16,
    num_l2_banks=1,
)

memory = SingleChannelDDR4_2400(size="3GiB")

processor = SimpleProcessor(
    cpu_type=CPUTypes.KVM,
    isa=ISA.X86,
    num_cores=2,
)

for proc in processor.cores:
    proc.core.usePerf = False

board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

workload = obtain_resource("x86-ubuntu-18.04-boot", resource_version="2.0.0")
workload.set_parameter("readfile_contents", "/bin/sh")
board.set_workload(workload)

simulator = Simulator(board=board)
simulator.run()
