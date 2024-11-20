---
Author: Tamara Lehman
Title: Secure Memory Metadata Cache in gem5
---

## Table of Contents

- [Introduction](#introduction)
- [Metadata Cache Functionality](#Metadata-Cache-Functionality)
- [Experimental setup](#experimental-setup)
- [Analysis](#analysis)
- [Submission](#submission)

## Introduction

In this assignment, you will extend the gem5 implementation of the secure memory system (completed during the workshop) to include a cache, the metadata cache, to improve the secure memory system performance. The metadata cache will hold recently used metadata nodes, including encryption counters, integrity tree nodes, and data hashes, reducing the overhead of repeatedly performing decryption and integrity verification for data fetched from memory.

## Metadata Cache Functionality

The secure memory metadata cache offers two benefits. Like the core data cache, it helps to alleviate the memory accesses that are needed to fetch all the metadata to both decrypt and integrity verify data read from memory. Recall that when there is a last level cache miss, the memory controller has to request an additional 3 memory blocks at least, if not more: (1) the decryption counter (2) the data hash (3) the integrity node that verifies the integrity of the encryption counter. The number of integrity tree levels traversed depends on the secure memory region size. For example, if the secure memory region size is 4GB, then the integrity tree will have 7 levels, and as a result, 7 additional memory accesses will be required (on top of the data hash and decryption counter). 


For this homework we will assume that all of the memory will be protected, and as a result the integrity tree will have x number of levels (memory size will be xGB). Your metadata cache should be placed to the side of the memory controller so that it can access it when needing to decrypt and integrity verify last level cache misses. The metadata cache access should happen before creating the correspoding memory requests but after the data memory request has been sent to the memory device. The metadata cache wil store all metadata blocks used for decrypting and encrypting data fetched from/written to memory, and metadata blocks required to verify the integrity of the data fetched from memory (including both the data hashes and the integrity tree nodes at every level). There will be three different types of metadata that the cache will hold:
     - The counters used to encrypt and decrypt data. These are grouped into 64 byte blocks each containing 64 8-bit minor counters (for the 64B data block) and one 8-byte major counter (for the page). 
     - The data hash to verify the integrity of the data. These are also grouped into 64 byte blocks, resulting in 8 8-byte hashes.
     - The hashes to verify the encryption counter integrity, which are the nodes that conformt the integrity tree. These hashes are also grouped into 64 byte blocks, each containing 8 8-byte hashes.
If the requested node is found in the metadata cache, a cache hit should be repoerted, and the integrity verification traversal of the tree will stop immediately. If a counter block is found in the cache, there is no need to traverse the integrity tree, as the integrity of the counter was verified when it was brought into the cache. If a data hash is found in the cache, then it can be used to verify the integrity of the data fetched from memory. If an integrity tree node is found in the cache, then the traversal of the tree can stop a the level to which the node belongs to, as its integrity was verified when the integrity tree node was brought into the cache. A miss in the cache triggers an immediate memory request to be created for that address and a check in the cache for its parent node (unless it is a data hash block). The traversal of the tree stops at the root, since it is always assumed to be on-chip (not in the metadata cache but in its own separate register)./

We will use the existing pseudo LRU eviction policy implementation and the writeback base cache design. We will assume the cache is 32KB 4-way set associative (except where explicitly stated to vary these parameters) with a 1 cycle access latency for both the data and the tags. 

---
## Experimental setup

For this assignment, you will use the model you developed during the worshop with the same parameters across your experiments.
However, for parts of the assignment, you might want to change the number of processor cores or the parameters for the metadata cache and/or the last level cache (LLC).
Refer to the list below for more information on the components you will be using.

- boards: you will only use `HW5X86Board`.
You can find its definition in `components/boards.py`.
- processors: you will only use `HW5O3CPU`.
You can find its definition in `components/processors.py`.
**NOTE**: you will notice that the component creates a processor with an extra core.
This is a weird gem5 thing.
Please ignore this.
However, when you look at your statistics you should ignore statistics for `board.processor.core.cores0` and
`board.cache_hierarchy.ruby_system.l1_controllers0`.
- cache hierarchies: you will only use `HW5MESITwoLevelCacheHierarchy`.
You can find its definition in `components/cache_hierarchies.py`.
**NOTE**: you will notice that its `__init__` takes **one** argument.
- memories: You will only use `HW5DDR4`.
You can find its definition in `components/memories.py`.
- clock frequency: Use `3GHz` as your clock frequency.

To run your experiments, create a configuration script that allows you to run *any of the 18 implementations* of the workload with *any number of cores* for `HW5O3CPU`.


### **IMPORTANT NOTE**

In your configuration scripts, make sure to import `exit_event_handler` using the command below.

```python
from workloads.roi_manager import exit_event_handler
```

You will have to pass `exit_event_handler` as a keyword argument named `on_exit_event` when creating a `simulator` object. Use the *template* below to create a simulator object.

```python
simulator = Simulator(board={name of your board}, full_system=False, on_exit_event=exit_event_handler)
```

---
## Analysis
Now, we are going to use the output of the gem5 simulation to understand how the metadta cache impacts the performance of the secure memroy system

### Question 1

Experiment with setting the size for the metadata cache at 4KB, 8KB, 16KB, 32KB, 64KB and 128KB. At what metadata cache size does the cache start making a difference? Use data to back up your answer.

### Question 2

Experiment with setting the associativity for the metadata cache at 4, 8, 16, and 32. Does increasing the associativity make any difference in performance? Use data to back up your answer.

### Question 3

Experiment with using the RandomRP, SHiPRP, and  LRURP replacement policies. Explain which one is the best to use for this scenario and why. 

### Question 4

Experiment with changing the last level cache size using 128KB, 256KB, 512KB and 1MB. How does the last level cache size impact the effectiveness of the metadata cache?

### Question 5

How do the statistics change (if at all) when running with 4 cores compared to when running with just 1?

---
## Submission

Use clear reasoning and visualization to drive your conclusions.

Submit all your code through your assignment repository. Please make sure to include code/scripts for the following.

- `Instruction.md`: should include instructions on how to run your simulations.
- Automation: code/scripts to run your simulations.
- Configuration: python file configuring the systems you need to simulate.
- `Answers.md`: should include the answers to the questions in the assignment.
