#include <string>
#include <bitset>
#include <fstream>
#include <iostream>

#include "pmperf.h"

const uint32 max_sockets = 256;
const uint32 max_imc_channels = 6;
const uint32 max_imc_controllers = 2;



void CoreResult::print(std::ostream & s)
{
    s << "UsedCore\t" << used << std::endl;
    
    //core
    s << "InvariantTSC\t" << tsc << std::endl; 
    s << "Cycles\t" << cycles << std::endl; 
    s << "RefCycles\t" << ref_cycles << std::endl;   
    s << "InstructionsRetired\t" << inst_retired << std::endl;
    s << "IPC\t" << ipc << std::endl; 
    s << "ExecUsage\t" << core_usage << std::endl;   
    s << "ActiveAverageFrequency\t" << avg_freq << std::endl; 
    s << "ActiveRelativeFrequency\t" << relative_freq << std::endl;
    //cache
    s << "L2CacheHitRatio\t" << l2hitratio << std::endl; 
    s << "L2CacheHits\t" << l2hits << std::endl;   
    s << "L2CacheMisses\t" << l2misses << std::endl;
    s << "L3CacheHitRatio\t" << l3hitratio << std::endl; 
    s << "L3CacheHits\t" << l3hits << std::endl;   
    s << "L3CacheMisses\t" << l3misses << std::endl;
}


void SocketResult::print(std::ostream & s)
{
    //core
    s << "InvariantTSC\t" << tsc << std::endl; 
    s << "Cycles\t" << cycles << std::endl; 
    s << "RefCycles\t" << ref_cycles << std::endl;   
    s << "InstructionsRetired\t" << inst_retired << std::endl;
    s << "IPC\t" << ipc << std::endl; 
    s << "ExecUsage\t" << core_usage << std::endl;   
    s << "ActiveAverageFrequency\t" << avg_freq << std::endl; 
    s << "ActiveRelativeFrequency\t" << relative_freq << std::endl;
    //cache
    s << "L2CacheHitRatio\t" << l2hitratio << std::endl; 
    s << "L2CacheHits\t" << l2hits << std::endl;   
    s << "L2CacheMisses\t" << l2misses << std::endl;
    s << "L3CacheHitRatio\t" << l3hitratio << std::endl; 
    s << "L3CacheHits\t" << l3hits << std::endl;   
    s << "L3CacheMisses\t" << l3misses << std::endl;
    
    //pmm
    s << "RPQInsert\t" << rinsert << std::endl;
    s << "RPQOccupancy\t" << roccupancy << std::endl;
    s << "ReadLatency\t" << rlatency << std::endl;
    s << "WPQInsert\t" << winsert << std::endl;
    s << "WPQOccupancy\t" << woccupancy << std::endl;
    s << "WriteLatency\t" << wlatency << std::endl;

}


PmState::PmState()
{
    pcm::PCM * m = pcm::PCM::getInstance();

    uncore_counter = new pcm::ServerUncoreCounterState[m->getNumSockets()];

}

void PmState::CollectState(pcm::PCM * m)
{
    for (unsigned int i=0; i<m->getNumSockets(); i++)
    {
        uncore_counter[i] = m->getServerUncoreCounterState(i);
    }
    
    m->getAllCounterStates(system_counter, socket_counter, core_counter);
}

double PmState::getRpqIns(pcm::PCM *m, PmState *before, PmState* after, int socket){
    double res = 0;
    for (size_t channel = 0; channel < m->getMCChannelsPerSocket(); ++channel)
    {
        res += (double)pcm::getMCCounter((uint32)channel, RPQ_INS, 
        before->uncore_counter[socket], after->uncore_counter[socket]);
    }
    return res;
}

double PmState::getRpqOcc(pcm::PCM *m, PmState *before, PmState* after, int socket){
    double res = 0;
    for (size_t channel = 0; channel < m->getMCChannelsPerSocket(); ++channel)
    {
        res += (double)pcm::getMCCounter((uint32)channel, RPQ_OCC, 
        before->uncore_counter[socket], after->uncore_counter[socket]);
    }
    return res;
}

double PmState::getWpqIns(pcm::PCM *m, PmState *before, PmState* after, int socket){
    double res = 0;
    for (size_t channel = 0; channel < m->getMCChannelsPerSocket(); ++channel)
    {
        res += (double)pcm::getMCCounter((uint32)channel, WPQ_INS, 
        before->uncore_counter[socket], after->uncore_counter[socket]);
    }
    return res;
}

double PmState::getWpqOcc(pcm::PCM *m, PmState *before, PmState* after, int socket){
    double res = 0;
    for (size_t channel = 0; channel < m->getMCChannelsPerSocket(); ++channel)
    {
        res += (double)pcm::getMCCounter((uint32)channel, WPQ_OCC, 
        before->uncore_counter[socket], after->uncore_counter[socket]);
    }
    return res;
}

void PmState::getCoreResult(pcm::PCM * m, CoreResult * res, PmState * before, PmState * after, int core)
{
    //core
    res->tsc = pcm::getInvariantTSC(before->core_counter[core], after->core_counter[core]);
    res->cycles = pcm::getCycles(before->core_counter[core], after->core_counter[core]);
    res->ref_cycles = pcm::getRefCycles(before->core_counter[core], after->core_counter[core]);
    res->inst_retired = pcm::getInstructionsRetired(before->core_counter[core], after->core_counter[core]);

    res->ipc = pcm::getIPC(before->core_counter[core], after->core_counter[core]);
    res->core_usage = pcm::getExecUsage(before->core_counter[core], after->core_counter[core]);
    res->avg_freq = pcm::getActiveAverageFrequency(before->core_counter[core], after->core_counter[core]);
    res->relative_freq = pcm::getActiveRelativeFrequency(before->core_counter[core], after->core_counter[core]);

    //L2, L3 cache
    res->l2hitratio = pcm::getL2CacheHitRatio(before->core_counter[core], after->core_counter[core]);
    res->l2hits = pcm::getL2CacheHits(before->core_counter[core], after->core_counter[core]);
    res->l2misses = pcm::getL2CacheMisses(before->core_counter[core], after->core_counter[core]);
    res->l3hitratio = pcm::getL3CacheHitRatio(before->core_counter[core], after->core_counter[core]);
    res->l3hits = pcm::getL3CacheHits(before->core_counter[core], after->core_counter[core]);
    res->l3misses = pcm::getL3CacheMisses(before->core_counter[core], after->core_counter[core]);
}


void PmState::getSocketResult(pcm::PCM * m, SocketResult * res, PmState * before, PmState * after, int socket)
{
    //core
    res->tsc = pcm::getInvariantTSC(before->socket_counter[socket], after->socket_counter[socket]);
    res->cycles = pcm::getCycles(before->socket_counter[socket], after->socket_counter[socket]);
    res->ref_cycles = pcm::getRefCycles(before->socket_counter[socket], after->socket_counter[socket]);
    res->inst_retired = pcm::getInstructionsRetired(before->socket_counter[socket], after->socket_counter[socket]);

    res->ipc = pcm::getIPC(before->socket_counter[socket], after->socket_counter[socket]);
    res->core_usage = pcm::getExecUsage(before->socket_counter[socket], after->socket_counter[socket]);
    res->avg_freq = pcm::getActiveAverageFrequency(before->socket_counter[socket], after->socket_counter[socket]);
    res->relative_freq = pcm::getActiveRelativeFrequency(before->socket_counter[socket], after->socket_counter[socket]);

    //L2, L3 cache
    res->l2hitratio = pcm::getL2CacheHitRatio(before->socket_counter[socket], after->socket_counter[socket]);
    res->l2hits = pcm::getL2CacheHits(before->socket_counter[socket], after->socket_counter[socket]);
    res->l2misses = pcm::getL2CacheMisses(before->socket_counter[socket], after->socket_counter[socket]);
    res->l3hitratio = pcm::getL3CacheHitRatio(before->socket_counter[socket], after->socket_counter[socket]);
    res->l3hits = pcm::getL3CacheHits(before->socket_counter[socket], after->socket_counter[socket]);
    res->l3misses = pcm::getL3CacheMisses(before->socket_counter[socket], after->socket_counter[socket]);

    //uncore
    res->rinsert = getRpqIns(m, before, after, socket);
    res->roccupancy = getRpqOcc(m, before, after, socket);
    res->winsert = getWpqIns(m, before, after, socket);
    res->woccupancy = getWpqOcc(m, before, after, socket);

    if(res->rinsert==0.) 
        res->rlatency = 0;
    else 
        res->rlatency = res->roccupancy / res->rinsert;

    if(res->winsert==0.) 
        res->wlatency = 0;
    else 
        res->wlatency = res->woccupancy / res->winsert;
}



std::map<PmPerf::Event, uint32> PmPerf::event_codes = {
        { UNC_M_CLOCKTICKS,             MC_CH_PCI_PMON_CTL_EVENT(0x00)},
        { DRAM_RPQ_INSERTS,             MC_CH_PCI_PMON_CTL_EVENT(0x10)},
        { DRAM_RPQ_CYCLES_NE,           MC_CH_PCI_PMON_CTL_EVENT(0x11)},
        { DRAM_RPQ_CYCLES_FULL,         MC_CH_PCI_PMON_CTL_EVENT(0x12)},
        { DRAM_RPQ_OCCUPANCY,           MC_CH_PCI_PMON_CTL_EVENT(0x80)},
        { DRAM_WPQ_INSERTS,             MC_CH_PCI_PMON_CTL_EVENT(0x20)},
        { DRAM_WPQ_CYCLES_NE,           MC_CH_PCI_PMON_CTL_EVENT(0x21)},
        { DRAM_WPQ_CYCLES_FULL,         MC_CH_PCI_PMON_CTL_EVENT(0x22)},
        { DRAM_WPQ_OCCUPANCY,           MC_CH_PCI_PMON_CTL_EVENT(0x81)},
        { DRAM_WPQ_READ_HIT,            MC_CH_PCI_PMON_CTL_EVENT(0x23)},
        { DRAM_WPQ_WRITE_HIT,           MC_CH_PCI_PMON_CTL_EVENT(0x24)},
        { PMM_RPQ_INSERTS,              MC_CH_PCI_PMON_CTL_EVENT(0xe3)},
        { PMM_WPQ_INSERTS,              MC_CH_PCI_PMON_CTL_EVENT(0xe7)},
        { PMM_RPQ_OCCUPANCY_ALL,        MC_CH_PCI_PMON_CTL_EVENT(0xe0) + MC_CH_PCI_PMON_CTL_UMASK(1)},
        { PMM_WPQ_OCCUPANCY_ALL,        MC_CH_PCI_PMON_CTL_EVENT(0xe4) + MC_CH_PCI_PMON_CTL_UMASK(1)},
        { PMM_CMD_ALL,                  MC_CH_PCI_PMON_CTL_EVENT(0xea) + MC_CH_PCI_PMON_CTL_UMASK(1)},
        { PMM_CMD_RD,                   MC_CH_PCI_PMON_CTL_EVENT(0xea) + MC_CH_PCI_PMON_CTL_UMASK(2)},
        { PMM_CMD_WR,                   MC_CH_PCI_PMON_CTL_EVENT(0xea) + MC_CH_PCI_PMON_CTL_UMASK(4)},
        { PMM_CMD_UFILL_RD,             MC_CH_PCI_PMON_CTL_EVENT(0xea) + MC_CH_PCI_PMON_CTL_UMASK(8)},
};

PmPerf::PmPerf()
{
    m = pcm::PCM::getInstance();
    if(m->getNumSockets() > max_sockets)
    {
        std::cerr << "Only systems with up to "<<max_sockets<<" sockets are supported! Program aborted" << std::endl;
        exit(EXIT_FAILURE);
    }
	if (m->getNumCores() != m->getNumOnlineCores())
	{
		std::cerr << "Number of online cores should be equal to number of available cores\n";
		exit(EXIT_FAILURE);
	}

    m->resetPMU();

    before_state = new PmState;
    after_state = new PmState;
}

PmPerf::~PmPerf()
{
    m->cleanup();
}

pcm::PCM::ErrorCode PmPerf::pmm_program()
{
    pcm::PCM::ErrorCode status;
 
	//build PMU configuration
	status = m->program();
    switch (status)
    {
    case pcm::PCM::Success:
        break;
    case pcm::PCM::MSRAccessDenied:
        std::cerr << "Access to Processor Counter Monitor has denied (no MSR or PCI CFG space access)." << std::endl;
        exit(EXIT_FAILURE);
    case pcm::PCM::PMUBusy:
        std::cerr << "Access to Processor Counter Monitor has denied (Performance Monitoring Unit is occupied by other application). Try to stop the application that uses PMU." << std::endl;
        std::cerr << "Alternatively you can try running PCM with option -r to reset PMU configuration at your own risk." << std::endl;
        exit(EXIT_FAILURE);
    default:
        std::cerr << "Access to Processor Counter Monitor has denied (Unknown error)." << std::endl;
        exit(EXIT_FAILURE);
    }
    
/*
 *    Programm IMC counters
 *    0. MC_CH_PCI_PMON_CTL_EVENT(0xe0) + MC_CH_PCI_PMON_CTL_UMASK(1);  // PMM RDQ occupancy
 *    1. MC_CH_PCI_PMON_CTL_EVENT(0xe3) + MC_CH_PCI_PMON_CTL_UMASK(0);  // PMM RDQ Insert
 *    2. MC_CH_PCI_PMON_CTL_EVENT(0xe4) + MC_CH_PCI_PMON_CTL_UMASK(1);  // PMM WPQ Occupancy
 *    3. MC_CH_PCI_PMON_CTL_EVENT(0xe7) + MC_CH_PCI_PMON_CTL_UMASK(0);  // PMM WPQ Insert
 */
    status = m->programServerUncoreLatencyMetrics(true);

    return status;
}


void PmPerf::before()
{
    before_state->CollectState(m);
}

void PmPerf::after()
{
    after_state->CollectState(m);
}

void PmPerf::clear()
{
    used_core_map.reset();
    external.clear();
}

void PmPerf::used_core(int id)
{
    used_core_map.set(id);
}

void PmPerf::add_external(const char * k, double v)
{
    external[k] = v;
}
void PmPerf::add_external(const char *k , uint64 v)
{
    external[k] = (double) v;
}

void PmPerf::diff(std::ostream & os)
{
    SocketResult * res_socket = new SocketResult[m->getNumSockets()];
    CoreResult * res_core = new CoreResult[m->getNumCores()];

    for (uint32 i=0; i<m->getNumSockets(); i++)
    {
        SocketResult * s = &res_socket[i];
        PmState::getSocketResult(m, s, before_state, after_state, i);
    }

    for (uint32 j=0; j<m->getNumCores(); j++)
    {
        CoreResult * c = &res_core[j];
        if (used_core_map.test(j))
            c->used = true;
        PmState::getCoreResult(m, c, before_state, after_state, j);
    }

    for (uint32 i=0; i<m->getNumSockets(); i++)
    {
        SocketResult * s = &res_socket[i];
        os << ":: Socket " << i << std::endl;
        s->print(os);

        for (uint32 j=0; j<m->getNumCores(); j++)
        {
            CoreResult * c = &res_core[j];
            
            if( m->getSocketId(j) != (int32) i) continue;

            os << "::: Core " << j << std::endl;
            c->print(os);

        }
    }

    delete res_socket;
    
    return;
}

void PmPerf::export_diff(char * path) {

    std::ofstream outFile(path);

    for ( auto & kv : external)
    {
        outFile << kv.first << "\t" << kv.second << std::endl;
    }
     
    diff(outFile);
    
    outFile.close();
    
    return;

}