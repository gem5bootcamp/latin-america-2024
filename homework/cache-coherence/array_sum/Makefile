GEM5_ROOT ?= ../../gem5

all: all-gem5 all-native
all-gem5: naive-gem5 chunking-gem5 res-race-opt-gem5 chunking-res-race-opt-gem5 block-race-opt-gem5 all-opt-gem5
all-native: naive-native chunking-native res-race-opt-native chunking-res-race-opt-native block-race-opt-native all-opt-native

clean:
	rm naive-native chunking-native res-race-opt-native chunking-res-race-opt-native block-race-opt-native all-opt-native
	rm naive-gem5 chunking-gem5 res-race-opt-gem5 chunking-res-race-opt-gem5 block-race-opt-gem5 all-opt-gem5

naive-native: array_sum.cpp
	g++ array_sum.cpp -o naive-native -static -DNAIVE -lpthread

chunking-native: array_sum.cpp
	g++ array_sum.cpp -o chunking-native -static -DCHUNKING -lpthread

res-race-opt-native: array_sum.cpp
	g++ array_sum.cpp -o res-race-opt-native -static -DRES_RACE_OPT -lpthread

chunking-res-race-opt-native: array_sum.cpp
	g++ array_sum.cpp -o chunking-res-race-opt-native -static -DCHUNKING_RES_RACE_OPT -lpthread

block-race-opt-native: array_sum.cpp
	g++ array_sum.cpp -o block-race-opt-native -static -DBLOCK_RACE_OPT -lpthread

all-opt-native: array_sum.cpp
	g++ array_sum.cpp -o all-opt-native -static -DALL_OPT -lpthread

naive-gem5: array_sum.cpp
	g++ array_sum.cpp -o naive-gem5 -static -DNAIVE -lpthread -DGEM5 -I../include -L../lib/x86 -lm5

chunking-gem5: array_sum.cpp
	g++ array_sum.cpp -o chunking-gem5 -static -DCHUNKING -lpthread -DGEM5 -I../include -L../lib/x86 -lm5

res-race-opt-gem5: array_sum.cpp
	g++ array_sum.cpp -o res-race-opt-gem5 -static -DRES_RACE_OPT -lpthread -DGEM5 -I../include -L../lib/x86 -lm5

chunking-res-race-opt-gem5: array_sum.cpp
	g++ array_sum.cpp -o chunking-res-race-opt-gem5 -static -DCHUNKING_RES_RACE_OPT -lpthread -DGEM5 -I../include -L../lib/x86 -lm5

block-race-opt-gem5: array_sum.cpp
	g++ array_sum.cpp -o block-race-opt-gem5 -static -DBLOCK_RACE_OPT -lpthread -DGEM5 -I../include -L../lib/x86 -lm5

all-opt-gem5: array_sum.cpp
	g++ array_sum.cpp -o all-opt-gem5 -static -DALL_OPT -lpthread -DGEM5 -I../include -L../lib/x86 -lm5
