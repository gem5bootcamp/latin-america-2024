# Copyright (c) 2022 The Regents of the University of California
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

import pathlib

from gem5.resources.resource import BinaryResource
from .custom_se_workload import CustomSEWorkload

this_dir = pathlib.Path(__file__).parent.absolute()


class NaiveArraySumWorkload(CustomSEWorkload):
    def __init__(self, array_size: int, num_threads: int):
        array_sum_bin = BinaryResource(str(this_dir / "array_sum/naive-gem5"))
        super().__init__(
            parameters={
                "binary": array_sum_bin,
                "arguments": [array_size, num_threads],
            }
        )


class ChunkingArraySumWorkload(CustomSEWorkload):
    def __init__(self, array_size: int, num_threads: int):
        array_sum_bin = BinaryResource(
            str(this_dir / "array_sum/chunking-gem5")
        )
        super().__init__(
            parameters={
                "binary": array_sum_bin,
                "arguments": [array_size, num_threads],
            }
        )


class NoResultRaceArraySumWorkload(CustomSEWorkload):
    def __init__(self, array_size: int, num_threads: int):
        array_sum_bin = BinaryResource(
            str(this_dir / "array_sum/res-race-opt-gem5")
        )
        super().__init__(
            parameters={
                "binary": array_sum_bin,
                "arguments": [array_size, num_threads],
            }
        )


class ChunkingNoResultRaceArraySumWorkload(CustomSEWorkload):
    def __init__(self, array_size: int, num_threads: int):
        array_sum_bin = BinaryResource(
            str(this_dir / "array_sum/chunking-res-race-opt-gem5")
        )
        super().__init__(
            parameters={
                "binary": array_sum_bin,
                "arguments": [array_size, num_threads],
            }
        )


class NoCacheBlockRaceArraySumWorkload(CustomSEWorkload):
    def __init__(self, array_size: int, num_threads: int):
        array_sum_bin = BinaryResource(
            str(this_dir / "array_sum/block-race-opt-gem5")
        )
        super().__init__(
            parameters={
                "binary": array_sum_bin,
                "arguments": [array_size, num_threads],
            }
        )


class ChunkingNoBlockRaceArraySumWorkload(CustomSEWorkload):
    def __init__(self, array_size: int, num_threads: int):
        array_sum_bin = BinaryResource(
            str(this_dir / "array_sum/all-opt-gem5")
        )
        super().__init__(
            parameters={
                "binary": array_sum_bin,
                "arguments": [array_size, num_threads],
            }
        )
