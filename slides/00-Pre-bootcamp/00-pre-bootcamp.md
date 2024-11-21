---
marp: true
paginate: true
theme: gem5
title: "gem5 bootcamp: Latin America 2024"
author: Jason Lowe-Power
---

<!-- _class: title -->

## gem5 bootcamp: Latin America 2024

Some things to get you started before the bootcamp

---

## Pre-bootcamp Reading

### If you want to get familiar with gem5

These papers are good to skim. You do not need to read carefully.

- The original gem5 paper: [The gem5 simulator](https://dl.acm.org/doi/pdf/10.1145/2024716.2024718)
- The gem5-20 paper: [The gem5 Simulator: Version 20.0+](https://arxiv.org/pdf/2007.03152)

The "original" paper was published in 2011 just after m5 and GEMS combined to form gem5 and is a good overview of the simulator architecture and models included at that time.

The new gem5-20 paper discusses the changes since the 2011 paper and provides an overview of the current models in gem5.

---

## Pre-bootcamp Reading on Secure Memory

In the bootcamp, we will be building a secure memory component. The following papers are a good introduction to secure memory:

- [AEGIS: A single-chip secure processor](./00-pre-bootcamp-imgs/AEGIS-SecureProcessor.pdf "download")
- [Efficient Memory Integrity Verification and Encryption for Secure Processor](./00-pre-bootcamp-imgs/Efficient_memory_integrity_verification_and_encryption_for_secure_processors.pdf "download")
- [Caches and Hash Trees for Efficient Memory Integrity Verification](./00-pre-bootcamp-imgs/Caches_and_hash_trees_for_efficient_memory_integrity_verification.pdf "download")
- [Using Address Independent Seed Encryption and Bonsai Merkle Trees to Make Secure Processors OS- and Performance-Friendly](./00-pre-bootcamp-imgs/Using_Address_Independent_Seed_Encryption_and_Bonsai_Merkle_Trees_to_Make_Secure_Processors_OS-_and_Performance-Friendly.pdf "download")
- [PoisonIvy: Safe Speculation for Secure Memory](./00-pre-bootcamp-imgs/PoisonIvy_Safe_speculation_for_secure_memory.pdf "download")

---

## Pre-bootcamp prep

The prerequisites for the bootcamp:

- Undergraduate computer architecture
  - Memory architecture
  - Caches
  - In-order and out-of-order processor design
  - Multicore architecture and cache coherence
- C++
- Python
  - The [next slidedeck](01-python-background.md) covers a python reminder
