GXX = g++
RISCV_GXX = riscv64-linux-gnu-g++
ARM_GXX = aarch64-linux-gnu-g++
GEM5_PATH ?= /workspaces/latin-america-2024/gem5

matrix-multiply: matrix-multiply.c
	$(GXX) -o matrix-multiply matrix-multiply.c \
		-I$(GEM5_PATH)/include \
		-L$(GEM5_PATH)/util/m5/build/x86/out \
		-lm5

matrix-multiply-riscv: matrix-multiply.c
	$(RISCV_GXX) -o matrix-multiply-riscv matrix-multiply.c \
		-I$(GEM5_PATH)/include \
		-L$(GEM5_PATH)/util/m5/build/riscv/out \
		-lm5 -static

matrix-multiply-arm: matrix-multiply.c
	$(ARM_GXX) -o matrix-multiply-arm matrix-multiply.c \
		-I$(GEM5_PATH)/include \
		-L$(GEM5_PATH)/util/m5/build/arm64/out \
		-lm5
