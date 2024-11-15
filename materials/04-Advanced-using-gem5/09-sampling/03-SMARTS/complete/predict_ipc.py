from pathlib import Path
import math

stats_file = Path("/workspaces/2024/materials/02-Using-gem5/09-sampling/03-SMARTS/complete/m5out/stats.txt")

with stats_file.open("r") as f:
    num_samples = 0
    sample_ipc = []
    for line in f:
        if "board.processor.switch.core.ipc" in line:
            line = line.split()
            ipc = float(line[1])
            sample_ipc.append(ipc)
            num_samples += 1
    num_samples -= 1
    avg_ipc = sum(sample_ipc[:-1]) / num_samples
    print(f"Number of samples: {num_samples}")
    print(f"Predicted Overall IPC: {avg_ipc}")
    print(f"Actual Overall IPC: 1.247741")
    print(f"Relative Error: {(math.fabs(avg_ipc - 1.247741)/1.247741)*100}%")

