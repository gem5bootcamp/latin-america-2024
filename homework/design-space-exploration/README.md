---
Author: Jason Lowe-Power
Title: Design Space Exploration in gem5
---

## Table of Contents

- [Introduction](#introduction)
- [Steps to Complete the Assignment](#steps-to-complete-the-assignment)
- [Specific Questions to Answer](#specific-questions-to-answer)
- [IMPORTANT](#important)
- [Submission](#submission)

**Suggested due date**: 27/12/2024 23:59

**Final due date**: 13/12/2024 23:59

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

> Note: There are some bugs in the multisim module that may cause the simulation to hang. If you encounter this issue, you can run the simulations one by one. To do this, you can list all the experiments with `gem5 <your multisim script>.py --list` and run them one at a time with `gem5 <your multisim script>.py <experiment name>`. You can get the experiment names from the list command.

5. **Collect and Analyze Data**:
   - Gather performance metrics such as execution time, IPC (Instructions Per Cycle), and cache hit/miss rates.
   - Use matplotlib to create visualizations of your results.

## Specific Questions to Answer

For the following questions, provide visualizations (graphs/charts) that illustrate your findings. The [matplotlib](https://matplotlib.org/) library or [seaborn](https://seaborn.pydata.org/) is useful. Include at least a bar graph comparing IPC across different configurations.

> Hint: GitHub Copilot (or ChatGPT) is *very good* at generating matplotlib code snippets. You can use it to generate the code for your visualizations.

1. **Performance Comparison**:
   - Compare the performance of the Big core and Little core configurations. What are the key differences in IPC and execution time? How do the two configurations perform across different workloads?
   - When changing the cache and memory configurations, does the performance gap between the Big and Little cores change?

2. **Cache Impact**:
   - How does changing the cache configuration affect performance? Discuss the trade-offs observed between your three-level cache and the alternative cache.

3. **Insights and Conclusions**:
   - Summarize your findings. What architectural choices led to the best performance? What recommendations would you make for future designs?

## **IMPORTANT**

Do not run a full cross product of all possible designs with all workloads.
It could take hours or days to run all of the simulations on a single machine.
Instead, focus on a few key configurations and workloads to analyze the impact of different architectural choices.
You can also run some preliminary experiments to see if some workloads are affected by certain changes more than others and concentrate your efforts on those workloads.

## Submission

You will submit this assignment using GitHub Classroom.
Use the "blank" repository that was created for you.

Create a new file named "hw2_submission.md" in the root of your repository and include the answers to the nine questions above.
After completing the assignment, commit and push your changes to the repository.

**Be sure to add your name and email address to the README.md file.**
This way we can associate your submission with you.
