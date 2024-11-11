"""
One of the most basic gem5 scripts you can write.

This boots linux (just the kernel) and exits. However, we will only run it for
20 ms to save time.

This takes just a minute or so to run.

$ gem5 basic.py
gem5 Simulator System.  https://www.gem5.org
...
info: Entering event queue @ 0.  Starting simulation
"""

from gem5.prebuilt.demo.x86_demo_board import X86DemoBoard
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

# Your code goes here
