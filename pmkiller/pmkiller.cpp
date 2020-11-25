#include <iostream>
#include <thread>
#include <mutex>
#include <vector>

//#include <algorithm>
#include <chrono>

#ifdef __linux__
#include <sched.h>
#endif

#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <pthread.h>
#include <immintrin.h>

#include <signal.h>

#include "pmperf.h"

using namespace std;

mutex iomutex;

#define CACHE_LINE_SIZE 0x40
#define XP_LINE_SIZE 0x100

#ifndef MAP_SYNC
#define MAP_SYNC 0x80000
#endif

#ifndef MAP_SHARED_VALIDATE
#define MAP_SHARED_VALIDATE 0x03
#endif

#define ONE_MB 1024*1024
#define ONE_KB 1024

#define FOOTPRINT ONE_KB

// typedef union __xp256B {
//     char                ch[256];    // 1B * 256
//     unsigned int        ui[64];     // 4B * 64
//     unsigned long long  ull[32];    // 8B * 32
//     __m512i             m512[4];    // 64B * 4
// }__xp256B;


uint64 total_flushed = 0;

uint64 seq_clflushopt(void * addr, size_t bytes) {

    size_t max_flush = 0x3fffffff;
    uint64 flushed = 0;

    asm volatile ("mfence":::"memory");

    asm volatile (
        "mov %[start_addr], %%r9 \n"
        "movq %[start_addr], %%xmm0 \n"

        "xor %%r10, %%r10 \n"

        "0:\n"
        "xor %%r8, %%r8 \n"

        "1:\n"
        "vmovdqa64 %%zmm0, 0x0(%%r9, %%r8) \n"
        "clflushopt (%%r9, %%r8) \n"
        "add $1, %%r10 \n"
        "add $0x40, %%r8 \n"
        "cmp %[bytes], %%r8 \n"
        "jl 1b \n"

        "cmp %[max_flush], %%r10 \n"
        "jl 0b \n"

        "2:\n"
        "mov %%r10, %[flushed]"
        : [flushed]"+m"(flushed)
        : [start_addr]"r"(addr), [bytes]"r"(bytes), [max_flush]"r"(max_flush)
        : "%r8", "%r9", "%r10"
    );

    asm volatile ("mfence":::"memory");

    return flushed;
}

uint64 seq_clwb(void * addr, size_t bytes) {

    size_t max_flush = 0x3fffffff;
    uint64 flushed = 0;

    asm volatile ("mfence":::"memory");

    asm volatile (
        "mov %[start_addr], %%r9 \n"
        "movq %[start_addr], %%xmm0 \n"

        "xor %%r10, %%r10 \n"

        "0:\n"
        "xor %%r8, %%r8 \n"

        "1:\n"
        "vmovdqa64 %%zmm0, 0x0(%%r9, %%r8) \n"
        "clwb (%%r9, %%r8) \n"
        "add $1, %%r10 \n"
        "add $0x40, %%r8 \n"
        "cmp %[bytes], %%r8 \n"
        "jl 1b \n"

        "cmp %[max_flush], %%r10 \n"
        "jl 0b \n"

        "2:\n"
        "mov %%r10, %[flushed]"
        : [flushed]"+m"(flushed)
        : [start_addr]"r"(addr), [bytes]"r"(bytes), [max_flush]"r"(max_flush)
        : "%r8", "%r9", "%r10"
    );

    asm volatile ("mfence":::"memory");

    return flushed;
}

void thread_func(int tid)
{
    int fd;
    char buf[40];
    void * pmaddr;

    uint64 flushed;

    sprintf(buf, "/mnt/pmemfs1.%d/data", tid);
    // open a pmem file and memory map it
    if ((fd = open(buf, O_RDWR)) < 0){
        cerr  << "file open error: " << buf << endl;
    }

    if ((pmaddr = mmap(NULL, FOOTPRINT,
                        PROT_READ | PROT_WRITE,
                        MAP_SHARED_VALIDATE | MAP_SYNC,
                        fd, 0)) == MAP_FAILED){
        cerr << "mmap error: " << buf << endl;
    }
    close(fd);

    flushed = seq_clwb(pmaddr, FOOTPRINT);
    {
        lock_guard<mutex> iolock(iomutex);
        total_flushed += flushed;
    }
    // Simulate important work done by the tread by sleeping for a bit...
    //this_thread::sleep_for(chrono::milliseconds(900));

    munmap(pmaddr, FOOTPRINT);
}

void sigint_handler(int signo)
{
    cerr << "Stopping..." << endl;
    return;
}

int main(int argc, const char** argv) {
    const static int cpu_offset = 28;

    signal(SIGINT, sigint_handler);

	PmPerf * monitor = new PmPerf();
	monitor->pmm_program();

    unsigned num_threads = thread::hardware_concurrency()/2;

    // A mutex ensures orderly access to cout from multiple threads.

    vector<thread> threads(num_threads);

	monitor->before();

	for (unsigned i = 0; i < num_threads; ++i) {
        threads[i] = thread( thread_func, i );

#ifdef __linux__
        // Create a cpu_set_t object representing a set of CPUs. Clear it and mark
        // only CPU i as set.
        cpu_set_t cpuset;
        CPU_ZERO(&cpuset);
        CPU_SET(i+cpu_offset, &cpuset);
        int rc = pthread_setaffinity_np(threads[i].native_handle(),
                                        sizeof(cpu_set_t), &cpuset);
        if (rc != 0) {
            cerr << "Error calling pthread_setaffinity_np: " << rc << "\n";
        }
#endif

    }

    for (auto& t : threads) {
		t.join();
    }

	monitor->after();
    cout << total_flushed << "\t";
	monitor->diff();
    return 0;
}
