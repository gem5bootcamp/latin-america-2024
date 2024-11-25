from typing import List
from gem5.isas import ISA
from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor

from m5.objects import RiscvO3CPU
from m5.objects.FuncUnitConfig import *
from m5.objects.BranchPredictor import (
    TournamentBP,
    BiModeBP,
    MultiperspectivePerceptronTAGE64KB,
)


class BigO3(RiscvO3CPU):
    def __init__(self):
        super().__init__()
        self.fetchWidth = 8
        self.decodeWidth = 8
        self.renameWidth = 8
        self.dispatchWidth = 8
        self.issueWidth = 8
        self.wbWidth = 8
        self.commitWidth = 8

        self.numROBEntries = 256
        self.numPhysIntRegs = 512
        self.numPhysFloatRegs = 512

class LittleO3(RiscvO3CPU):
    def __init__(self):
        super().__init__()
        self.fetchWidth = 2
        self.decodeWidth = 2
        self.renameWidth = 2
        self.dispatchWidth = 2
        self.issueWidth = 2
        self.wbWidth = 2
        self.commitWidth = 2

        self.numROBEntries = 30
        self.numPhysIntRegs = 40
        self.numPhysFloatRegs = 40

class BigCore(BaseCPUCore):
    def __init__(self):
        core = BigO3()
        super().__init__(core, ISA.RISCV)

class LittleCore(BaseCPUCore):
    def __init__(self):
        core = LittleO3()
        super().__init__(core, ISA.RISCV)

class BigProcessor(BaseCPUProcessor):
    def __init__(self):
        super().__init__(
            cores=[BigCore()]
        )

class LittleProcessor(BaseCPUProcessor):
    def __init__(self):
        super().__init__(
            cores=[LittleCore()]
        )
