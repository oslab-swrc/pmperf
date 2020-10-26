import sys
import os

class PMMCounter:
    def __init__(self, before=None, after=None, id=-1):

        if before is None and after is None:
            self.media_read = 0
            self.media_write = 0
            self.media_rreq = 0  
            self.media_wreq = 0
            self.read_amp = 0
            self.write_amp = 0
            self.dimmid = id
            
        else: 
            self.diff(before, after)

    
    def diff (self, before, after):
        if before.dimmid != after.dimmid:
            raise ValueError
        self.dimmid = before.dimmid
        self.media_read = after.media_read - before.media_read
        self.media_write = after.media_write - before.media_write
        self.media_rreq = after.media_rreq - before.media_rreq    
        self.media_wreq = after.media_wreq - before.media_wreq

        if self.media_rreq is not 0:
            self.read_amp = float(self.media_read)/self.media_rreq
        else:
            self.read_amp = 0
        if self.media_rreq is not 0:
            self.write_amp = float(self.media_write)/self.media_wreq
        else:
            self.write_amp = 0
        
        return 

    def __str__(self):
        rt_str = ""
        rt_str += "DimmID\t" + str(self.dimmid) + '\n'
        rt_str += "ReadRequests\t" + str(self.media_rreq) + '\n'
        rt_str += "MediaReads\t" + str(self.media_read) + '\n'
        rt_str += "WriteRequests\t" + str(self.media_wreq) + '\n'
        rt_str += "MediaWrites\t" + str(self.media_write) + '\n'
        rt_str += "ReadAmplification\t" + str(self.write_amp) + '\n'
        rt_str += "WriteAmplification\t" + str(self.write_amp) + '\n'

        return rt_str

class CoreCounters:
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
        rt_str += str(self.l3miss) + '\n'

        
        return rt_str

class SocketConter:
    def __init__(self):
        self.num_counter = 21
        self.used_cores = []
        self.core_counters = {}    
    
    def add_pmm(self, pmm):
        self.pmm_counter = pmm

    def add_core(self, counter):
        self.core_counters[counter.core_id] = counter

        if (counter.used):
            self.used_cores.append(counter.core_id)

    def build(self, lines):
        self.lines = lines
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

    def __str__ (self):
        rt_str = ""
        try:
            rt_str += 'RPQInsert\t' + str(self.rpq_ins) + '\n'
            rt_str += 'RPQOccupancy\t' + str(self.rpq_occ) + '\n'
            rt_str += 'RPQLatency\t' + str(self.rpq_lat) + '\n'
            rt_str += 'WPQInsert\t' + str(self.wpq_ins) + '\n'
            rt_str += 'WPQOccupancy\t' + str(self.wpq_occ) + '\n'
            rt_str += 'WPQLatency\t' + str(self.wpq_lat) + '\n'
        except AttributeError:
            print(self.lines)
        
        rt_str += self.pmm_counter.__str__()
        
        rt_str += 'CoreId\t'
        rt_str += 'UsedCore\t'
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
        rt_str += 'L3CacheMisses\n'

        rt_str += 'Socket\t'
        rt_str += 'True\t'
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
        rt_str += str(self.l3miss) + '\n'

        for id in self.used_cores:
            rt_str += self.core_counters[id].__str__ ()
        
        return rt_str

class Summary:
    def __init__(self, fpath):
        self.filepath = fpath
        self.basepath = os.path.splitext(fpath)
        
        basename = os.path.basename(os.path.splitext(fpath)[0])
        settings = basename.split('_')

        # (algorithm, workload, num_threads)
        self.algorithm = settings[0]
        self.workload = settings[1]
        self.num_threads = settings[2]

    def build(self):
        pmm_before = []
        pmm_after = []

        with open(self.filepath , 'r') as f:
            self.lines = f.readlines()

        dimmid = -1
        offset = -1
        for (idx,line) in enumerate(self.lines):
            if '::' in line:
                offset = idx
                break
            elif 'Before PMM' in line:
                counter = pmm_before
            elif 'After PMM' in line:
                counter = pmm_after
            elif 'DimmID' in line:
                dimmid = int(line.strip().strip('-').split('=')[1],base=16)>>12
                counter.append(PMMCounter(id=dimmid))
            elif 'TotalMediaReads' in line:
                counter[dimmid].media_read = int(line.strip().split('=')[1],base=16)
            elif 'TotalMediaWrites' in line:
                counter[dimmid].media_write = int(line.strip().split('=')[1],base=16)
            elif 'TotalReadRequests' in line:
                counter[dimmid].media_rreq = int(line.strip().split('=')[1],base=16)
            elif 'TotalWriteRequests' in line:
                counter[dimmid].media_wreq = int(line.strip().split('=')[1],base=16)
        
        self.sockets = {}
   
        socket_id = -1
        while True:
            if '::' in self.lines[offset]:
                if ':::' in self.lines[offset]:
                    counter = CoreCounters()
                    counter.build(self.lines[offset:offset+counter.num_counter])
                    self.sockets[socket_id].add_core(counter)
                else:
                    counter = SocketConter()
                    counter.build(self.lines[offset:offset+counter.num_counter])
                    socket_id = counter.socket_id

                    self.sockets[socket_id] = counter
                offset += counter.num_counter
            else:
                offset += 1

            if offset >= len(self.lines):
                break

        for (a,b) in zip(pmm_after, pmm_before):
            diff = PMMCounter(b, a)
            if diff.dimmid not in self.sockets.keys():
                self.sockets[diff.dimmid] = SocketConter()
            self.sockets[diff.dimmid].add_pmm(diff)


    def export(self, name):
        self.build()
        
        f = open(self.basepath[0] + '_' + name +'.summary', 'w')

        #database name
        f.write(name + '\n')

        for socket in self.sockets.values():
            if len(socket.used_cores) > 0:
                f.write(socket.__str__())

        f.close()


    def key(self):
        return (self.algorithm, self.workload, self.num_threads)


if __name__ == '__main__':
    Summary(sys.argv[1])