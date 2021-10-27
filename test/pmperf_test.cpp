// SPDX-FileCopyrightText: Copyright (c) 2021 Electronics and Telecommunications Research Institute
// SPDX-License-Identifier: MIT
// 
// Author : Youngjoo Woo <my.cat.liang@gmail.com>

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
