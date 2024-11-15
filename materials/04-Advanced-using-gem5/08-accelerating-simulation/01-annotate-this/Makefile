GEM5_PATH = /workspaces/2024/gem5
ISA = x86
GXX = g++


all: 01-annotate-this

01-annotate-this: 01-annotate-this.cpp
	$(GXX) -o 01-annotate-this 01-annotate-this.cpp -no-pie -I$(GEM5_PATH)/include -L$(GEM5_PATH)/util/m5/build/$(ISA)/out -I$(GEM5_PATH)/util/m5/src -lm5

clean:
	rm -f 01-annotate-this
