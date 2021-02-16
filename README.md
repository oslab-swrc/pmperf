## Pmperf: Performance Monitoring Library for Persistent Memory Programms

Pmperf is a c++ library that provides functionalities of reading the performance counter and exporting results to files for persistent memory(PMem) programs.

### Dependencies
Pmperf uses Intel's PCM (https://github.com/opcm/pcm) library and libipmctl.
We had tested this library with an Intel Optane PMM installed Ubuntu server.

#### Install [ndctl](https://github.com/pmem/ndctl.git) & [ipmctl](https://github.com/intel/ipmctl.git) from Source

To build ipmctl, we need libndctl. We had tested with v71.1. 

<pre>
 $ git clone https://github.com/pmem/ndctl.git
 $ cd ndctl/
 $ git checkout tags/v71.1
 $ ./autogen.sh
 $ ./configure CFLAGS='-g -O2' --prefix=/usr --sysconfdir=/etc --libdir=/usr/lib
 $ make
 $ sudo make install
 $ sudo ldconfig
</pre>

If you want to check if ndctl is installed correctly, use the command below. If y is displayed, the installation was successful.
<pre>
 $ pkg-config "libndctl >= 63" && echo y || echo n
 $ pkg-config "libdaxctl >= 63" && echo y || echo n
</pre>

<pre>
 $ git clone https://github.com/intel/ipmctl.git
 $ cd ipmctl
 $ git checkout tags/v02.00.00.3833
 $ mkdir output && cd output
 $ cmake -DRELEASE=ON -DCMAKE_INSTALL_PREFIX=/usr ..
 $ make -j all
 $ sudo make install
 $ pkg-config "libipmctl" && echo y || echo n
</pre>
If y is displayed after last command, the installation was successful.


#### Install [PCM](https://github.com/opcm/pcm)
<pre>
 $ git clone https://github.com/opcm/pcm
 $ cd pcm
 & git checkout tags/202011
 $ make -j
</pre>

You can add `CXXFLAGS += -DPCM_SILENT` to Makefile to reduce the number of messages produced by PCM.
 
### Building Pmperf Library
<pre>
 $ git clone https://github.com/oslab-swrc/pmperf.git
 $ cd pmperf
</pre>
Open `Makefile` and change the PCM_PATH variable to the location of the PCM library you installed.
<pre>
 $ make
</pre>

### Test
We implemented a simple example in the *test* directory.
To run programs using the PCM library, you need root permission and the *msr* kernel module.
<pre>
	# modprobe msr
</pre>
Run *pmperf_test*.

## License
Pmperf is under the MIT license (https://opensource.org/licenses/MIT).
Copyright for Pmperf is held by the ETRI.

## Acknowledgements


## Contact
Please contact us at `youngjoo@etri.re.kr` with any questions.
