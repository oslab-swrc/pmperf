TARGET = libpmperf.a
INSTALL_PATH = libs
OBJS = libpmperf.o

CLEANEXTS = o a

PCM_PATH = ../pcm
INC_PATH = -I$(PCM_PATH)
INC_PATH += -Iinclude

LIB_DIRS = -L$(PCM_PATH)
LIB_DIRS += -Llibs
LIB= -lpmperf -lPCM -pthread -lrt

CXXFLAGS += -Wall -g -O3 -mmmx -msse2 -mavx512f -lpthread
CXXFLAGS += $(INC_PATH)

.SUFFIXES : .c .o

.PHONY: all
all: install pmperf_test

$(TARGET): $(OBJS) 
	ar rcs $@ $^

pmperf_test: pmperf_test.o
	$(CXX) -o $@ $^ $(LIB_DIRS) $(LIB) 

.PHONY: install
install: $(TARGET)
	mkdir -p $(INSTALL_PATH)
	cp -p $(TARGET) $(INSTALL_PATH)

.PHONY: clean
clean:
	for file in $(CLEANEXTS); do rm -f *.$$file; done
	rm -rf $(INSTALL_PATH)
	rm -f pmperf_test 
