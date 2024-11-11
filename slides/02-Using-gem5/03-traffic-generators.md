---
marp: true
paginate: true
theme: gem5
title: Using synthetic traffic generators
---

<!-- _class: title -->

## Using synthetic traffic generators

Using synthetic traffic generators to test memory systems.

---

<!-- _class: center-image -->

## Synthetic Traffic Generation

Synthetic traffic generation is a technique for driven memory subsystems without requiring the simulation of processor models and running workload programs. We have to note the following about synthetic traffic generation.

- It can be used for the following: measuring maximum theoretical bandwidth, testing correctness of cache coherency protocol
- It can not be used for: measuring the execution time of workloads (even if you have their memory trace)

Synthetic traffic could follow a certain pattern like `sequential (linear)`, `strided`, and `random`. In this section we will look at tools in gem5 that facilitate synthetic traffic generation.

![Traffic generator center](03-running-in-gem5-imgs/t_gen_diagram.drawio.svg)

---

## gem5: stdlib Components for Synthetic Traffic Generation

gem5's standard library has a collection of components for generating synthetic traffic. All such components inherit from `AbstractGenerator`, found in `src/python/gem5/components/processors`.

- These components simulate memory accesses. They are intended to replace a processor in a system that you configure with gem5.
- Examples of these components include `LinearGenerator` and `RandomGenerator`.

We will see how to use `LinearGenerator` and `RandomGenerator` to stimulate a memory subsystem. The memory subsystem that we are going to use is going to consist of a cache hierarchy with `private l1 caches and a shared l2 cache` with one channel of `DDR3` memory.

In the next slides we will look at `LinearGenerator` and `RandomGenerator` at a high level. We'll see how to write a configuration script that uses them.

---

<!-- _class: two-col code-70-percent -->

## Types of traffic generators

### LinearGenerator

[Python Here](/gem5/src/python/gem5/components/processors/linear_generator.py)

```python
class LinearGenerator(AbstractGenerator):
    def __init__(
        self,
        num_cores: int = 1,
        duration: str = "1ms",
        rate: str = "100GB/s",
        block_size: int = 64,
        min_addr: int = 0,
        max_addr: int = 32768,
        rd_perc: int = 100,
        data_limit: int = 0,
    ) -> None:
```

### RandomGenerator

[Python Here](/gem5/src/python/gem5/components/processors/random_generator.py)

```python
class RandomGenerator(AbstractGenerator):
    def __init__(
        self,
        num_cores: int = 1,
        duration: str = "1ms",
        rate: str = "100GB/s",
        block_size: int = 64,
        min_addr: int = 0,
        max_addr: int = 32768,
        rd_perc: int = 100,
        data_limit: int = 0,
    ) -> None:
```

---
<!-- _class: two-col -->

## LinearGenerator/RandomGenerator: Knobs

- **num_cores**
  - The number of cores in your system
- **duration**
  - Length of time to generate traffic
- **rate**
  - Rate at which to request data from memory
    - **Note**: This is *NOT* the rate at which memory will respond. This is the **maximum** rate at which requests will be made
- **block_size**
  - The number of bytes accessed with each read/write

###

- **min_addr**
  - The lowest memory address for the generator to access (via reads/writes)
- **max_addr**
  - The highest memory address for the generator to access (via reads/writes)
- **rd_perc**
  - The percentage of accesses that should be reads
- **data_limit**
  - The maximum number of bytes that the generator can access (via reads/writes)
    - **Note**: if `data_limit` is set to 0, there will be no data limit.

---
<!-- _class: two-col -->

## Traffic Patterns Visualized

`min_addr`: 0, `max_addr`: 4, `block_size`: 1

**Linear**: We want to access addresses 0 through 4 so a linear access would mean accessing memory in the following order.

**Random**: We want to access addresses 0 through 4 so a random access would mean accessing memory in any order. (In this example, we are showing the order: 1, 3, 2, 0).

###

![linear traffic pattern](03-running-in-gem5-imgs/linear_traffic_pattern.drawio.svg)

![random traffic pattern](03-running-in-gem5-imgs/random_traffic_pattern.drawio.svg)

---

<!-- _class: exercise -->

## Exercise: Measuring memory performance

In this exercise you will use different traffic patterns to better understand the performance characteristics of gem5's memory models.

Try to answer the questions before you run the experiments, then update your answers afterwards.

### Questions

- When using the SimpleMemory model, how does the memory bandwidth change with different traffic patterns? Why or why not?
- When using DDR4 memory, how does the memory bandwidth change with different traffic patterns? Why or why not?
- Compare the performance of DDR4 to LPDDR2. Which has better bandwidth? What about latency? (Or, is this the wrong way to measure latency?)

---

## Running an example with the standard library

Open [`materials/02-Using-gem5/06-memory/run-mem.py`](../../materials/02-Using-gem5/06-memory/run-mem.py)

This file uses traffic generators (seen [previously](03-running-in-gem5.md)) to generate memory traffic at 64GiB.

Let's see what happens when we use a simple memory. Add the following line for the memory system.

```python
memory = SingleChannelSimpleMemory(latency="50ns", bandwidth="32GiB/s", size="8GiB", latency_var="10ns")
```

Run with the following. Use `-c <LinearGenerator,RandomGenerator>` to specify the traffic generators and `-r <read percentage>` to specify the percentage of reads.

```sh
gem5 run-mem.py
```

---

## Vary the latency and bandwidth

Results for running with 16 GiB/s, 32 GiB/s, 64 GiB/s, and 100% reads and 50% reads.

| Bandwidth | Read Percentage | Linear Speed (GB/s) | Random Speed (GB/s) |
|-----------|-----------------|---------------------|---------------------|
| 16 GiB/s  | 100%            | 17.180288           | 17.180288           |
|           | 50%             | 17.180288           | 17.180288           |
| 32 GiB/s  | 100%            | 34.351296           | 34.351296           |
|           | 50%             | 34.351296           | 34.351296           |
| 64 GiB/s  | 100%            | 34.351296           | 34.351296           |
|           | 50%             | 34.351296           | 34.351296           |

With the `SimpleMemory` you don't see any complex behavior in the memory model (but it **is** fast).

---

## Running Channeled Memory

- Open [`gem5/src/python/gem5/components/memory/single_channel.py`](../../gem5/src/python/gem5/components/memory/single_channel.py)
- We see `SingleChannel` memories such as:

```python
def SingleChannelDDR4_2400(
    size: Optional[str] = None,
) -> AbstractMemorySystem:
    """
    A single channel memory system using DDR4_2400_8x8 based DIMM.
    """
    return ChanneledMemory(DDR4_2400_8x8, 1, 64, size=size)
```

- We see the `DRAMInterface=DDR4_2400_8x8`, the number of channels=1, interleaving_size=64, and the size.

---

## Running Channeled Memory

- Lets go back to our script and replace the SingleChannelSimpleMemory with this!

Replace

```python
SingleChannelSimpleMemory(latency="50ns", bandwidth="32GiB/s", size="8GiB", latency_var="10ns")
```

with

```python
SingleChannelDDR4_2400()
```

### Let's see what happens when we run our test

---

## Vary the latency and bandwidth

Results for running with 16 GiB/s, 32 GiB/s, and 100% reads and 50% reads.

| Bandwidth | Read Percentage | Linear Speed (GB/s) | Random Speed (GB/s) |
|-----------|-----------------|---------------------|---------------------|
| 16 GiB/s  | 100%            | 13.85856            | 14.557056           |
|           | 50%             | 13.003904           | 13.811776           |
| 32 GiB/s  | 100%            | 13.85856            | 14.541312           |
|           | 50%             | 13.058112           | 13.919488           |

As expected, because of read-to-write turn around, reading 100% is more efficient than 50% reads.
Also as expected, the bandwidth is lower than the SimpleMemory (only about 75% utilization).

Somewhat surprising, the memory modeled has enough banks to handle random traffic efficiently.

---

## Adding a new channeled memory

- Open [`materials/02-Using-gem5/06-memory/lpddr2.py`](../../materials/02-Using-gem5/06-memory/lpddr2.py)
- If we wanted to add LPDDR2 as a new memory in the standard library, we first make sure there's a DRAM interface for it in the [`dram_interfaces` directory](../../gem5/src/python/gem5/components/memory/dram_interfaces/lpddr2.py)
- Then we need to make sure we import it by adding the following to the top of your `lpddr2.py`:
```python
from gem5.components.memory.abstract_memory_system import AbstractMemorySystem
from gem5.components.memory.dram_interfaces.lpddr2 import LPDDR2_S4_1066_1x32
from gem5.components.memory.memory import ChanneledMemory
from typing import Optional
```

---

## Adding a new channeled memory

Then add the following to the body of `lpddr2.py`:

```python
def SingleChannelLPDDR2(
    size: Optional[str] = None,
) -> AbstractMemorySystem:
    return ChanneledMemory(LPDDR2_S4_1066_1x32, 1, 64, size=size)
```

Then we import this new class to our script with:

```python
from lpddr2 import SingleChannelLPDDR2
```

### Let's test this again!

---

## Vary the latency and bandwidth

Results for running with 16 GiB/s, and 100% reads and 50% reads.

| Bandwidth | Read Percentage | Linear Speed (GB/s) | Random Speed (GB/s) |
|-----------|-----------------|---------------------|---------------------|
| 16 GiB/s  | 100%            | 4.089408            | 4.079552            |
|           | 50%             | 3.65664             | 3.58816             |

LPDDR2 doesn't perform as well as DDR4.

---

## 06-traffic-gen

### Let's run an example on how to use the traffic generator

Open the following file.
[`materials/02-Using-gem5/03-running-in-gem5/06-traffic-gen/simple-traffic-generators.py`](../../materials/02-Using-gem5/03-running-in-gem5/06-traffic-gen/simple-traffic-generators.py)

Steps:

1. Run with a Linear Traffic Generator.
2. Run with a Hybrid Traffic Generator.

---
<!-- _class: two-col -->

## 06-traffic-gen: LinearGenerator: Looking at the Code


Go to this section of the code on the right.

Right now, we have set up a board with a Private L1 Shared L2 Cache Hierarchy (go to [`materials/02-Using-gem5/03-running-in-gem5/06-traffic-gen/components/cache_hierarchy.py`](../../materials/02-Using-gem5/03-running-in-gem5/06-traffic-gen/components/cache_hierarchy.py) to see how it's constructed), and a Single Channel memory system.

Add a traffic generator right below
`memory = SingleChannelDDR3_1600()` with the following lines.

```python
generator = LinearGenerator(num_cores=1, rate="1GB/s")
```

###

```python
cache_hierarchy = MyPrivateL1SharedL2CacheHierarchy()

memory = SingleChannelDDR3_1600()

motherboard = TestBoard(
    clk_freq="3GHz",
    generator=generator,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)
```

---
<!-- _class: two-col code-70-percent -->

## 06-traffic-gen: LinearGenerator: Completed Code

The completed code snippet should look like this.

```python
cache_hierarchy = MyPrivateL1SharedL2CacheHierarchy()

memory = SingleChannelDDR3_1600()

generator = LinearGenerator(num_cores=1, rate="1GB/s")

motherboard = TestBoard(
    clk_freq="3GHz",
    generator=generator,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)
```

---
<!-- _class: code-100-percent -->

## 06-traffic-gen: LinearGenerator: Running the Code

### Run the following commands to see a Linear Traffic Generator in action

```sh
cd ./materials/02-Using-gem5/03-running-in-gem5/06-traffic-gen/

gem5 --debug-flags=TrafficGen --debug-end=1000000 \
simple-traffic-generators.py
```

We will see some of the expected output in the following slide.

---

## 06-traffic-gen: LinearGenerator Results

```sh
  59605: system.processor.cores.generator: LinearGen::getNextPacket: r to addr 0, size 64
  59605: system.processor.cores.generator: Next event scheduled at 119210
 119210: system.processor.cores.generator: LinearGen::getNextPacket: r to addr 40, size 64
 119210: system.processor.cores.generator: Next event scheduled at 178815
 178815: system.processor.cores.generator: LinearGen::getNextPacket: r to addr 80, size 64
 178815: system.processor.cores.generator: Next event scheduled at 238420
```

Throughout this output, we see `r to addr --`. This means that the traffic generator is simulating a **read** request to access memory address `0x--`.

<!-- Is the sentence above accurate? -->

Above, we see `r to addr 0` in line 1, `r to addr 40` in line 3, and `r to addr 80` in line 5.

This is because the Linear Traffic Generator  is simulating requests to access memory addresses 0x0000, 0x0040, 0x0080.

As you can see, the simulated requests are very linear. Each new memory access is 0x0040 bytes above the previous one.

---

## 06-traffic-gen: Random

We are not going to do this right now, but if you swapped `LinearGenerator` with `RandomGenerator` and kept the parameters the same, the output is going to look like below. Notice how the pattern of addresses is not a linear sequence anymore.

```sh
  59605: system.processor.cores.generator: RandomGen::getNextPacket: r to addr 2000, size 64
  59605: system.processor.cores.generator: Next event scheduled at 119210
 119210: system.processor.cores.generator: RandomGen::getNextPacket: r to addr 7900, size 64
 119210: system.processor.cores.generator: Next event scheduled at 178815
 178815: system.processor.cores.generator: RandomGen::getNextPacket: r to addr 33c0, size 64
 178815: system.processor.cores.generator: Next event scheduled at 238420
```

---
<!-- _class: center-image -->

## Our Focus: LinearGenerator and AbstractGenerator

- We will be focusing on `LinearGenerator` and `RandomGenerator` generators (and a new one later!).
  - They are essentially the same, but one performs linear memory accesses and one performs random memory accesses

![Different Generators](03-running-in-gem5-imgs/generator_inheritance.drawio.svg)

---

## Detailed Look on Some Components

- You can find all generator related standard library components under [`src/python/gem5/components/processors`](https://github.com/gem5/gem5/tree/stable/src/python/gem5/components/processors).
- Looking at [`AbstractGenerator.__init__`](https://github.com/gem5/gem5/blob/stable/src/python/gem5/components/processors/abstract_generator.py#L53), you'll see that this class takes a list of `AbstractGeneratorCores` as the input. Example classes that inherit from `AbstractGenerator` are `LinearGenerator` and `RandomGenerator`.
- We will look at classes that extend `AbstractGeneratorCore` that will will create **synthetic traffic** by using a `SimObject` called `PyTrafficGen`. For more information you can look at `src/cpu/testers/traffic_gen`.
- `LinearGenerator` can have multiple `LinearGeneratorCores` and `RandomGenerator` can have multiple `RandomGeneratorCores`.

Next we will look at extending `AbstractGenerator` to create `HybridGenerator` that has both `LinearGeneratorCores` and `RandomGeneratorCores`.

---
## Extending AbstractGenerator

gem5 has a lot of tools in its standard library, but if you want to simulate specific memory accesses patterns in your research, there might not be anything in the standard library to do this.

In this case, you would have to extend `AbstractGenerator` to create a concrete generator that is tailored to your needs.

To do this, we will go through an example called `HybridGenerator`.

The goal of `HybridGenerator` is to simultaneously simulate both linear and random memory accesses.

To do this, we need `LinearGeneratorCores` (to simulate linear traffic) and `RandomGeneratorCores` (to simulate random traffic).

---

## 06-traffic-gen: HybridGenerator: A Quick Side Note about LinearGeneratorCores

`LinearGeneratorCores` simulate linear traffic.

When we have multiple `LinearGeneratorCores`, if we configure each one to have the same `min_addr` and `max_addr`, each one will start simulating memory accesses at the same `min_addr` and go up to the same `max_addr`. They will be accessing the same addresses at the same time.

We want `LinearGeneratorCore` to simulate a more reasonable accesses pattern.

Therefore, we will have each `LinearGeneratorCore` simulate accesses to a different chunk of memory. To do this, we will have to split up memory into equal-sized chunks and configure each `LinearGeneratorCore` to simulate accesses to one of these chunks.

---
<!-- _class: center-image -->

## 06-traffic-gen: HybridGenerator: A Quick Side Note about LinearGeneratorCores Cont.

Here's a diagram that shows how each `LinearGeneratorCore` should access memory.

![Linear Generator Core Memory Access Diagram](03-running-in-gem5-imgs/lin_core_access_diagram.drawio.svg)


---

## 06-traffic-gen: HybridGenerator: Dividing Memory Address Range

When we create a `HybridGenerator`, we have to determine which `LinearGeneratorCore` gets what chunk of memory.

As previously discussed, we need to partition the memory address range into equally sized sections and configure each `LinearGeneratorCore` to simulate accesses to a different section.

To partition, we will use the `partition_range()` function in [`gem5/src/python/gem5/components/processors/abstract_generator.py`](../../gem5/src/python/gem5/components/processors/abstract_generator.py).

This function takes the range of `min_addr` to `max_addr` and partitions it into `num_partitions` equal-length pieces.

For example, if `min_addr` = 0, `max_addr` = 9, and `num_partitions` = 3, then `partition_range` would return <0,3>, <3,6>, <6,9>.

---

## 06-traffic-gen: HybridGenerator: A quick reminder about RandomGeneratorCores

We also have to consider the `RandomGeneratorCores`.

It would be reasonable to assume that we should partition them like the `LinearGeneratorCores`, but this is not the case.

Even if each `RandomGeneratorCore` has the same `min_addr` and `max_addr`, since each one simulates a random memory access, each one will be simulating accesses to different (random) memory addresses.

---

<!-- _class: center-image -->

## 06-traffic-gen: HybridGenerator: Dividing Memory Address Range Cont.

In the end, this is how each core will simulate memory accesses.

![Linear vs. Random memory accesses](./03-running-in-gem5-imgs/core_access_diagram.drawio.svg)

---

<!-- _class: code-70-percent -->

## 06-traffic-gen: HybridGenerator: Choosing a Distribution of Cores

Now that we know how each core will access memory, next, we need to determine how many `LinearGeneratorCores` and `RandomGeneratorCores` we need.

There are many correct ways to do this, but we will use the following function to determine the number of `LinearGeneratorCores`.

```python
        def get_num_linear_cores(num_cores: int):
            """
            Returns the largest power of two that is smaller than num_cores
            """
            if (num_cores & (num_cores - 1) == 0):
                return num_cores//2
            else:
                return 2 ** int(log(num_cores, 2))
```

The rest of the cores will be `RandomGeneratorCores`.

---

<!-- _class: two-col code-60-percent -->

## 06-traffic-gen: HybridGenerator Constructor

Let's start looking at the code!

Make sure you have the following file open.
[`materials/02-Using-gem5/03-running-in-gem5/06-traffic-gen/components/hybrid_generator.py`](../../materials/02-Using-gem5/03-running-in-gem5/06-traffic-gen/components/hybrid_generator.py)

On the right, you'll see the constructor for `HybridGenerator`.

When we initialize `HybridGenerator` (via `def __init__`), we will be initializing an `AbstractGenerator` (via `super() __init__`) with the values on the right.

```python
class HybridGenerator(AbstractGenerator):
    def __init__(
        self,
        num_cores: int = 2,
        duration: str = "1ms",
        rate: str = "1GB/s",
        block_size: int = 8,
        min_addr: int = 0,
        max_addr: int = 131072,
        rd_perc: int = 100,
        data_limit: int = 0,
    ) -> None:
        if num_cores < 2:
            raise ValueError("num_cores should be >= 2!")
        super().__init__(
            cores=self._create_cores(
                num_cores=num_cores,
                duration=duration,
                rate=rate,
                block_size=block_size,
                min_addr=min_addr,
                max_addr=max_addr,
                rd_perc=rd_perc,
                data_limit=data_limit,
            )
        )
```

---

## 06-traffic-gen: Designing a HybridGenerator

Right now, our `HybridGenerator` class has a constructor, but we need to return a list of cores.

In gem5, the method that returns a list of cores is conventionally named `_create_cores`.

If you look at our file, [`hybrid_generator.py`](../../materials/02-Using-gem5/03-running-in-gem5/06-traffic-gen/components/hybrid_generator.py), you'll see this method called `_create_cores`.

---

## 06-traffic-gen: HybridGenerator: Initializing Variables

Let's define `_create_cores`!

Let's start by declaring/defining some important variables.

First, we'll declare our list of cores.

Then, we'll define the number of `LinearGeneratorCores` and `RandomGeneratorCores`.

Add the following lines under the comment labeled `(1)`.

```python
core_list = []

num_linear_cores = get_num_linear_cores(num_cores)
num_random_cores = num_cores - num_linear_cores
```

---

## 06-traffic-gen: HybridGenerator: Partitioning Memory Address Range

Next, let's define the memory address range for each `LinearGeneratorCore`.

If we want to give each `LinearGeneratorCore` an equal chunk of the given memory address range, we need to partition the range of `min_addr` to `max_addr` into `num_linear_cores` pieces.

To do this, we need to add the following line to our code under the comment labeled `(2)`.

```python
addr_ranges = partition_range(min_addr, max_addr, num_linear_cores)
```

`addr_ranges` will be a `num_linear_cores`-long list of equal-length partitions from `min_addr` to `max_addr`.

---

## 06-traffic-gen: Partitioning Memory Address Range Cont.

For example, we have `min_addr=0`, `max_addr=32768`, and `num_cores=16` (8 `LinearGeneratorCores`), then

```sh
addr_ranges=
  [(0, 4096), (4096, 8192), (8192, 12288), (12288, 16384),
  (16384, 20480), (20480, 24576), (24576, 28672), (28672, 32768)]
```

For the `i`'th `LinearGeneratorCore`, we take the `i`'th entry in `addr_ranges`. `min_addr` is the first value that entry, and `max_addr` is the second value in that entry.

In this example, `LinearGeneratorCore` 0 gets initialized with `min_addr=0` and `max_addr=4096`, `LinearGeneratorCore` 1 gets initialized with `min_addr=4096` and `max_addr=8192`, etc.

---
<!-- _class: two-col -->

## 06-traffic-gen: HybridGenerator: Creating a List of Cores: LinearGeneratorCore

Next, let's start creating our list of cores.

First, let's add all the `LinearGeneratorCores`.

Add the lines on the right under the comment labeled `(3)`.

```python
for i in range(num_linear_cores):
            core_list.append(LinearGeneratorCore(
                duration=duration,
                rate=rate,
                block_size=block_size,
                min_addr=addr_ranges[i][0],
                max_addr=addr_ranges[i][1],
                rd_perc=rd_perc,
                data_limit=data_limit,)
            )
```

---
<!-- _class: two-col -->

## 06-traffic-gen: HybridGenerator: Creating a List of Cores Explained: LinearGeneratorCore

In the for loop, we create `num_linear_cores` `LinearGeneratorCores` and append each one to our `core_list`.

Each `LinearGeneratorCore` parameter is initialized with the same values from the constructor, except for `min_addr` and `max_addr`.

We change `min_addr` and `max_addr` so that each `LinearGeneratorCore` only simulates accesses to a section of the range of `HybridGenerator's` `min_addr` to `max_addr`.

###

```python
for i in range(num_linear_cores):
            core_list.append(LinearGeneratorCore(
                duration=duration,
                rate=rate,
                block_size=block_size,
                min_addr=addr_ranges[i][0],
                max_addr=addr_ranges[i][1],
                rd_perc=rd_perc,
                data_limit=data_limit,)
            )
```

---
<!-- _class: two-col -->

## 06-traffic-gen: HybridGenerator: Creating a List of Cores: RandomGeneratorCore

Now that we've added the `LinearGeneratorCores`, let's add all the `RandomGeneratorCores`.

Add the lines on the right under the comment labeled `(4)`.

###

```python
for i in range(num_random_cores):
            core_list.append(RandomGeneratorCore(
                duration=duration,
                rate=rate,
                block_size=block_size,
                min_addr=min_addr,
                max_addr=max_addr,
                rd_perc=rd_perc,
                data_limit=data_limit,)
            )
```

---
<!-- _class: two-col -->

## 06-traffic-gen: HybridGenerator: Creating a List of Cores Explained: RandomGeneratorCore

Once again, in the for loop, we create `num_linear_cores` `RandomGeneratorCores` and append each one to our core_list.

Each `RandomGeneratorCore` parameter is initialized with the same values from the constructor, including `min_addr` and `max_addr`.

`min_addr` and `max_addr` do not change because each `RandomGeneratorCore` should be able to access the entire range of `HybridGenerator's` `min_addr` to `max_addr`.

###

```python
for i in range(num_random_cores):
            core_list.append(RandomGeneratorCore(
                duration=duration,
                rate=rate,
                block_size=block_size,
                min_addr=min_addr,
                max_addr=max_addr,
                rd_perc=rd_perc,
                data_limit=data_limit,)
            )
```

---

## 06-traffic-gen: HybridGenerator: Returning and Beginning Configuration

We're almost done with this file!

Let's return our `core_list` by adding the following line under the comment labeled `(5)`.

```python
return core_list
```

Now, open the file [materials/02-Using-gem5/03-running-in-gem5/06-traffic-gen/simple-traffic-generators.py](../../materials/02-Using-gem5/03-running-in-gem5/06-traffic-gen/simple-traffic-generators.py).

Let's replace our `LinearGenerator` with a `HybridGenerator`.

First, add the following line somewhere at the top of your code to import the `HybridGenerator`.

```python
from components.hybrid_generator import HybridGenerator
```

---

<!-- _class: two-col code-70-percent -->

## 06-traffic-gen: HybridGenerator: Configuring

In this section of code to the right, you should currently have a `LinearGenerator`.

Let's replace it with a `HybridGenerator`.

Replace the following lines

```python
generator = LinearGenerator(
    num_cores=1
)
```

with

```python
generator = HybridGenerator(
    num_cores=6
)
```

###

```python
cache_hierarchy = MyPrivateL1SharedL2CacheHierarchy()

memory = SingleChannelDDR3_1600()

generator = LinearGenerator(
    num_cores=1
)

motherboard = TestBoard(
    clk_freq="3GHz",
    generator=generator,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)
```

---
<!-- _class: two-col code-70-percent -->

## 06-traffic-gen: HybridGenerator: Configuring Cont.

This is what it should look like now.

###

```python
cache_hierarchy = MyPrivateL1SharedL2CacheHierarchy()

memory = SingleChannelDDR3_1600()

generator = HybridGenerator(
    num_cores=6
)

motherboard = TestBoard(
    clk_freq="3GHz",
    generator=generator,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)
```

---

## 06-traffic-gen: HybridGenerator: Running

Now, that we've created a `HybridGenerator`, let's run the program again!

Make sure you're in the following directory.

**`materials/02-Using-gem5/03-running-in-gem5/06-traffic-gen/`**

Now run with the following command.

```sh
gem5 --debug-flags=TrafficGen --debug-end=1000000 \
simple-traffic-generators.py
```

---

## 06-traffic-gen: HybridGenerator: Output

After running the command, you should see something like below.

```sh
   7451: system.processor.cores5.generator: RandomGen::getNextPacket: r to addr 80a8, size 8
   7451: system.processor.cores5.generator: Next event scheduled at 14902
   7451: system.processor.cores4.generator: RandomGen::getNextPacket: r to addr 10a90, size 8
   7451: system.processor.cores4.generator: Next event scheduled at 14902
   7451: system.processor.cores3.generator: LinearGen::getNextPacket: r to addr 18000, size 8
   7451: system.processor.cores3.generator: Next event scheduled at 14902
   7451: system.processor.cores2.generator: LinearGen::getNextPacket: r to addr 10000, size 8
   7451: system.processor.cores2.generator: Next event scheduled at 14902
   7451: system.processor.cores1.generator: LinearGen::getNextPacket: r to addr 8000, size 8
   7451: system.processor.cores1.generator: Next event scheduled at 14902
   7451: system.processor.cores0.generator: LinearGen::getNextPacket: r to addr 0, size 8
   7451: system.processor.cores0.generator: Next event scheduled at 14902
```

As you can see, cores 0, 1, 2, and 3 are `LinearGeneratorCores`, and cores 4 and 5 are `RandomGeneratorCores`!

---

## 06-traffic-gen: HybridGenerator: Statistics

Now, let's look at some of the statistical differences between our `LinearGeneratorCores` and `RandomGeneratorCores`.

Run the following command to see the miss rate for each core's l1 data cache.

```sh
grep ReadReq.missRate::processor m5out/stats.txt
```

On the next slide, you'll see the expected output (with some text removed for readability).

---

## 06-traffic-gen: HybridGenerator: Statistics Cont.

```sh
system.cache_hierarchy.l1dcaches0.ReadReq.missRate::processor.cores0.generator     0.132345
system.cache_hierarchy.l1dcaches1.ReadReq.missRate::processor.cores1.generator     0.133418
system.cache_hierarchy.l1dcaches2.ReadReq.missRate::processor.cores2.generator     0.133641
system.cache_hierarchy.l1dcaches3.ReadReq.missRate::processor.cores3.generator     0.132971
system.cache_hierarchy.l1dcaches4.ReadReq.missRate::processor.cores4.generator     0.876426
system.cache_hierarchy.l1dcaches5.ReadReq.missRate::processor.cores5.generator     0.875055
```

Cores 0, 1, 2, and 3 (`LinearGeneratorCores`) have a miss rate of **0.13309375** (~13.3%) on average.

Cores 4 and 5 (`RandomGeneratorCores`) have a miss rate of **0.8757405** (~87.5%) on average.

This is because `LinearGeneratorCores` access memory linearly. Therefore, they exhibit more locality which in turn results in less misses in the l1dcache.

On the other hand, since the `RandomGeneratorCores` access memory randomly, the caches can't take advantage of locality in the same way.

---
<!-- Speaker Notes:

## More summaries

m5ops can be used to communicate between simulated workload and the simulator

Traffic generator can abstract away the details of a data requestor such as CPU for generating test cases for memory systems

-->

## Summary

Overall, we discussed two different types of traffic generators: **Linear** and **Random**.

`LinearGenerators` simulate linear memory accesses, and `RandomGenerators` simulate random memory accesses.

We looked into how to configure a board that uses these traffic generators.

We also extended the `AbstractGenerator` class to create a `HybridGenerator`, which simulates linear and random memory accesses simultaneously.

Finally, we saw some of the statistical differences between`LinearGeneratorCores` and `RandomGeneratorCores`.
