# Copyright (c) 2024 The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Usage
-----

gem5 -re SMARTS.py

"""

import argparse
import math
from pathlib import Path

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_walk_cache_hierarchy import (
    PrivateL1PrivateL2WalkCacheHierarchy,
)
from gem5.components.memory import DualChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_switchable_processor import SimpleSwitchableProcessor
from gem5.isas import ISA
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator
from gem5.resources.resource import BinaryResource
from gem5.utils.requires import requires
import json
import m5

requires(isa_required=ISA.X86)

cache_hierarchy = PrivateL1PrivateL2WalkCacheHierarchy(
    l1d_size="32kB",
    l1i_size="32kB",
    l2_size="256kB",
)

memory = DualChannelDDR4_2400(size="3GB")

processor = SimpleSwitchableProcessor(
    starting_core_type=CPUTypes.ATOMIC,
    switch_core_type=CPUTypes.O3,
    isa=ISA.X86,
    num_cores=1,
)

board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

board.set_se_binary_workload(
    binary=BinaryResource(local_path=Path("/workspaces/2024/materials/02-Using-gem5/09-sampling/01-simpoint/workload/simple_workload").as_posix())
)

def smarts_generator(
    k: int, U: int, W: int, processor
):
    """
    :param k: the systematic sampling interval. Each interval simulation k*U
    instructions. The interval includes the fast-forwarding part, detailed
    warmup part, and the detail simulation part.
    :param U: sampling unit size. The instruction length in each unit.
    :param W: the length of the detailed warmup part.

    Each interval instruction length is k*U.
    The warmup part starts at (k-1)*U-W
    The detailed simulation part starts at (k-1)*U

    This exit generator only works with SwitchableProcessor.
    When it reaches to the start of the detailed warmup part, it resets the
    stats; then it switches the core type and schedule for the end of the
    warmup part and the end of the interval. When it reaches to the end of the
    detailed warmup part, it resets the stats. When it reaches to the end of
    the detailed simulation, it dumps the stats; then it switches the core type
    and schedule for the start of the next detailed warmup part.
    """
    is_switchable = isinstance(processor, SimpleSwitchableProcessor)
    warmup_start = U * (k - 1) - W
    warmup_plus_detailed = U + W
    counter = 0

    while is_switchable:
        print(f"curTick is {m5.curTick()}")
        print("got to warmup start\n")

        print("switch core type")
        # switch core type
        processor.switch()
        print(
            "now schedule for end of warmup and start of detailed simluation\n"
        )
        # schedule for warmup end
        # schedule for detailed simulation end
        processor.get_cores()[0]._set_simpoint([W, warmup_plus_detailed], True)
        print("fall back to simulation\n")
        # fall back to simualtion
        yield False

        # reached warmup end
        print(f"curTick is {m5.curTick()}")
        print("got to detail simulation start\n")
        print("now reset m5 stats\n")

        # reset stats
        m5.stats.reset()
        print("fall back to simulation\n")
        # fall back to simulation
        yield False

        # reached end of detailed simulation
        print(f"curTick is {m5.curTick()}")
        print("got to end of detail simulation\n")
        print("now dump stats\n")
        # dump stats
        m5.stats.dump()

        # switch core type
        print("switch core type\n")
        processor.switch()
        print(
            "now schedule for next warmup start and detail simulation start\n"
        )
        # schedule for the next start of warmup
        print("schedule for the next start of warmup\n")
        processor.get_cores()[0]._set_simpoint([warmup_start], True)
        print("increase n counter\n")
        # increment sample counter
        counter += 1
        print("switch core type to functional core type")
        print("fall back to simulation\n")
        yield False

program_length = 9115640
ideal_region_length = math.ceil(program_length/50)
ideal_U = 1000
ideal_k = math.ceil(ideal_region_length/ideal_U)
ideal_W = 2 * ideal_U

simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.SIMPOINT_BEGIN: smarts_generator(
            k=ideal_k,
            U=ideal_U,
            W=ideal_W,
            processor=processor,
        )
    }
)

processor.get_cores()[0]._set_simpoint([1], False)
simulator.run()

print("Simulation Done")
