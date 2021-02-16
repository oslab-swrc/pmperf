INSTALL_PATH = libs
TARGET = $(INSTALL_PATH)/libpmperf.a
OBJS = libpmperf.o

CLEANEXTS = o a

PCM_PATH = ../pcm
export PCM_PATH
INC_PATH = -I$(PCM_PATH)
INC_PATH += -Iinclude

LIB_DIRS = -L$(PCM_PATH)
LIB_DIRS += -L$(INSTALL_PATH)
LIB= -lpmperf -lPCM -lpthread -lrt -lipmctl

CXXFLAGS += -std=c++11 -Wall -g -O3 -mmmx -msse2 #-mavx512f 
CXXFLAGS += $(INC_PATH)

SUBDIRS = $(filter-out include/ $(INSTALL_PATH)/ , $(wildcard */))

.SUFFIXES : .c .o

.PHONY: all subdirs $(SUBDIRS)

all: subdirs $(INSTALL_PATH) 

$(TARGET): $(OBJS) $(INSTALL_PATH)
	ar rcs $@ $(OBJS)

subdirs: $(SUBDIRS)

$(SUBDIRS): $(TARGET)
	$(MAKE) -C $@


$(INSTALL_PATH):
	mkdir -p $(INSTALL_PATH)

.PHONY: clean distclean

clean:
	for subdir in $(SUBDIRS); do $(MAKE) -C $$subdir clean; done
	for file in $(CLEANEXTS); do rm -f *.$$file; done

distclean: clean	
	rm -rf $(INSTALL_PATH)
