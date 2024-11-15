baseline_ipc = 0.0
baseline_stats_file = "/workspaces/2024/materials/02-Using-gem5/09-sampling/01-simpoint/full-detailed-run-m5out/stats.txt"

with open(baseline_stats_file, "r") as f:
    for line in f:
        if "board.processor.cores.core.ipc" in line:
            line = line.split()
            baseline_ipc = float(line[1])
            break

num_simpoints = 3
simpoint_ipcs = []
simpoint_weights = []

for i in range(num_simpoints):
    simpoint_stats_file = f"/workspaces/2024/materials/02-Using-gem5/09-sampling/01-simpoint/simpoint{i}-run/stats.txt"
    with open(simpoint_stats_file, "r") as f:
        simpoint_ipc = 0.0
        for line in f:
            if "board.processor.cores.core.ipc" in line:
                line = line.split()
                simpoint_ipc = float(line[1])
        simpoint_ipcs.append(simpoint_ipc)
    simpoint_stdout_file = f"/workspaces/2024/materials/02-Using-gem5/09-sampling/01-simpoint/simpoint{i}-run/simout.txt"
    simpoint_weight = 0.0
    with open(simpoint_stdout_file, "r") as f:
        for line in f:
            if "Ran SimPoint" in line:
                line = line.split()
                simpoint_weight = float(line[-1])
    simpoint_weights.append(simpoint_weight)

predicted_ipc = 0.0

for i in range(num_simpoints):
    predicted_ipc += simpoint_ipcs[i] * simpoint_weights[i]

print(f"predicted IPC: {predicted_ipc}")
print(f"actual IPC: {baseline_ipc}")
print(f"relative error: {(abs(baseline_ipc - predicted_ipc)/baseline_ipc)*100}%")
