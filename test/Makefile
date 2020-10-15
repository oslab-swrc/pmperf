TARGET = pmperf_test
OBJS = pmperf_test.o
CLEANEXTS = o 

PCM_PATH_LOCAL = ../$(PCM_PATH)
INC_PATH = -I$(PCM_PATH_LOCAL)
INC_PATH += -I../include

LIB_DIRS = -L$(PCM_PATH_LOCAL)
LIB_DIRS += -L../libs
LIB= -lpmperf -lPCM -pthread -lrt

CXXFLAGS += -Wall -g -O3 -mmmx -msse2 -mavx512f -lpthread
CXXFLAGS += $(INC_PATH)

.SUFFIXES : .c .o

.PHONY: all
all: pmperf_test

$(TARGET): $(OBJS)
	$(CXX) -o $@ $^ $(LIB_DIRS) $(LIB) 

.PHONY: clean
clean:
	for file in $(CLEANEXTS); do rm -f *.$$file; done
	rm -f $(TARGET)
