## SPDX-FileCopyrightText: Copyright (c) 2021 Electronics and Telecommunications Research Institute
## SPDX-License-Identifier: MIT
## 
## Author : Youngjoo Woo <my.cat.liang@gmail.com>

PWD = $(shell pwd)
PCM_PATH = $(PWD)/../pcm
INSTALL_PATH = $(PWD)/libs
export PCM_PATH
export INSTALL_PATH

PMPERF_SRC = pmperf
LIB_TARGET = $(INSTALL_PATH)/libpmperf.a

APPS = test pmkiller

CLEANEXTS = o a

.PHONY: all $(LIBSRC) $(APPS)

all: $(PMPERF_SRC) $(APPS)

$(LIB_TARGET): 
	$(MAKE) -C $(PMPERF_SRC)

$(APPS): $(LIB_TARGET)
	$(MAKE) -C $@


.PHONY: clean distclean

clean:
	for subdir in $(APPS); do $(MAKE) -C $$subdir clean; done
	for file in $(CLEANEXTS); do rm -f *.$$file; done

distclean: clean
	rm -rf $(INSTALL_PATH)
