GEM5_PATH = /workspaces/2024/gem5
ISA = arm64
GXX = aarch64-linux-gnu-g++


all: 04-cross-compile-this-static 04-cross-compile-this-dynamic

04-cross-compile-this-static: 04-cross-compile-this.cpp
	$(GXX) -o 04-cross-compile-this-static 04-cross-compile-this.cpp -static -I$(GEM5_PATH)/include -L$(GEM5_PATH)/util/m5/build/$(ISA)/out -lm5

04-cross-compile-this-dynamic: 04-cross-compile-this.cpp
	$(GXX) -o 04-cross-compile-this-dynamic 04-cross-compile-this.cpp -I$(GEM5_PATH)/include -L$(GEM5_PATH)/util/m5/build/$(ISA)/out -lm5

clean:
	rm -f 04-cross-compile-this-static 04-cross-compile-this-dynamic

