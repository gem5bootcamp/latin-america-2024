GEM5_PATH = /workspaces/2024/gem5
ISA = x86
GXX = g++


all: 02-annotate-this

02-annotate-this: 02-annotate-this.cpp
	$(GXX) -o 02-annotate-this 02-annotate-this.cpp -I$(GEM5_PATH)/include -L$(GEM5_PATH)/util/m5/build/$(ISA)/out -lm5

clean:
	rm -f 02-annotate-this

