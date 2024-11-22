---
Author: Jason Lowe-Power
Title: Design Space Exploration in gem5
---

## Table of Contents

- [Introduction](#introduction)
- [Steps to Complete the Assignment](#steps-to-complete-the-assignment)
- [Specific Questions to Answer](#specific-questions-to-answer)
- [IMPORTANT](#important)

## Introduction

In this assignment, you will explore the design space of a heterogeneous architecture featuring both Big and Little cores. You will modify the cache configurations and memory channels to analyze their impact on performance. The goal is to understand how architectural choices affect system efficiency and performance metrics.

In this assignment you will take all of the different components that you have built throughout the bootcamp and put them together to explore the design space of an system-on-chip (SoC).

### Objectives:

- To gain hands-on experience with gem5 for architectural simulation.
- To analyze the performance of different core configurations and memory architectures.
- To visualize and interpret the results of your experiments.

## Steps to Complete the Assignment

1. **Set Up Your Environment**:
   - Create a new directory which contains all of the components you have built throughout the bootcamp.
   - `BigProcessor`, `LittleProcessor` from [Modeling CPU cores in gem5](/slides/02-Using-gem5/05-cores.md)
   - `ThreeLevelCache` from [Modeling caches in gem5](/slides/02-Using-gem5/04-cache-hierarchies.md)
   - `MultiChannelLPDDR5` from [Traffic generators](/slides/02-Using-gem5/03-traffic-generators.md)

2. **Modify Cache Configurations**:
   - Implement a different cache configuration. You could make the cache four levels or use a different replacement policy. Use your creativity!

3. **Run Simulations**:
   - Run the workloads from the [Getting Started Suite](https://resources.gem5.org/resources/riscv-getting-started-benchmark-suite?version=1.0.0) that we used in the [Multisim](/slides/02-Using-gem5/08-multisim.md) exercise.

> Note: There are some bugs in the multisim module that may cause the simulation to hang. If you encounter this issue, you can run the simulations one by one.

5. **Collect and Analyze Data**:
   - Gather performance metrics such as execution time, IPC (Instructions Per Cycle), and cache hit/miss rates.
   - Use matplotlib to create visualizations of your results.

## Specific Questions to Answer

1. **Performance Comparison**:
   - Compare the performance of the Big core and Little core configurations. What are the key differences in IPC and execution time?
   - When changing the cache and memory configurations, does the performance gap between the Big and Little cores change?

2. **Cache Impact**:
   - How does changing the cache configuration affect performance? Discuss the trade-offs observed between your three-level cache and the alternative cache.

3. **Memory Architecture**:
   - Analyze the impact of switching from DDR4 to LPDDR5. How does the increased number of memory channels influence performance metrics?

4. **Visualizations**:
   - Provide visualizations (graphs/charts) that illustrate your findings. Include at least:
     - A bar graph comparing IPC across different configurations.
     - A line graph showing execution time for each benchmark across configurations.

5. **Insights and Conclusions**:
   - Summarize your findings. What architectural choices led to the best performance? What recommendations would you make for future designs?

## **IMPORTANT**

Do not run a full cross product of all possible designs with all workloads.
It could take hours or days to run all of the simulations on a single machine.
Instead, focus on a few key configurations and workloads to analyze the impact of different architectural choices.
You can also run some preliminary experiments to see if some workloads are affected by certain changes more than others and concentrate your efforts on those workloads.
