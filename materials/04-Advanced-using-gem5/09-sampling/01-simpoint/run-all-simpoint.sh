#!/bin/bash

# Run the gem5 commands in parallel
gem5 -re --outdir=simpoint0-run simpoint-run.py --sid=0 &
pid0=$!
gem5 -re --outdir=simpoint1-run simpoint-run.py --sid=1 &
pid1=$!
gem5 -re --outdir=simpoint2-run simpoint-run.py --sid=2 &
pid2=$!

# Array of PIDs and SIDs
pids=($pid0 $pid1 $pid2)
sids=(0 1 2)

# Loop to wait for each process and echo a message when it finishes
for i in "${!pids[@]}"; do
    wait ${pids[$i]} && echo "gem5 with sid ${sids[$i]} finished"
done

# Wait for all background jobs to finish
wait
