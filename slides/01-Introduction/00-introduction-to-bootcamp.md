---
marp: true
paginate: true
theme: gem5
title: Getting Started with gem5
author: Jason Lowe-Power
---

<!-- _class: title -->

## Welcome to the gem5 bootcamp!

---

## About the overall structure of the bootcamp

These slides and are available at <https://gem5bootcamp.github.io/latin-america-2024> for you to follow along.

(Note: They will be archived at <https://gem5bootcamp.github.io/latin-america-2024>)

The source for the slides, and what you'll be using throughout the bootcamp can be found on github at <https://github.com/gem5bootcamp/latin-america-2024>

> Note: Don't clone that repo, yet. We'll do that in a bit.

---

<!-- _class: two-col -->

## A bit about us

I am **Prof. Jason Lowe-Power** (he/him).
I am an associate professor in the Computer Science Department and
the *Project Management Committee chair* for the gem5 project.

I lead the Davis Computer Architecture Research (DArchR) Group.

<https://arch.cs.ucdavis.edu>

![UC Davis logo width:500px](00-introduction-to-bootcamp-imgs/expanded_logo_gold-blue.png)

![DArchR logo width:550px](00-introduction-to-bootcamp-imgs/darchr.png)

---

## The bootcamp team

![Everyone who has contributed to the bootcamp width:1200px](00-introduction-to-bootcamp-imgs/devs.drawio.svg)

---

<!-- _class: outline -->

## Plan for the week

### Day 1

- Introduction
  - [Background on simulation](01-simulation-background.md) <!-- 1 hour (Jason) -->
    - What is is simulation and why does it matter
    - gem5 history
  - [Getting started with gem5](02-getting-started.md) <!-- 30 minutes (Jason) -->
    - Getting into the codespace environment
    - Running your first simulation
  - [Background on Python and gem5](03-python-background.md) <!--  1.5 hours (Bobby) -->
    - Python basics
    - Python in gem5
    - Object-oriented programming in Python
- Using gem5
  - [gem5's standard library](../02-Using-gem5/01-stdlib.md) <!--  2 hours (Bobby) -->
  - [gem5 resources](../02-Using-gem5/02-gem5-resources.md) <!--  1 hour (Harshil) -->
    - What are resources? (Disks, kernels, binaries, etc.)
    - How to get resources
    - How to use resources
    - Workloads and suites
    - Local resources

### Day 2

- Using gem5
  - [Running things in gem5](../02-Using-gem5/03-running-in-gem5.md) <!--  2 hours (Erin / Zhantong) -->
    - Intro to syscall emulation mode
    - The gem5-bridge utility and library
    - Cross compiling
    - Traffic generator (Test board)
    - Process.map and drivers in SE mode (maybe cut)
  - [Modeling cores in gem5](../02-Using-gem5/04-cores.md) <!--  1 hour (Mysore / Jason) -->
    - CPU models in gem5
    - Using the CPU models
    - Branch predictors
    - Look at the gem5 generated statistics
    - Overview of ISAs and tradeoffs
  - [Modeling caches in gem5](../02-Using-gem5/05-cache-hierarchies.md) <!--  1.5 hour (Leo / Mahyar) -->
    - Cache models in gem5 (Ruby and classic)
    - Using the cache models
    - Replacement policies
    - Tag policies
    - Tradeoffs between classic and Ruby
    - Look at the gem5 generated statistics
  - [Modeling memory in gem5](../02-Using-gem5/06-memory.md) <!-- 1 hours (Noah / William (Maryam)) -->
    - Memory models in gem5
    - Using the memory models
    - Testing memory with traffic generators
    - Comm Monitor
  - [Full system simulation](../02-Using-gem5/07-full-system.md) <!--(Harshil) 1 hour -->
    - What is full system simulation?
    - Basics of booting up a real system in gem5
    - Creating disk images using packer and qemu
    - Extending/modifying a gem5 disk image
    - m5term to interact with a running system

### Day 3

- Using gem5
  - [Accelerating simulation](../02-Using-gem5/08-accelerating-simulation.md) <!--  (Zhantong) 0.5 hours -->
    - KVM fast forwarding
    - Checkpointing
  - [Sampled simulation with gem5](../02-Using-gem5/09-sampling.md) <!--  (Zhantong) 1.5 hours -->
    - Simpoint & Looppoint ideas
    - Simpoint & Loopoint analysis
    - Simpoint & Loopoint checkpoints
    - How to analyze sampled simulation data
    - Statistical simulation ideas
    - Statistical simulation running and analysis
  - [Power modeling](../02-Using-gem5/10-modeling-power.md) <!--  (Jason?) -->
  - [Multisim](../02-Using-gem5/11-multisim.md) <!-- (Bobby) (10 minutes) -->
    - Example using multisim
- Developing gem5 models
  - [SimObject intro](../03-Developing-gem5-models/01-sim-objects-intro.md) <!-- (Mahyar) 0.5 hours -->
    - Development environment, code style, git branches
    - The most simple `SimObject`
    - Simple run script
    - How to add parameters to a `SimObject`
  - [Debugging and debug flags](../03-Developing-gem5-models/02-debugging-gem5.md) <!-- (Mahyar) 0.5 hours -->
    - How to enable debug flags (examples of DRAM and Exec)
    - `--debug-help`
    - Adding a new debug flag
    - Functions other than DPRINTF
    - Panic/fatal/assert
    - gdb?
  - [Event-driven simulation](../03-Developing-gem5-models/03-event-driven-sim.md) <!-- (Mahyar) 1 hours -->
    - Creating a simple callback event
    - Scheduling events
    - Modeling bandwidth and latency with events
    - Other SimObjects as parameters
    - Hello/Goodbye example with buffer
    - Clock domains?

### Day 4

- Developing gem5 models
  - [Modeling Cores](../03-Developing-gem5-models/05-modeling-cores.md) <!-- (Bobby) 1.5 hours -->
    - New instructions
    - How the execution model works
    - Debugging
  - [Modeling cache coherence with Ruby and SLICC](../03-Developing-gem5-models/06-modeling-cache-coherence.md) <!--  (Jason) 1.5 hours -->
    - Ruby intro
    - Structure of SLICC
    - Building/running/configuring protocols
    - Debugging
    - Ruby network
    - (Note to Jason: could do a whole day here if split like before.)
  - [Extending gem5](../03-Developing-gem5-models/09-extending-gem5-models.md) <!-- (Zhantong) 1 hours -->
    - Probe points
    - Generic cache object
    - Base utilities (e.g., bitset)
    - Random numbers
    - Signal ports?
- [GPU modeling](../04-GPU-model/01-intro.md) <!-- (Matt S.) -->

### Day 5

- Developing gem5 models
  - [Ports and memory-based SimObjects](../03-Developing-gem5-models/04-ports.md) <!-- (Mahyar) 1 hours -->
    - Idea of ports (request/response), packets, interface
    - A simple memory object that forwards things
    - Connecting ports and writing config files
    - Adding stats to a SimObject
    - Adding latency and and modeling buffers/computing time
  - [Using the CHI protocol](../03-Developing-gem5-models/07-chi-protocol.md) <!-- (Jason) 0.5 hours -->
    - How is CHI different from other protocols?
    - Configuring a CHI hierarchy
  - [Modeling the on-chip network with Garnet](../03-Developing-gem5-models/08-ruby-network.md) <!-- (Jason) 1 hours -->
    - Garnet intro
    - Building/running/configuring networks
    - Debugging
- Other simulators <!-- (Jason?) -->
  - [SST](../05-Other-simulators/01-sst.md)
  - [DRAMSim/DRAMSys](../05-Other-simulators/02-dram.md)
  - [SystemC](../05-Other-simulators/03-systemc.md)
- Contributing to gem5 <!-- (Bobby) -->
  - [gem5 contributing process](../06-Contributing-to-gem5/01-contributing.md)
  - [gem5 testing](../06-Contributing-to-gem5/02-testing.md)

---

## Our goals for the gem5 bootcamp

- Make gem5 less painful and flatten the learning curve
- Give you a vocabulary for asking questions​
- Provide a reference for the future​
- Give you material to take back and teach your colleagues

### Other likely outcomes

- You will be overwhelmed by the amount of information and how large gem5 is
  - That's OK! You can take these materials with you and refer back to them
- You will not understand everything
  - That's OK! You can ask questions as we go

---

## How this is going to work

- We'll be going mostly top-down
  1. How to use gem5
  2. How to each model can be used
  3. How to develop your own models and modify existing models
- Highly iterative:
  - You'll see the same thing over and over
  - Each time it will be one level deeper
- Lots of coding examples
  - Both live coding and practice problems

---

## Coding examples

You can write the following code

```python
print("Hello, world!")
print("You'll be seeing a lot of Python code")
print("The slides will be a reference, but we'll be doing a lot of live coding!")
```

And you'll see this output.

```console
Hello, world!
You'll be seeing a lot of Python code
The slides will be a reference, but we'll be doing a lot of live coding!
```

---

## Bootcamp logistics

---

## Other admin things

---

## Important resources

### Bootcamp links

- [Bootcamp website](https://gem5bootcamp.gem5.org/) (Maybe you're here now)
  - [Bootcamp archive](https://gem5bootcamp.github.io/2024) (If you're coming to this later)
- [Source for bootcamp materials](https://github.com/gem5bootcamp/2024) (You'll work here)
- [GitHub Classroom](https://classroom.github.com/a/gCcXlgBs) (Needed to use codespaces)

### gem5 links

- [gem5 code](https://github.com/gem5/gem5)
- [gem5 website](https://www.gem5.org/)
- [gem5 YouTube](https://youtube.com/@gem5)
- [gem5 Slack](https://gem5-workspace.slack.com/join/shared_invite/zt-2e2nfln38-xsIkN1aRmofRlAHOIkZaEA) (for asking offline questions)
