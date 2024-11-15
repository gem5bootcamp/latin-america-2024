#!/bin/bash

# Copyright (c) 2024 The Regents of the University of California.
# SPDX-License-Identifier: BSD 3-Clause

# Install the necessary packages
apt-get install -y build-essential libboost-all-dev

echo "Installing GAP Benchmark Suite"
git clone https://github.com/sbeamer/gapbs.git
cd gapbs
# Build the benchmark suite
make
