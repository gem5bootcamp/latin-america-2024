"""
This script creates a simple system with a single ARM processor, a single
channel DDR4 memory and a MESI two level cache hierarchy. The processor is
configured to run the ARM ISA and uses a simple timing-based CPU model. The
system is then run with the BFS workload from the GAPBS benchmark suite.

Note that the output will be the output of the workload (in this case BFS) and
the gem5 simulator output.

$ gem5-mesi 01-components.py
Generate Time:       0.00462
Build Time:          0.00141
Graph has 1024 nodes and 10496 undirected edges for degree: 10
...
Average Time:        0.00009
"""

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator


# Your code goes below
