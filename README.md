# rayTrace

To make necessary input files: run make_inputfile.py

Edits can be made to the variables in lines 44-53 of this script to change input files.

To run python version of rayTrace: run rt_run.py [inputfile] [outputfile]

You can also just run on default inputs: run rt_run.py

rt_run.py run functions in rt_function.  These must be in the same foulder.

To run fortran version first move .inc and .h files into include folder.

Then compile: make or make all

Then ./rayTrace [inputfile]
