
TARGET = pmperf_test
OBJS = pmperf_test.o
CLEANEXTS = o 

INC_PATH = -I$(PCM_PATH)
INC_PATH += -I../include

LIB_DIRS = -L$(PCM_PATH)
LIB_DIRS += -L../libs
LIB= -lpmperf -lPCM -lpthread -lrt -lipmctl 

CXXFLAGS += -std=c++11 -Wall -g -O3 -mmmx -msse2 #-mavx512f
CXXFLAGS += $(INC_PATH)

.SUFFIXES : .c .o

.PHONY: all
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) -o $@ $^ $(LIB_DIRS) $(LIB) 

.PHONY: clean
clean:
	for file in $(CLEANEXTS); do rm -f *.$$file; done
	rm -f $(TARGET)
