#include <atomic>
#include <iostream>
#include <thread>
#include <vector>

#ifdef GEM5
#include <gem5/m5ops.h>
#endif

void sum_1(int *array, std::atomic<int> *result, size_t length, size_t tid, size_t threads)
{
    for (int i=tid; i < length; i += threads) {
        *result += array[i];
    }
}

void sum_2(int *array, std::atomic<int> *result, size_t length, size_t tid, size_t threads)
{
    size_t chunk_size = (length+threads-1)/threads;
    for (int i=tid*chunk_size; i < (tid+1)*chunk_size && i < length; i++) {
        *result += array[i];
    }
}

void sum_3(int *array, std::atomic<int> *result, size_t length, size_t tid, size_t threads)
{
    for (int i=tid; i < length; i += threads) {
        result[tid] += array[i];
    }
}

void sum_4(int *array, std::atomic<int> *result, size_t length, size_t tid, size_t threads)
{
    size_t chunk_size = (length+threads-1)/threads;
    for (int i=tid*chunk_size; i < (tid+1)*chunk_size && i < length; i++) {
        result[tid] += array[i];
    }
}

void sum_5(int *array, std::atomic<int> *result, size_t length, size_t tid, size_t threads)
{
    for (int i=tid; i < length; i += threads) {
        result[tid*16] += array[i];
    }
}

void sum_6(int *array, std::atomic<int> *result, size_t length, size_t tid, size_t threads)
{
    size_t chunk_size = (length+threads-1)/threads;
    for (int i=tid*chunk_size; i < (tid+1)*chunk_size && i < length; i++) {
        result[tid*16] += array[i];
    }
}

void print_usage()
{
    std::cout << "This program sums up an array into one number." << std::endl;
    std::cout << "Please refer to the usage below for arguments to pass." << std::endl;
    std::cout << "{array length: int} {number of threads: int}." << std::endl;
}

int main(int argc, char* argv[])
{
    if (argc != 3) {
        print_usage();
        return 1;
    }

    int length = atoi(argv[1]);

    if (length <= 0 or length > 65536) {
        std::cout << "Array length must be above 0 and less than 65536" << std::endl;
        print_usage();
        return 2;
    }

    int threads = atoi(argv[2]);

    if (threads <= 0 || threads > std::thread::hardware_concurrency()) {
        std::cout << "Threads must be above 0 and below 8" << std::endl;
        print_usage();
        return 3;
    }

    std::cout << "Initializing array and reseting result." << std::endl;
    int* array = new int[length];
    std::atomic<int>* result = new std::atomic<int> [threads * 16]; // Enough room for 64 bytes for each int
    for (int i=0; i<threads*16; i++) {
        result[i] = 0;
    }
    for (int i=0; i<length; i++) {
        array[i] = i;
    }
    std::vector<std::thread> thread_pool;
    std::cout << "Done initializing." << std::endl;

#ifdef NAIVE
    auto func = sum_1;
    std::cout << "Using a naive approach to sum up the array." << std::endl;
#endif

#ifdef CHUNKING
    auto func = sum_2;
    std::cout << "Chunking the array for summation." << std::endl;
#endif

#ifdef RES_RACE_OPT
    auto func = sum_3;
    std::cout << "Removing race condition on result." << std::endl;
#endif

#ifdef CHUNKING_RES_RACE_OPT
    auto func = sum_4;
    std::cout << "Removing race condition on result and using chunking." << std::endl;
#endif

#ifdef BLOCK_RACE_OPT
    auto func = sum_5;
    std::cout << "Removing race condition on cache blocks holding result array." << std::endl;
#endif

#ifdef ALL_OPT
    auto func = sum_6;
    std::cout << "Removing race condition on cache blocks and using chunking to sum up the array." << std::endl;
#endif

    std::cout << "Beginning summation ..." << std::endl;
    auto start = std::chrono::high_resolution_clock::now();

#ifdef GEM5
    m5_work_begin(0, 0);
#endif

#if defined(NAIVE) || defined(CHUNKING) || defined(RES_RACE_OPT) || defined(CHUNKING_RES_RACE_OPT) || defined(BLOCK_RACE_OPT) || defined(ALL_OPT)
    for (int i=0; i<threads; i++) {
        thread_pool.emplace_back(func, array, result, length, i, threads);
    }

    for (auto &thread: thread_pool) {
        thread.join();
    }

    for (int i=1; i<threads*16; i++) {
        result[0] += result[i];
    }
#endif

#ifdef GEM5
    m5_work_end(0, 0);
#endif

    auto end = std::chrono::high_resolution_clock::now();

    std::cout << "Done." << std::endl;
    std::cout << "Time " << (double) (end - start).count() / 1e6 << " ms" << std::endl;
    if (result[0] != ((uint) length) * ((uint)(length - 1)) / 2) {
        std::cout << "ERROR: RESULT WRONG!" << std::endl;
        std::cout << "Expected " << ((uint)length)*((uint)(length-1))/2 << " got " << result[0] << std::endl;
    }

    delete[] array;
    delete[] result;
    return 0;
}
