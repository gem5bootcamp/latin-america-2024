GEM5_PATH = /workspaces/2024/gem5
ISA = arm64
GXX = aarch64-linux-gnu-g++


all: 04-cross-compile-this-static 04-cross-compile-this-dynamic

04-cross-compile-this-static: 04-cross-compile-this.cpp
# compile command with -static flag

04-cross-compile-this-dynamic: 04-cross-compile-this.cpp
# compile command without -static flag

clean:
	rm -f 04-cross-compile-this-static 04-cross-compile-this-dynamic

