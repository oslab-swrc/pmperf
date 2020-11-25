TARGET = libpmperf.a
INSTALL_PATH = libs
OBJS = libpmperf.o

CLEANEXTS = o a

PCM_PATH = ../pcm
export PCM_PATH
INC_PATH = -I$(PCM_PATH)
INC_PATH += -Iinclude

LIB_DIRS = -L$(PCM_PATH)
LIB_DIRS += -Llibs
LIB= -lpmperf -lPCM -lpthread -lrt

CXXFLAGS += -std=c++11 -Wall -g -O3 -mmmx -msse2 #-mavx512f 
CXXFLAGS += $(INC_PATH)

SUBDIRS = test pmkiller
SUBDIRSCLEAN=$(addsuffix clean,$(SUBDIRS))

.SUFFIXES : .c .o

.PHONY: all subdirs $(SUBDIRS)
all: $(SUBDIRS) $(INSTALL_PATH) 

$(TARGET): $(OBJS) 
	ar rcs $@ $^

subdirs: $(SUBDIRS)

$(SUBDIRS): libs/libpmperf.a
	$(MAKE) -C $@

$(INSTALL_PATH)/libpmperf.a: $(INSTALL_PATH)

$(INSTALL_PATH): $(TARGET)
	mkdir -p $(INSTALL_PATH)
	cp -p $(TARGET) $(INSTALL_PATH)

.PHONY: clean distclean subdirsclean $(SUBDIRSCLEAN)

clean: $(SUBDIRSCLEAN)
	for file in $(CLEANEXTS); do rm -f *.$$file; done

distclean: clean
	rm -rf $(INSTALL_PATH)

%clean:
	$(MAKE) -C $(SUBDIRS) clean
