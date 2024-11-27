---
Author: Tamara Lehman
Title: Secure Memory Metadata Cache in gem5
---

## Table of Contents

- [Introduction](#introduction)
- [Metadata Cache Functionality](#metadata-cache-functionality)
- [Experimental setup](#experimental-setup)
- [Implementation](#implementation)
- [Analysis](#analysis)
- [Submission](#submission)

**Suggested due date**: 6/12/2024 23:59

**Final due date**: 13/12/2024 23:59

## Introduction

In this assignment, you will extend the gem5 implementation of the secure memory system (completed during the workshop) to include a cache, the metadata cache, to improve the secure memory system performance. The metadata cache will hold recently used metadata nodes, including encryption counters, integrity tree nodes, and data hashes, reducing the overhead of repeatedly performing decryption and integrity verification for data fetched from memory.

## Metadata Cache Functionality

The secure memory metadata cache offers two benefits. Like the core data cache, it helps to alleviate the memory accesses that are needed to fetch all the metadata to both decrypt and integrity verify data read from memory. Recall that when there is a last level cache miss, the memory controller has to request an additional 3 memory blocks at least, if not more: (1) the decryption counter (2) the data hash (3) the integrity node that verifies the integrity of the encryption counter. The number of integrity tree levels traversed depends on the secure memory region size. For example, if the secure memory region size is 4GB, then the integrity tree will have 7 levels, and as a result, 7 additional memory accesses will be required (on top of the data hash and decryption counter).

For this homework we will assume that all of the memory will be protected, assuming a memory capacity of 2GB. Your metadata cache should be placed to the side of the memory controller so that it can access it when needing to decrypt and integrity verify last level cache misses. The metadata cache access should happen before creating the corresponding memory requests but after the data memory request has been sent to the memory device. The metadata cache wil store all metadata blocks used for decrypting and encrypting data fetched from/written to memory, and metadata blocks required to verify the integrity of the data fetched from memory (including both the data hashes and the integrity tree nodes at every level). There will be three different types of metadata that the cache will hold:
     - The counters used to encrypt and decrypt data. These are grouped into 64 byte blocks each containing 64 8-bit minor counters (for the 64B data block) and one 8-byte major counter (for the page).
     - The data hash to verify the integrity of the data. These are also grouped into 64 byte blocks, resulting in 8 8-byte hashes.
     - The hashes to verify the encryption counter integrity, which are the nodes that conform the integrity tree. These hashes are also grouped into 64 byte blocks, each containing 8 8-byte hashes.
If the requested node is found in the metadata cache, a cache hit should be reported, and the integrity verification traversal of the tree will stop immediately. If a counter block is found in the cache, there is no need to traverse the integrity tree, as the integrity of the counter was verified when it was brought into the cache. If a data hash is found in the cache, then it can be used to verify the integrity of the data fetched from memory. If an integrity tree node is found in the cache, then the traversal of the tree can stop a the level to which the node belongs to, as its integrity was verified when the integrity tree node was brought into the cache. A miss in the cache triggers an immediate memory request to be created for that address and a check in the cache for its parent node (unless it is a data hash block). The traversal of the tree stops at the root, since it is always assumed to be on-chip (not in the metadata cache but in its own separate register).

The default parameters for the cache will include the LRU replacement policy, the writeback base cache design, a size of 32KB 4-way set associative with a 1 cycle access latency for both the data and the tags.

## Implementation

The first change we will have to make will be to include the ports (the send and receive ports) to be able to declare a cache inside the SecureMemory component that we created during the workshop. You fill make these changes in the file called SecureMemoryTutorial.py which is in gem5/src/mem/secmem-tutorial/.  The code in this file will look something like below:

```metadata_cache_request_port  = RequestPort("Cache access port, sends requests for metadata")
   metadata_cache_response_port = RequestPort("Response side port, receives responses from the metadata cache")
   ```

The next change you will have to make will be inside the secure.py file which is in gem5/src/python/gem5/components/memory/. In this file you will have to import the L1DCache module so that you can instantiate the metadata cache:

```python
from m5.objects import L1Cache
...
self.metadata_cache = L1Cache()
```
Then you will have to connect the mem and cpu side ports from the cache to the secure memory object.

The third change you have to make is in the secure_memory.hh and secure_memory.cc files, found in the gem5/src/mem/ directory. Here you will modify the way the simulator models the secure memory controller to include a cache. You will first need to declare the ports, that you referenced in the SecureMemoryTutorial.py declarations. Once declared, you need to include their instation in the constructor of the secure memory object. Then everywhere where a packet is being sent, you need to change it to use the cache's request port instead of the memory's port.

Then the recvTimingReq of the cache implementation on the cpu side port will also need to be modified so that we can identify when a cache access resulted in a cache hit. Remember that when we have a cache hit, the integrity verification process can stop, since everything that is fetched from the cache is trusted. This change will take a bit of thinking as the cache access function does not record if the access was a hit or not. One hint to implement this functionality the easiest way is to simply add a field into the packet object to record when there is a cache hit.

## Experimental setup

For this assignment, you will use the model you developed during the bootcamp with the same parameters across your experiments.
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

Now, we are going to use the output of the gem5 simulation to understand how the metadata cache impacts the performance of the secure memroy system

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

You will submit this assignment using GitHub Classroom.
Use the "blank" repository that was created for you.

Create a new file named "hw3_submission.md" in the root of your repository and include the answers to the nine questions above.
After completing the assignment, commit and push your changes to the repository.

**Be sure to add your name and email address to the README.md file.**
This way we can associate your submission with you.
