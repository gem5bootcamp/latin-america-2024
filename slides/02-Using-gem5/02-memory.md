---
marp: true
paginate: true
theme: gem5
title: Modeling Memory in gem5
---

<!-- _class: title -->

## Modeling Memory in gem5

DRAM and other memory devices!

**TO DO**: Improve the exercise and improve discussion of memory interleaving.

---

## Reminder: gem5's software architecture

**Ports** are used to connect components in gem5. They are used to send and receive *packets* between components.

The memory controller has a *response port* which receives requests from something on the "cpu side" and sends responses.

The memory object has two jobs:

1. Model the functional memory data and respond with the correct data for the memory request.
2. Model the timing behavior of the memory device.

![Overview of gem5's software architecture with ports connecting components. left](../01-Introduction/02-simulation-background-imgs/abstractions-1.drawio.svg)

---

<!-- _class: center-image -->

## Memory System

### gem5's memory system consists of two main components

1. *Memory Controller*: Orders and schedules read and write requests
2. *Memory Interface(s)*: Implements the timing and architecture of the memory device

![Diagram of the gem5 memory system](02-memory-imgs/memory-system.drawio.svg)

---

<!-- _class: center-image -->

## Memory Controller

### When `MemCtrl` receives packets...

1. Packets enqueued into the read and/or write queues
2. Applies **scheduling algorithm** (FCFS, FR-FCFS, ...) to issue read and write requests

![Diagram of the gem5 memory controller queues](02-memory-imgs/memory-controller-queues.drawio.svg)

---

<!-- _class: center-image -->

## Memory Interface

- The memory interface implements the **architecture** and **timing parameters** of the chosen memory type.
- It manages the **media specific operations** like activation, pre-charge, refresh and low-power modes, etc.

![Diagram of the gem5 memory interface](02-memory-imgs/memory-interface.drawio.svg)

---

## Included memory controllers

### `MemCtrl`

This is the most common memory controller. Used for all DDR devices, LPDDR devices, and other DRAM devices.

### `HeteroMemCtrl`

This memory controller allows you to have a heterogeneous memory system.
You can have both DRAM (e.g., DDR devices) and non-volatile memory (e.g., NVM devices) in the same system. This is like 3DXPoint systems where DRAM and NVM have separate memory spaces.

### `HBMCtrl`

This is a controller specifically for HBM (High Bandwidth Memory) devices.
HBM needs its own controller because of the pseudo-channel architecture.
Each HBM controller actually has two different HBM interfaces to model the two pseudo-channels.

---

## How the memory model works

- The memory controller is responsible for scheduling and issuing read and write requests
- It obeys the timing parameters of the memory interface
  - `tCAS`, `tRAS`, etc. are tracked *per bank* in the memory interface
  - Use gem5 *events* ([more later](../03-Developing-gem5-models/03-event-driven-sim.md)) to schedule when banks are free

The model isn't "cycle accurate," but it's *cycle level* and quite accurate compared to other DRAM simulators such as [DRAMSim](https://github.com/umd-memsys/DRAMsim3) and [DRAMSys](https://github.com/tukl-msd/DRAMSys).

You can extend the interface for new kinds of memory devices (e.g., DDR6), but usually you will use interfaces that have already been implemented.

The main way gem5's memory is normally configured is the number of channels and the channel/rank/bank/row/column bits since systems rarely use bespoke memory devices.

---

## Address Interleaving

### Idea: we can parallelize memory accesses

- For example, we can access multiple banks/channels/etc at the same time
- Use part of the address as a selector to choose which bank/channel to access
- Allows contiguous address ranges to interleave between banks/channels

---

<!-- _class: center-image -->

## Address Interleaving

### For example...

![Diagram showing an example of address interleaving](02-memory-imgs/address-interleaving.drawio.svg)

---

## Address Interleaving

### Using address interleaving in gem5

- We can use AddrRange constructors to define a selector function
  - [`src/base/addr_range.hh`](../../gem5/src/base/addr_range.hh)

- Example: standard library's multi-channel memory
  - [`gem5/src/python/gem5/components/memory/multi_channel.py`](../../gem5/src/python/gem5/components/memory/multi_channel.py)

---

## Memory in the standard library

The standard library wraps the DRAM/memory models into `MemorySystem`s.

Many examples are already implemented in the standard library for you.

See [`gem5/src/python/gem5/components/memory/multi_channel.py`](../../gem5/src/python/gem5/components/memory/multi_channel.py) and [`gem5/src/python/gem5/components/memory/single_channel.py`](../../gem5/src/python/gem5/components/memory/single_channel.py) for examples.

Additionally,

- `SimpleMemory()` allows the user to not worry about timing parameters and instead, just give the desired latency, bandwidth, and latency variation.
- `ChanneledMemory()` encompasses a whole memory system (both the controller and the interface).
- `ChanneledMemory` provides a simple way to use multiple memory channels.
- `ChanneledMemory` handles things like scheduling policy and interleaving for you.
