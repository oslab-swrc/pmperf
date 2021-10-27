## SPDX-FileCopyrightText: Copyright (c) 2021 Electronics and Telecommunications Research Institute
## SPDX-License-Identifier: MIT
## 
## Author : Youngjoo Woo <my.cat.liang@gmail.com>

import os
import subprocess
import time
import signal

def get_spare_percentage():
    ndctl_cmd = ["ndctl", "list", "-d1", "-H", "-M"]
    ndctl_out = subprocess.check_output(ndctl_cmd, shell=False).decode()
    ndctl_str = ndctl_out.split('\n')
    percentage = 0
    for line in ndctl_str:
        if "spares_percentage" in line:
            percentage = int(line.split(':')[1].split(',')[0])
    return percentage

def get_pmperf():
    ipmctl_cmd = ["ipmctl", "show", "-dimm", "0x1001", "-performance"]
    ipmctl_out = subprocess.check_output(ipmctl_cmd, shell=False).decode()
    return ipmctl_out

running = True

def signal_handler(signum, frame):
    global running
    print("You pressed Ctrl+C!")
    running = False
    print("Waiting to finish...")

def main_function():
    global running

    signal.signal(signal.SIGINT, signal_handler)

    datetime = time.strftime('%Y%m%d_%H%M')
    outfile = "pmkiller_%s.out" %(datetime)

    print("Log file : " + outfile)
    killer_cmd = ["./pmkiller.x"]

    while(running):
        killer_out = subprocess.check_output(killer_cmd, shell=False)
        spare = get_spare_percentage()

        # Save log strings
        f = open(outfile, 'a')
        f.write("%d\t%s\n" % (spare,killer_out.decode()))
        f.write (get_pmperf())
        f.close()

    print("Finished!!")


if __name__ == '__main__':
    main_function()