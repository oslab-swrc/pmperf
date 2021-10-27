## SPDX-FileCopyrightText: Copyright (c) 2021 Electronics and Telecommunications Research Institute
## SPDX-License-Identifier: MIT
## 
## Author : Youngjoo Woo <my.cat.liang@gmail.com>


TARGET = $(INSTALL_PATH)/libpmperf.a
OBJS = libpmperf.o

CLEANEXTS = o a

INC_PATH = -I$(PCM_PATH)
INC_PATH += -I../include

LIB_DIRS = -L$(PCM_PATH)
LIB_DIRS += -L$(INSTALL_PATH)
LIB= -lpmperf -lPCM -lpthread -lrt -lipmctl

CXXFLAGS += -std=c++11 -Wall -g -O3 -mmmx -msse2 #-mavx512f 
CXXFLAGS += $(INC_PATH)

.SUFFIXES : .c .o

.PHONY: all

all: $(TARGET)

$(TARGET): $(OBJS) $(INSTALL_PATH)
	ar rcs $@ $(OBJS)


$(INSTALL_PATH):
	mkdir -p $(INSTALL_PATH)

.PHONY: clean

clean:
	for file in $(CLEANEXTS); do rm -f *.$$file; done

