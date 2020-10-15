## Pmperf: Performance Monitoring Library for Persistent Memory Programms

Pmperf is a c++ library that provides functionalities of reading the performance counter and exporting results to files for persistent memory(PMem) programs.

### Dependencies
Pmperf uses Intel's PCM (https://github.com/opcm/pcm) library and ipmctl tool.
We had tested this library with an Intel Optane PMM installed Ubuntu server.

#### Install [ipmctl](https://github.com/intel/ipmctl.git)
<pre>
 $ git clone https://github.com/intel/ipmctl.git
 $ cd ipmctl
 $ mkdir output && cd output
 $ cmake -DRELEASE=ON -DCMAKE_INSTALL_PREFIX=/ ..
 $ make -j all
 $ sudo make install
</pre>

#### Install [PCM](https://github.com/opcm/pcm)
<pre>
 $ git clone https://github.com/opcm/pcm
 $ cd pcm
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
