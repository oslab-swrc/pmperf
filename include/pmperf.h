#ifndef PMPERF_H
#define PMPERF_H 1

#include <bitset>
#include "cpucounters.h"

typedef unsigned long long uint64;
typedef signed long long int64;
typedef unsigned int uint32;
typedef signed int int32;

#define RPQ_OCC 0
#define RPQ_INS 1
#define WPQ_OCC 2
#define WPQ_INS 3

class CoreResult
{
public:
    bool used;
    uint64 tsc, cycles, ref_cycles, inst_retired;
    double ipc, core_usage, avg_freq, relative_freq;
    double l2hitratio, l3hitratio;
    uint64 l2hits, l2misses, l3hits, l3misses;

    CoreResult() :
        used(false),
        tsc(0), cycles(0), ref_cycles(0), inst_retired(0),
        ipc(0), core_usage(0), avg_freq(0), relative_freq(0),
        l2hitratio(0.0), l3hitratio(0.0),
        l2hits(0), l2misses(0), l3hits(0), l3misses(0)
    {};

    void print(std::ostream &  stream = std::cout);
};

class SocketResult
{
public:
    uint64 tsc, cycles, ref_cycles, inst_retired;
    double ipc, core_usage, avg_freq, relative_freq;
    double l2hitratio, l3hitratio;
    uint64 l2hits, l2misses, l3hits, l3misses;
    uint64 rinsert, roccupancy, winsert, woccupancy;
    double rlatency, wlatency;

    SocketResult() :
        tsc(0), cycles(0), ref_cycles(0), inst_retired(0),
        ipc(0), core_usage(0), avg_freq(0), relative_freq(0),
        l2hitratio(0.0), l3hitratio(0.0),
        l2hits(0), l2misses(0), l3hits(0), l3misses(0),
        rinsert(0), roccupancy(0), winsert(0), woccupancy(0),
        rlatency(0), wlatency(0)
    {};

    void print(std::ostream & stream  = std::cout);
};

class PmState {
private:
    pcm::ServerUncoreCounterState * uncore_counter;
    pcm::SystemCounterState system_counter;
    std::vector<pcm::CoreCounterState> core_counter;
    std::vector<pcm::SocketCounterState> socket_counter;

public:
    PmState();
    void CollectState(pcm::PCM *m);

    static void getSocketResult(pcm::PCM * m, SocketResult * res, PmState * before, PmState * after, int socket);
    static void getCoreResult(pcm::PCM * m, CoreResult * res, PmState * before, PmState * after, int core);
private:
    static double getRpqIns(pcm::PCM *m, PmState *before, PmState* after, int socket);
    static double getRpqOcc(pcm::PCM *m, PmState *before, PmState* after, int socket);
    static double getWpqIns(pcm::PCM *m, PmState *before, PmState* after, int socket);
    static double getWpqOcc(pcm::PCM *m, PmState *before, PmState* after, int socket);

};

class PmPerf {
    enum Event
    {
        UNC_M_CLOCKTICKS,
        DRAM_RPQ_INSERTS,
        DRAM_RPQ_CYCLES_NE,
        DRAM_RPQ_CYCLES_FULL,
        DRAM_RPQ_OCCUPANCY,
        DRAM_WPQ_INSERTS,
        DRAM_WPQ_CYCLES_NE,
        DRAM_WPQ_CYCLES_FULL,
        DRAM_WPQ_OCCUPANCY,
        DRAM_WPQ_READ_HIT,
        DRAM_WPQ_WRITE_HIT,
        PMM_RPQ_INSERTS,
        PMM_WPQ_INSERTS,
        PMM_RPQ_OCCUPANCY_ALL,
        PMM_WPQ_OCCUPANCY_ALL,
        PMM_CMD_ALL,
        PMM_CMD_RD,
        PMM_CMD_WR,
        PMM_CMD_UFILL_RD,
        NUM_IMC_EVENT
    };

private:
    pcm::PCM * m;
    static std::map <Event,uint32> event_codes;

    PmState * before_state;
    PmState * after_state;

    std::map <std::string,double> external;
    std::bitset <256> used_core_map;

public:
    PmPerf();
    ~PmPerf();

    pcm::PCM::ErrorCode pmm_program();

    void before();
    void after();
    void diff(std::ostream & stream = std::cout);
    void export_diff(char * path);
    void clear();
    void used_core(int);
    void add_external(const char *, double);
    void add_external(const char *, uint64);

};

#endif
