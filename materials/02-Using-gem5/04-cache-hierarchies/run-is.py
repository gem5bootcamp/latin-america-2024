"""Run script for the IS-A benchmark.

This script runs the IS-A benchmark on a gem5 simulator with a three level
hierarchy.py. This script can be used to run either Arm SE mode or X86 FS
mode. (You can change the comment.)

Running IS-A in SE mode takes about 30 seconds
Running IS-A in FS mode takes much longer, so FS mode with x86 is set to run
just 10 million instructions (on each thread for at total of about 40M). This
takes about one minute.
See lines 85 and 86 to choose Arm or X86.

To run this script, you can use the following command:
> gem5 run-is.py
"""

from gem5.components.memory.multi_channel import DualChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_switchable_processor import (
    SimpleSwitchableProcessor,
)
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator

from three_level import PrivateL1PrivateL2SharedL3CacheHierarchy

import m5

cache_hierarchy = PrivateL1PrivateL2SharedL3CacheHierarchy(
    l1d_size="32KiB",
    l1d_assoc=8,
    l1i_size="32KiB",
    l1i_assoc=8,
    l2_size="256KiB",
    l2_assoc=16,
    l3_size="2MiB",
    l3_assoc=32,
)

memory = DualChannelDDR4_2400(size="3GiB")

def get_x86_board(cache_hierarchy, memory):
    from gem5.components.boards.x86_board import X86Board
    processor = SimpleSwitchableProcessor(
        starting_core_type=CPUTypes.KVM,
        switch_core_type=CPUTypes.TIMING,
        isa=ISA.X86,
        num_cores=4,
    )

    # Here we tell the KVM CPU (the starting CPU) not to use perf.
    for proc in processor.start:
        proc.core.usePerf = False

    # Here we setup the board. The X86Board allows for Full-System X86 simulations.
    board = X86Board(
        clk_freq="3GHz",
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy,
    )

    board.set_workload(obtain_resource("npb-is-a"))
    return board

def get_arm_board(cache_hierarchy, memory):
    from gem5.components.boards.simple_board import SimpleBoard
    from gem5.components.processors.simple_processor import SimpleProcessor
    processor = SimpleProcessor(
        cpu_type=CPUTypes.TIMING,
        num_cores=4,
        isa=ISA.ARM,
    )
    board = SimpleBoard(
        clk_freq="3GHz",
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy,
    )
    board.set_workload(obtain_resource("arm-npb-is-size-s-run"))
    return board

board = get_arm_board(cache_hierarchy, memory)
# board = get_x86_board(cache_hierarchy, memory)
processor = board.processor

def on_exit():
    if board.get_processor().get_isa() == ISA.ARM:
        # No ROI or exits for ARM/SE mode
        yield True
    print("Exiting the simulation for kernel boot")
    yield False
    print("Exiting the simulation for systemd complete")
    yield False

def on_work_begin():
    print("Work begin. Switching to detailed CPU")
    m5.stats.reset()
    processor.switch()
    print("Running for 10,000,000 instructions on any thread")
    simulator.schedule_max_insts(10_000_000)
    yield False

def on_work_end():
    print("Work end")
    yield True

simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.EXIT: on_exit(),
        ExitEvent.WORKBEGIN: on_work_begin(),
        ExitEvent.WORKEND: on_work_end(),
    },
)

simulator.run()
