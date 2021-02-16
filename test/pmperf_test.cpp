#include <stdlib.h>

#include <unistd.h>
#include <fstream>
#include <iostream>

#include "pmperf.h"

int main (int argc, char ** argv){
   PmPerf * monitor = new PmPerf();
   monitor->pmm_program();
   monitor->before();
   sleep(5);
   monitor->after();
   monitor->export_diff("test.pmperf");
   delete monitor;
}
