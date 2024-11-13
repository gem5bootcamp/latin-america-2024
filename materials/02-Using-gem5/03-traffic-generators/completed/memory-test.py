"""
This script creates a simple system with a traffic generator to test memory
There are four arguments to this script:
- generator: The type of the generator (linear or random)
- rate: The rate of the generator
- rd_perc: The percentage of read requests
- memory: The type of the memory (simple, DDR4, SC_LPDDR5, MC_LPDDR5)

You can run a simple bash script to test different configurations:

```bash
for rate in "16GiB/s" "32GiB/s" "64GiB/s"; do
    for rd_perc in "100" "50"; do
        for gen_type in "linear" "random"; do
            gem5 memory-test.py $gen_type $rate $rd_perc DDR4
        done;
    done;
done; | grep "Total bandwidth"
```

$ gem5 memory-test.py linear 16GiB/s 50 DDR4
...
Total bandwidth: 12.05 GiB/s
Average latency: 341.84 ns
"""

import argparse

from gem5.components.boards.test_board import TestBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.simple import SingleChannelSimpleMemory
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.memory.multi_channel import ChanneledMemory
from gem5.components.memory.dram_interfaces.lpddr5 import LPDDR5_6400_1x16_BG_BL32
from gem5.components.processors.linear_generator import LinearGenerator
from gem5.components.processors.random_generator import RandomGenerator
from gem5.simulate.simulator import Simulator


def get_generator(type: str, rate: str, rd_perc: int) -> LinearGenerator:
    if type == "linear":
        return LinearGenerator(num_cores=1, rate=rate, rd_perc=rd_perc)
    elif type == "random":
        return RandomGenerator(num_cores=1, rate=rate, rd_perc=rd_perc)
    else:
        raise ValueError(f"Unknown generator type: {type}")


def get_memory(mem_type: str):
    if mem_type == "simple":
        return SingleChannelSimpleMemory(
            latency="20ns", bandwidth="32GiB/s", latency_var="0s", size="1GiB"
        )
    elif mem_type == "DDR4":
        return SingleChannelDDR4_2400()
    elif mem_type == "SC_LPDDR5":
        return ChanneledMemory(LPDDR5_6400_1x16_BG_BL32, 1, 64)
    elif mem_type == "MC_LPDDR5":
        return ChanneledMemory(LPDDR5_6400_1x16_BG_BL32, 4, 64)
    else:
        raise ValueError(f"Unknown memory type: {mem_type}")


if __name__ == "__m5_main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "generator",
        type=str,
        help="The type of the generator",
        choices=["linear", "random"],
    )
    parser.add_argument("rate", type=str, help="The rate of the generator")
    parser.add_argument(
        "rd_perc", type=int, help="The percentage of read requests"
    )
    parser.add_argument(
        "memory",
        type=str,
        help="The type of the memory",
        choices=["simple", "DDR4", "SC_LPDDR5", "MC_LPDDR5"],
    )
    args = parser.parse_args()

    board = TestBoard(
        clk_freq="3GHz",  # ignored
        generator=get_generator(args.generator, args.rate, args.rd_perc),
        memory=get_memory(args.memory),
        cache_hierarchy=NoCache(),
    )

    simulator = Simulator(board=board)
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
