"""
Example script to demonstrate how to obtain a suite and its workloads

$ gem5 suite-example.py
...
SuiteResource(x86-getting-started-benchmark-suite
...
Workloads from npb:
Workload ID: x86-npb-is-size-s-run, version:
"""

from gem5.resources.resource import obtain_resource


getting_started_suite = obtain_resource("x86-getting-started-benchmark-suite")

print(getting_started_suite)

print(f"Input groups: {getting_started_suite.get_input_groups()}")

# Print all the available workloads in the suite
print("All available workloads:")
for workload in getting_started_suite:
    print(
        f"Workload ID: {workload.get_id()}, "
        f"version: {workload.get_resource_version()}"
    )

print("Workloads from npb:")
for workload in getting_started_suite.with_input_group("npb"):
    print(
        f"Workload ID: {workload.get_id()}, "
        f"version: {workload.get_resource_version()}"
    )
