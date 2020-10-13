#include <unistd.h>
#include "pmperf.h"

int main (int argc, char ** argv){
    PmPerf * monitor = new PmPerf();
    monitor->pmm_program();
    monitor->before();
    sleep(10);
    monitor->after();
    monitor->diff();
    delete monitor;
    return 0;
}