cd /workspaces/2024/gem5/util/m5 && scons build/x86/out/m5;
echo built x86 m5ops library;
cd /workspaces/2024/gem5/util/m5 && scons arm64.CROSS_COMPILE=aarch64-linux-gnu- build/arm64/out/m5;
echo built arm64 m5ops library;
cd /workspaces/2024/materials/02-Using-gem5/03-running-in-gem5/01-build-m5ops-library/complete;
