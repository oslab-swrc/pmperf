import sys
import os

from .counters import SocketConter, CoreCounter, PMMCounter

class Summary:
    def __init__(self, fpath=None):

        if(fpath):
            self.filepath = fpath
            self.basepath = os.path.splitext(fpath)
            
            basename = os.path.basename(os.path.splitext(fpath)[0])
            settings = basename.split('_')

            # (algorithm, workload, num_threads)
            self.algorithm = settings[0]
            self.workload = settings[1]
            self.num_threads = int(settings[2][1:])
        
            self.build()
        else:
            self.sockets = {}

    def build(self):
        with open(self.filepath , 'r') as f:
            self.lines = f.readlines()
        offset = -1
        self.envs = {}
        header = 0
        for (idx,line) in enumerate(self.lines):
            if len(line) <= 1:
                continue
            elif ': Host' in line:
                continue
            elif 'PMem' in line:
                offset = idx
                break
            else:
                toks = line.split()
                if toks[0] == 'name:':
                    self.envs['name'] = str(toks[1])
                elif toks[0] == 'os_name:':
                    self.envs['os_name'] = str(toks[1])
                elif toks[0] == 'os_version:':
                    self.envs['os_version'] = str(toks[1])
                elif toks[0] == 'os_type:':
                    self.envs['os_type'] = int(toks[1])
                elif toks[0] == 'mixed_sku:':
                    self.envs['mixed_sku'] = bool(toks[1])
                elif toks[0] == 'sku':
                    self.envs['sku_violation'] = bool(toks[2])
                else:
                    self.envs[toks[0]] = toks[1]
        
        pmm_counters = []
        offset += 1
        header = 0
        for (idx,line) in enumerate(self.lines[offset:]):
            if len(line) <= 1:
                continue
            elif ':' in line or '#' in line:
                header += 1
                if header > 1:
                    offset += idx-1
                    break
            else:
                counter = PMMCounter(line)
                pmm_counters.append(counter)

        self.sockets = {}
   
        socket_id = -1
        while True:
            if '::' in self.lines[offset]:
                if ':::' in self.lines[offset]:
                    counter = CoreCounter()
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
        for counter in pmm_counters:
            self.sockets[counter.socket].add_pmm(counter)


    def export(self, name):
        self.build()
        
        f = open(self.basepath[0] + '_' + name +'.summary', 'w')

        #database name
        f.write(name + '\n')

        for socket in self.sockets.values():
            if len(socket.used_cores) > 0:
                f.write(socket.__str__())

        f.close()

    def print_out(self):
        for k,v in self.envs.items():
            print(k+'\t', end='')
            print(v)
        for socket in self.sockets.values():
            if len(socket.used_cores) > 0:
                print(socket)

    def key(self):
        return (self.algorithm, self.workload, self.num_threads)

    def __add__(self, other):
        for socket_id, o_socket in other.sockets.items():
            if socket_id not in self.sockets:
                self.sockets[socket_id] = SocketConter(socket_id)
            self.sockets[socket_id].__add__(o_socket)

    def __div__(self, divisor):
        for socket in self.sockets.values():
            socket.__div__(divisor)
        
    def __str__(self):
        rt_str = ''
        for v in self.sockets.values():
            rt_str += v.__str__() 
        return rt_str + '\n'

if __name__ == '__main__':
    result = Summary(sys.argv[1])
    result.print_out()