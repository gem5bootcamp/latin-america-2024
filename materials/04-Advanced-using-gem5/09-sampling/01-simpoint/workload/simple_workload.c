#include <stdlib.h>
#include <stdio.h>

#define ARRAY_SIZE 1000
#define NUM_ITERATIONS 1000

int main() {
    unsigned long long i, j;
    unsigned long long sum = 0;
    unsigned long long *array = (unsigned long long *)malloc(ARRAY_SIZE * sizeof(unsigned long long));

    for (i = 0; i < ARRAY_SIZE; i++) {
        array[i] = i * i;
    }

    for (i = 0; i < NUM_ITERATIONS; i++) {
        for (j = 0; j < ARRAY_SIZE; j++) {
            sum += array[j];
        }
    }

    printf("Sum: %llu\n", sum);

    return 0;
}
