## SPDX-FileCopyrightText: Copyright (c) 2021 Electronics and Telecommunications Research Institute
## SPDX-License-Identifier: MIT
## 
## Author : Youngjoo Woo <my.cat.liang@gmail.com>

class PMMCounter:
    def __init__(self, line=None):
        if not line:
            self.media_read = 0
            self.media_write = 0
            self.media_rreq = 0
            self.media_wreq = 0
            self.read_amp = 0.0
            self.write_amp = 0.0
            return

        values = line.split()
        self.id = int(values[0])
        self.socket = int(values[1])
        self.controller = int(values[2])
        self.channel = int(values[3])
        self.media_read = int(values[4])
        self.media_write = int(values[5])
        self.media_rreq = int(values[6])
        self.media_wreq = int(values[7])
        
        if (self.media_rreq > 0):
            self.read_amp = float(self.media_read)/self.media_rreq
        if (self.media_wreq > 0):
            self.write_amp = float(self.media_write)/self.media_wreq
    
    @staticmethod
    def header_str():
        rt_str = ""
        rt_str += "ReadRequests\t" 
        rt_str += "MediaReads\t" 
        rt_str += "WriteRequests\t" 
        rt_str += "MediaWrites\t"
        rt_str += "ReadAmplification\t"
        rt_str += "WriteAmplification\t"
    
        return rt_str

    def __str__(self):
        rt_str = ""

        rt_str += str(self.media_rreq) + '\t'
        rt_str += str(self.media_read) + '\t'
        rt_str += str(self.media_wreq) + '\t'
        rt_str += str(self.media_write) + '\t'
        rt_str += str(self.read_amp) + '\t'
        rt_str += str(self.write_amp) + '\t'

        return rt_str
    
    def __add__ (self, other):
        self.media_read += other.media_read
        self.media_write += other.media_write
        self.media_rreq += other.media_rreq
        self.media_wreq += other.media_wreq

        if (self.media_rreq > 0):
            self.read_amp = float(self.media_read)/self.media_rreq
        if (self.media_wreq > 0):
            self.write_amp = float(self.media_write)/self.media_wreq

    def __div__(self, divisor):
        self.media_read /= divisor
        self.media_write /= divisor
        self.media_rreq /= divisor
        self.media_wreq /= divisor

class CoreCounter:
    def __init__(self):
        self.num_counter = 16
        self.core_id = -1
        self.used = False

    def build(self, lines):
        #self.lines = lines
        for line in lines:
            if ':::' in line:
                self.core_id = int(line.split()[2])
            elif 'UsedCore' in line:
                self.used = (int(line.split()[1]) == 1)
            elif 'InvariantTSC' in line:
                self.tsc = int(line.split()[1])
            elif 'Cycles' in line and 'RefCycles' not in line:
                self.cycles = int(line.split()[1])
            elif 'RefCycles' in line:
                self.ref_cycle = int(line.split()[1])	
            elif 'InstructionsRetired' in line:
                self.inst_retired = int(line.split()[1])
            elif 'IPC' in line:
                self.ipc = float(line.split()[1])
            elif 'ExecUsage' in line:
                self.exec_usage = float(line.split()[1])
            elif 'ActiveAverageFrequency' in line:
                self.active_avg_freq = float(line.split()[1])
            elif 'ActiveRelativeFrequency' in line:
                self.active_rel_freq = float(line.split()[1])
            elif 'L2CacheHitRatio' in line:
                self.l2hit_ratio = float(line.split()[1])
            elif 'L2CacheHits' in line:
                self.l2hit = int(line.split()[1])
            elif 'L2CacheMisses' in line:
                self.l2miss = int(line.split()[1])
            elif 'L3CacheHitRatio' in line:
                self.l3hit_ratio = float(line.split()[1])
            elif 'L3CacheHits' in line:
                self.l3hit = int(line.split()[1])
            elif 'L3CacheMisses' in line:
                self.l3miss = int(line.split()[1])
    
    def __str__ (self):

        rt_str = ""
        rt_str += str(self.core_id) +'\t'
        rt_str += str(self.used) + '\t'
        rt_str += str(self.tsc) + '\t'
        rt_str += str(self.cycles) + '\t'
        rt_str += str(self.ref_cycle) + '\t'	
        rt_str += str(self.inst_retired) + '\t'
        rt_str += str(self.ipc) + '\t'
        rt_str += str(self.exec_usage) + '\t'
        rt_str += str(self.active_avg_freq) + '\t'
        rt_str += str(self.active_rel_freq) + '\t'
        rt_str += str(self.l2hit_ratio) + '\t'
        rt_str += str(self.l2hit) + '\t'
        rt_str += str(self.l2miss) + '\t'
        rt_str += str(self.l3hit_ratio) + '\t'
        rt_str += str(self.l3hit) + '\t'
        rt_str += str(self.l3miss) + '\t'
        
        return rt_str

class SocketConter:
    def __init__(self,id = -1):
        self.socket_id = id
        self.num_counter = 21

        self.tsc = 0.0
        self.cycles = 0.0
        self.ref_cycle = 0.0
        self.inst_retired = 0.0
        self.ipc = 0.0
        self.exec_usage = 0.0
        self.active_avg_freq = 0.0
        self.active_rel_freq = 0.0
        self.l2hit_ratio = 0.0
        self.l2hit = 0.0
        self.l2miss = 0.0
        self.l3hit_ratio = 0.0
        self.l3hit = 0.0
        self.l3miss = 0.0
        self.rpq_ins = 0.0
        self.rpq_lat = 0.0
        self.wpq_ins = 0.0
        self.wpq_lat = 0.0
        self.rpq_occ = 0.0
        self.wpq_occ = 0.0

        self.pmm_total = PMMCounter()

    def add_pmm(self, pmm: PMMCounter):
        self.pmm_counters.append(pmm)
        self.pmm_total.__add__(pmm)

    def add_core(self, counter):
        self.core_counters[counter.core_id] = counter

        if (counter.used):
            self.used_cores.append(counter.core_id)

    def build(self, lines):
        self.used_cores = []
        self.core_counters = {}    
        self.pmm_counters = []

        for line in lines:
            if 'Socket' in line:
                self.socket_id = int(line.split()[2])
            elif 'InvariantTSC' in line:
                self.tsc = int(line.split()[1])
            elif 'Cycles' in line and 'RefCycles' not in line:
                self.cycles = int(line.split()[1])
            elif 'RefCycles' in line:
                self.ref_cycle = int(line.split()[1])	
            elif 'InstructionsRetired' in line:
                self.inst_retired = int(line.split()[1])
            elif 'IPC' in line:
                self.ipc = float(line.split()[1])
            elif 'ExecUsage' in line:
                self.exec_usage = float(line.split()[1])
            elif 'ActiveAverageFrequency' in line:
                self.active_avg_freq = float(line.split()[1])
            elif 'ActiveRelativeFrequency' in line:
                self.active_rel_freq = float(line.split()[1])
            elif 'L2CacheHitRatio' in line:
                self.l2hit_ratio = float(line.split()[1])
            elif 'L2CacheHits' in line:
                self.l2hit = int(line.split()[1])
            elif 'L2CacheMisses' in line:
                self.l2miss = int(line.split()[1])
            elif 'L3CacheHitRatio' in line:
                self.l3hit_ratio = float(line.split()[1])
            elif 'L3CacheHits' in line:
                self.l3hit = int(line.split()[1])
            elif 'L3CacheMisses' in line:
                self.l3miss = int(line.split()[1])
            elif 'RPQInsert' in line:
                self.rpq_ins = int(line.split()[1])
            elif 'RPQOccupancy' in line:
                self.rpq_occ = int(line.split()[1])
            elif 'WPQInsert' in line:
                self.wpq_ins = int(line.split()[1])
            elif 'WPQOccupancy' in line:
                self.wpq_occ = int(line.split()[1])
        
        if self.rpq_ins > 0:
            self.rpq_lat = float(self.rpq_occ)/self.rpq_ins
        else:
            self.rpq_lat = 0
            
        if self.wpq_ins > 0:
            self.wpq_lat = float(self.wpq_occ)/self.wpq_ins
        else:
            self.wpq_ins = 0

    def __add__ (self, other):
        if self.socket_id != other.socket_id:
            return
        
        self.cycles += other.cycles
        self.tsc += other.tsc
        self.ref_cycle += other.ref_cycle
        self.inst_retired += other.inst_retired
        self.ipc += other.ipc
        self.exec_usage += other.exec_usage
        self.active_avg_freq += other.active_avg_freq
        self.active_rel_freq += other.active_rel_freq
        self.l2hit_ratio += other.l2hit_ratio
        self.l2miss += other.l2miss
        self.l2hit += other.l2hit
        self.l3hit_ratio += other.l3hit_ratio
        self.l3miss += other.l3miss
        self.l3hit += other.l3hit
        self.rpq_ins += other.rpq_ins
        self.rpq_lat += other.rpq_lat
        self.wpq_ins += other.wpq_ins
        self.wpq_lat += other.wpq_lat
        self.rpq_occ += other.rpq_occ
        self.wpq_occ += other.wpq_occ

        self.pmm_total.__add__(other.pmm_total)
    
    def __div__ (self, divisor):
        self.cycles /= divisor
        self.tsc /= divisor
        self.ref_cycle /= divisor
        self.inst_retired /= divisor
        self.ipc /= divisor
        self.exec_usage /= divisor
        self.active_avg_freq /= divisor
        self.active_rel_freq /= divisor
        self.l2hit_ratio /= divisor
        self.l2miss /= divisor
        self.l2hit /= divisor
        self.l3hit_ratio /= divisor
        self.l3miss /= divisor
        self.l3hit /= divisor
        self.rpq_ins /= divisor
        self.rpq_lat /= divisor
        self.wpq_ins /= divisor
        self.wpq_lat /= divisor
        self.rpq_occ /= divisor
        self.wpq_occ /= divisor

        self.pmm_total.__div__(divisor)

    @staticmethod
    def header_str():
        rt_str = ""
        rt_str += 'SocketId\t'

        rt_str += 'InvariantTSC\t'
        rt_str += 'Cycles\t'
        rt_str += 'RefCycles\t'
        rt_str += 'InstructionsRetired\t'
        rt_str += 'IPC\t'
        rt_str += 'ExecUsage\t'
        rt_str += 'ActiveAverageFrequency\t'
        rt_str += 'ActiveRelativeFrequency\t'

        rt_str += 'L2CacheHitRatio\t'
        rt_str += 'L2CacheHits\t' 
        rt_str += 'L2CacheMisses\t'
        rt_str += 'L3CacheHitRatio\t'
        rt_str += 'L3CacheHits\t'
        rt_str += 'L3CacheMisses\t'
        
        rt_str += 'RPQInsert\t'
        rt_str += 'RPQOccupancy\t'
        rt_str += 'RPQLatency\t'
        rt_str += 'WPQInsert\t' 
        rt_str += 'WPQOccupancy\t'
        rt_str += 'WPQLatency\t'

        rt_str += PMMCounter.header_str()

        return rt_str
        
    def __str__ (self):
        rt_str = ""
        rt_str += str(self.socket_id) + '\t'
        rt_str += str(self.tsc) + '\t'
        rt_str += str(self.cycles) + '\t'
        rt_str += str(self.ref_cycle) + '\t'	
        rt_str += str(self.inst_retired) + '\t'
        rt_str += str(self.ipc) + '\t'
        rt_str += str(self.exec_usage) + '\t'
        rt_str += str(self.active_avg_freq) + '\t'
        rt_str += str(self.active_rel_freq) + '\t'
        rt_str += str(self.l2hit_ratio) + '\t'
        rt_str += str(self.l2hit) + '\t'
        rt_str += str(self.l2miss) + '\t'
        rt_str += str(self.l3hit_ratio) + '\t'
        rt_str += str(self.l3hit) + '\t'
        rt_str += str(self.l3miss) + '\t'

        rt_str += str(self.rpq_ins) + '\t'
        rt_str += str(self.rpq_occ) + '\t'
        rt_str += str(self.rpq_lat) + '\t'
        rt_str += str(self.wpq_ins) + '\t'
        rt_str += str(self.wpq_occ) + '\t'
        rt_str += str(self.wpq_lat) + '\t'
        
        rt_str += self.pmm_total.__str__()
        
        return rt_str